#!/usr/bin/env python3
"""
Configuration module for FastAPI-Authlib-Keycloak.

This module handles loading and management of configuration settings
from environment variables and explicit parameters.
"""

import os
from typing import List, Optional, Dict, Any, Union


class Config:
    """Configuration class for FastAPI-Authlib-Keycloak."""

    def __init__(self):
        """Initialize configuration with default values."""
        # Keycloak settings
        self.keycloak_url = ""
        self.keycloak_realm = ""
        
        # Client settings
        self.client_id = ""
        self.client_secret = ""
        self.api_client_id = ""
        self.api_client_secret = ""
        
        # API settings
        self.api_base_url = ""
        
        # Session settings
        self.session_secret = ""
        self.session_max_age = 3600
        self.session_https_only = False
        self.session_same_site = "lax"
        
        # CORS settings
        self.cors_origins = ["*"]
        self.cors_credentials = True
        
        # Security settings
        self.token_algorithm = "RS256"
        self.strict_client_check = False
        
        # SSL settings
        self.ssl_enabled = False
        self.ssl_cert_file = ""
        self.ssl_key_file = ""
        self.ssl_cert_verify = True
        
        # Swagger UI settings
        self.custom_swagger_title = None
        self.custom_swagger_css = None
        
        # Debug settings
        self.debug_endpoints_enabled = False
    
    def update(self, values: Dict[str, Any]):
        """
        Update configuration with values from a dictionary.
        
        Args:
            values: Dictionary of configuration values
        """
        for key, value in values.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)


def load_config_from_env() -> Dict[str, Any]:
    """
    Load configuration values from environment variables.
    
    Returns:
        Dict[str, Any]: Dictionary of configuration values
    """
    # Define mapping of environment variables to config attributes
    env_mappings = {
        "KEYCLOAK_URL": "keycloak_url",
        "KEYCLOAK_REALM": "keycloak_realm",
        "CLIENT_ID": "client_id",
        "CLIENT_SECRET": "client_secret",
        "API_CLIENT_ID": "api_client_id",
        "API_CLIENT_SECRET": "api_client_secret",
        "API_BASE_URL": "api_base_url",
        "SESSION_SECRET": "session_secret",
        "SESSION_MAX_AGE": ("session_max_age", int),
        "SESSION_HTTPS_ONLY": ("session_https_only", lambda v: v.lower() == "true"),
        "SESSION_SAME_SITE": "session_same_site",
        "CORS_ORIGINS": ("cors_origins", lambda v: [s.strip() for s in v.split(",")]),
        "CORS_CREDENTIALS": ("cors_credentials", lambda v: v.lower() == "true"),
        "TOKEN_ALGORITHM": "token_algorithm",
        "STRICT_CLIENT_CHECK": ("strict_client_check", lambda v: v.lower() == "true"),
        "SSL_ENABLED": ("ssl_enabled", lambda v: v.lower() == "true"),
        "SSL_CERT_FILE": "ssl_cert_file",
        "SSL_KEY_FILE": "ssl_key_file",
        "SSL_CERT_VERIFY": ("ssl_cert_verify", lambda v: v.lower() == "true"),
        "DEBUG_ENDPOINTS_ENABLED": ("debug_endpoints_enabled", lambda v: v.lower() == "true"),
    }
    
    # Load values from environment
    config_values = {}
    
    for env_name, config_info in env_mappings.items():
        env_value = os.environ.get(env_name)
        
        if env_value is not None:
            # Handle simple string mapping or tuple with converter function
            if isinstance(config_info, tuple):
                config_name, converter = config_info
                try:
                    config_values[config_name] = converter(env_value)
                except Exception:
                    # Skip if conversion fails
                    pass
            else:
                config_values[config_info] = env_value
    
    return config_values
