#!/usr/bin/env python3
"""
SSL Utilities for FastAPI-Authlib-Keycloak Integration.

This module provides utilities for managing SSL certificates in the application.
"""

import os
import shutil
import logging
import urllib.request
from pathlib import Path
from typing import Optional, Dict


def setup_ssl(
    ssl_cert_file: Optional[str] = None,
    ssl_key_file: Optional[str] = None,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Set up SSL certificate verification.
    
    Args:
        ssl_cert_file: Path to SSL certificate file
        ssl_key_file: Path to SSL key file
        logger: Logger instance
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Initialize logger if not provided
    logger = logger or logging.getLogger("fastapi-keycloak.ssl")
    
    # Basic validation
    if not ssl_cert_file or not os.path.isfile(ssl_cert_file):
        logger.error(f"SSL certificate file not found: {ssl_cert_file}")
        return False
    
    if ssl_key_file and not os.path.isfile(ssl_key_file):
        logger.warning(f"SSL key file not found: {ssl_key_file}")
    
    # Install certificate in certifi
    cert_installed = install_cert_in_certifi(ssl_cert_file, logger)
    
    # Set environment variables
    env_vars_set = set_ssl_cert_env_vars(ssl_cert_file, logger)
    
    return cert_installed and env_vars_set


def install_cert_in_certifi(
    ssl_cert_file: str,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Install the certificate in the certifi bundle for Python requests.
    
    This allows libraries like requests and httpx to verify the
    Keycloak server's SSL certificate.
    
    Args:
        ssl_cert_file: Path to SSL certificate file
        logger: Logger instance
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize logger if not provided
        logger = logger or logging.getLogger("fastapi-keycloak.ssl")
        
        # Get the certifi CA bundle path
        try:
            import certifi
            certifi_path = certifi.where()
            logger.info(f"Certifi CA bundle located at: {certifi_path}")
        except ImportError:
            logger.error("certifi package not installed. Install it with 'pip install certifi'")
            return False
        
        # Check if certificate file exists
        if not os.path.isfile(ssl_cert_file):
            logger.error(f"SSL certificate file not found: {ssl_cert_file}")
            return False
            
        # Read the certificate file content
        with open(ssl_cert_file, 'r') as cert_file:
            cert_content = cert_file.read()
            
        # Append the certificate to the certifi bundle
        # First, make a backup of the original bundle
        certifi_backup = certifi_path + '.backup'
        if not os.path.exists(certifi_backup):
            logger.info(f"Creating backup of certifi bundle: {certifi_backup}")
            shutil.copy2(certifi_path, certifi_backup)
        
        # Append the certificate
        with open(certifi_path, 'a') as ca_bundle:
            ca_bundle.write('\n')
            ca_bundle.write(cert_content)
            
        logger.info(f"Certificate successfully added to certifi bundle")
        return True
        
    except Exception as e:
        if logger:
            logger.error(f"Error installing certificate in certifi: {str(e)}")
        return False


def set_ssl_cert_env_vars(
    ssl_cert_file: str,
    logger: Optional[logging.Logger] = None
) -> bool:
    """
    Set environment variables for SSL certificate verification.
    
    This ensures that libraries like requests, httpx, and urllib use
    the correct certificate for verification.
    
    Args:
        ssl_cert_file: Path to SSL certificate file
        logger: Logger instance
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize logger if not provided
        logger = logger or logging.getLogger("fastapi-keycloak.ssl")
        
        # Set environment variables for certificate verification
        os.environ['REQUESTS_CA_BUNDLE'] = ssl_cert_file
        os.environ['SSL_CERT_FILE'] = ssl_cert_file
        
        # Configure urllib to use our certificate
        try:
            # Create an SSL context with our certificate
            import ssl
            ssl_context = ssl.create_default_context(cafile=ssl_cert_file)
            # Install it as the default HTTPS context
            urllib.request.install_opener(
                urllib.request.build_opener(
                    urllib.request.HTTPSHandler(context=ssl_context)
                )
            )
            logger.info("SSL context configured for urllib")
        except Exception as ssl_ctx_error:
            logger.error(f"Error configuring SSL context for urllib: {str(ssl_ctx_error)}")
            
        logger.info("SSL environment variables set successfully")
        return True
        
    except Exception as e:
        if logger:
            logger.error(f"Error setting SSL environment variables: {str(e)}")
        return False


def configure_oauth_ssl(
    ssl_enabled: bool = False,
    ssl_cert_file: Optional[str] = None
) -> Dict[str, any]:
    """
    Configure SSL certificate verification for the OAuth client.
    
    Args:
        ssl_enabled: Whether SSL verification is enabled
        ssl_cert_file: Path to SSL certificate file
    
    Returns:
        dict: Client kwargs with SSL configuration
    """
    client_kwargs = {
        "scope": "openid email profile",
    }
    
    if ssl_enabled and ssl_cert_file:
        client_kwargs["verify"] = ssl_cert_file
    
    return client_kwargs
