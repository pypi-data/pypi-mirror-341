#!/usr/bin/env python3
"""
OAuth module for FastAPI-Authlib-Keycloak integration.

This module initializes the OAuth client for Keycloak integration.
"""

import logging
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi_authlib_keycloak.utils.ssl_utils import configure_oauth_ssl


def setup_oauth(
    keycloak_url: str,
    keycloak_realm: str,
    client_id: str,
    client_secret: str,
    ssl_enabled: bool = False,
    ssl_cert_file: Optional[str] = None,
    logger: Optional[logging.Logger] = None
) -> OAuth:
    """
    Set up OAuth client for Keycloak.
    
    Args:
        keycloak_url: URL of the Keycloak server
        keycloak_realm: Keycloak realm name
        client_id: Client ID
        client_secret: Client secret
        ssl_enabled: Whether SSL verification is enabled
        ssl_cert_file: Path to SSL certificate file
        logger: Logger instance
        
    Returns:
        OAuth: Configured OAuth client
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.oauth")
    
    # Initialize OAuth
    oauth = OAuth()
    
    # Get client kwargs with SSL configuration if needed
    client_kwargs = configure_oauth_ssl(
        ssl_enabled=ssl_enabled, 
        ssl_cert_file=ssl_cert_file
    )
    
    # Register Keycloak as an OAuth provider
    oauth.register(
        name="keycloak",
        server_metadata_url=f"{keycloak_url}/realms/{keycloak_realm}/.well-known/openid-configuration",
        client_id=client_id,
        client_secret=client_secret,
        client_kwargs=client_kwargs
    )
    
    logger.info(f"OAuth client initialized for {keycloak_url}/realms/{keycloak_realm}")
    
    return oauth
