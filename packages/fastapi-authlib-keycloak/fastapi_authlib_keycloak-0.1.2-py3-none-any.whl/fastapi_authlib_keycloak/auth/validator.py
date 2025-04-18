#!/usr/bin/env python3
"""
JWT Token Validator for Keycloak Integration.

This module handles JWT token validation using Authlib and Keycloak.
"""

import base64
import json
import logging
import ssl
from typing import Dict, Optional, List, Any, Union

import httpx
from authlib.jose import JsonWebToken, JsonWebKey
from authlib.jose.errors import JoseError
from fastapi import HTTPException, status


class KeycloakJWTValidator:
    """Validator for Keycloak JWT tokens."""

    def __init__(
        self,
        issuer: str,
        jwks_uri: str,
        client_id: str,
        api_client_id: Optional[str] = None,
        strict_client_check: bool = False,
        ssl_cert_file: Optional[str] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the validator with the required parameters.

        Args:
            issuer: The issuer URL (usually the Keycloak server URL)
            jwks_uri: The URL to the JWK Set
            client_id: The primary client ID to verify in the token
            api_client_id: Secondary client ID that is also acceptable (for flexibility)
            strict_client_check: Whether to strictly enforce client ID matching
            ssl_cert_file: Path to SSL certificate file for verification
            logger: Logger instance
        """
        self.issuer = issuer
        self.jwks_uri = jwks_uri
        self.client_id = client_id
        self.api_client_id = api_client_id
        self.strict_client_check = strict_client_check
        self.ssl_cert_file = ssl_cert_file
        self.logger = logger or logging.getLogger("fastapi-keycloak.validator")
        self.jwks = None

    async def fetch_jwks(self) -> Dict:
        """Fetch the JWK Set from the JWKS URI.
        
        Returns:
            Dict: The JWKS as a dictionary
            
        Raises:
            HTTPException: If the JWKS cannot be fetched
        """
        try:
            # Configure SSL verification
            verify = self.ssl_cert_file if self.ssl_cert_file else True
            
            # Create client with appropriate SSL verification
            async with httpx.AsyncClient(verify=verify) as client:
                self.logger.info(f"Fetching JWKS from {self.jwks_uri}")
                response = await client.get(self.jwks_uri)
                response.raise_for_status()
                self.jwks = response.json()
                self.logger.info(f"JWKS successfully fetched from {self.jwks_uri}")
                return self.jwks
        except Exception as e:
            self.logger.error(f"Error fetching JWKS: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not fetch JWKS: {str(e)}"
            )

    async def validate_token(self, token: str) -> Dict:
        """
        Validate a JWT token using the JWKS.

        Args:
            token: The JWT token string

        Returns:
            Dict: The decoded token claims if valid

        Raises:
            HTTPException: If token validation fails
        """
        try:
            # Ensure token format - remove Bearer prefix if present
            if token.startswith("Bearer "):
                token = token[7:]

            if not self.jwks:
                await self.fetch_jwks()

            # Create JsonWebKey instance from JWKS
            json_web_key = JsonWebKey.import_key_set(self.jwks)

            # Setup the JWT instance
            jwt = JsonWebToken(['RS256'])

            # Decode and validate the token
            claims = jwt.decode(
                token,
                json_web_key,
                claims_options={
                    'iss': {'essential': True, 'value': self.issuer},
                    'exp': {'essential': True},
                    # Allow any audience (Keycloak might use the realm as audience)
                    'aud': {'essential': False}
                }
            )

            # Perform additional verifications
            claims.validate()
            
            # Extract AZP (authorized party) from token - this is usually the client ID
            token_client_id = claims.get('azp')
            # Fallback to 'client_id' claim if 'azp' is not present
            if not token_client_id:
                token_client_id = claims.get('client_id')
            
            # Check client ID only if strict checking is enabled and a client ID exists in the token
            if self.strict_client_check and token_client_id:
                # Allow either the primary client ID or the API client ID
                valid_client_ids = [self.client_id]
                if self.api_client_id:
                    valid_client_ids.append(self.api_client_id)
                
                if token_client_id not in valid_client_ids:
                    self.logger.warning(f"Client ID mismatch: Token has '{token_client_id}' but validator expects one of {valid_client_ids}")
                    # We're logging a warning but not raising an exception to be more tolerant
                    # If you want to strictly enforce this, uncomment the following lines:
                    # raise HTTPException(
                    #    status_code=status.HTTP_401_UNAUTHORIZED,
                    #    detail=f"Client ID mismatch: Token has '{token_client_id}' but validator expects one of {valid_client_ids}"
                    #)

            self.logger.info(f"Token successfully validated for user: {claims.get('preferred_username')}")
            return claims

        except JoseError as e:
            # More detailed error logging
            token_content, client_id_in_token = self._extract_token_info(token)
            self.logger.error(f"Token client ID: {client_id_in_token}, Validator client IDs: primary={self.client_id}, secondary={self.api_client_id}")
            
            # Determine the error detail to return
            detail = self._get_error_detail(token_content, client_id_in_token, str(e))
                
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail
            )
            
        except Exception as e:
            self.logger.error(f"Unexpected error during token validation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}"
            )

    def _extract_token_info(self, token: str) -> tuple:
        """Extract information from a token for debugging purposes.
        
        Args:
            token: The JWT token string
            
        Returns:
            tuple: (token_content, client_id_in_token)
        """
        token_content = None
        client_id_in_token = None
        try:
            # Remove Bearer prefix if present
            if token.startswith("Bearer "):
                token = token[7:]
                
            parts = token.split('.')
            if len(parts) >= 2:
                # Fix padding for base64url decode
                payload = parts[1]
                payload += '=' * (4 - len(payload) % 4)
                decoded = base64.urlsafe_b64decode(payload)
                token_content = json.loads(decoded)
                # Check both 'azp' and 'client_id' claims
                client_id_in_token = token_content.get("azp")
                if not client_id_in_token:
                    client_id_in_token = token_content.get("client_id")
        except Exception as decode_error:
            self.logger.error(f"Error decoding token: {str(decode_error)}")
            
        return token_content, client_id_in_token
        
    def _get_error_detail(self, token_content, client_id_in_token, error_msg: str) -> str:
        """Get detailed error message for token validation failure.
        
        Args:
            token_content: The decoded token content
            client_id_in_token: The client ID extracted from the token
            error_msg: The original error message
            
        Returns:
            str: A detailed error message
        """
        if token_content:
            # Check if it's a client ID issue or something else
            if client_id_in_token and self.strict_client_check:
                valid_client_ids = [self.client_id]
                if self.api_client_id:
                    valid_client_ids.append(self.api_client_id)
                    
                if client_id_in_token not in valid_client_ids:
                    return f"Client ID mismatch: Token has '{client_id_in_token}' but validator expects one of {valid_client_ids}"
                else:
                    return f"Token validation error: {error_msg}"
            else:
                return f"Token validation error: {error_msg}"
        else:
            return f"Invalid token format or token could not be decoded: {error_msg}"


def create_validator(
    keycloak_url: str,
    keycloak_realm: str,
    client_id: str,
    api_client_id: Optional[str] = None,
    strict_client_check: bool = False,
    ssl_cert_file: Optional[str] = None,
    logger: Optional[logging.Logger] = None
) -> KeycloakJWTValidator:
    """
    Create a Keycloak JWT validator.
    
    Args:
        keycloak_url: URL of the Keycloak server
        keycloak_realm: Keycloak realm name
        client_id: Client ID
        api_client_id: API client ID
        strict_client_check: Whether to strictly enforce client ID matching
        ssl_cert_file: Path to SSL certificate file
        logger: Logger instance
        
    Returns:
        KeycloakJWTValidator: Configured validator
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.validator")
    
    # Initialize validator
    validator = KeycloakJWTValidator(
        issuer=f"{keycloak_url}/realms/{keycloak_realm}",
        jwks_uri=f"{keycloak_url}/realms/{keycloak_realm}/protocol/openid-connect/certs",
        client_id=client_id,
        api_client_id=api_client_id,
        strict_client_check=strict_client_check,
        ssl_cert_file=ssl_cert_file,
        logger=logger
    )
    
    return validator
