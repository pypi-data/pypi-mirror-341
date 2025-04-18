#!/usr/bin/env python3
"""
Main module for FastAPI-Authlib-Keycloak integration.

This module provides the KeycloakAuth class, which is the main entry point
for integrating FastAPI applications with Keycloak authentication.
"""

import os
import logging
from typing import List, Optional, Dict, Callable, Any, Union

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from fastapi_authlib_keycloak.auth.oauth import setup_oauth
from fastapi_authlib_keycloak.auth.validator import create_validator
from fastapi_authlib_keycloak.auth.dependencies import (
    create_get_token_header,
    create_get_current_user,
    create_require_roles
)
from fastapi_authlib_keycloak.auth.routes import create_auth_router
from fastapi_authlib_keycloak.ui.swagger import setup_swagger_ui
from fastapi_authlib_keycloak.utils.ssl_utils import setup_ssl
from fastapi_authlib_keycloak.models import User
from fastapi_authlib_keycloak.config import Config, load_config_from_env


class KeycloakAuth:
    """
    Main class for FastAPI + Keycloak integration.
    
    This class provides a simple interface for adding Keycloak authentication
    to FastAPI applications with enhanced Swagger UI integration.
    
    Attributes:
        config: Configuration object with all settings
        get_current_user: Dependency for getting the current user
        require_roles: Function factory for role-based access control
    """

    def __init__(
        self,
        app: FastAPI,
        keycloak_url: str = "",
        keycloak_realm: str = "",
        client_id: str = "",
        client_secret: str = "",
        api_base_url: Optional[str] = None,
        api_client_id: Optional[str] = None,
        api_client_secret: Optional[str] = None,
        session_secret: Optional[str] = None,
        session_max_age: int = 3600,
        session_https_only: bool = False,
        session_same_site: str = "lax",
        cors_origins: List[str] = None,
        cors_credentials: bool = True,
        ssl_enabled: bool = False,
        ssl_cert_file: Optional[str] = None,
        ssl_key_file: Optional[str] = None,
        custom_swagger_title: Optional[str] = None,
        custom_swagger_css: Optional[str] = None,
        load_from_env: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize Keycloak authentication for a FastAPI application.
        
        Args:
            app: FastAPI application instance
            keycloak_url: URL of the Keycloak server (e.g., https://keycloak.example.com/auth)
            keycloak_realm: Keycloak realm name
            client_id: Client ID for the UI client
            client_secret: Client secret for the UI client
            api_base_url: Base URL for the API (defaults to request base URL if not provided)
            api_client_id: Client ID for the API client (if different from UI client)
            api_client_secret: Client secret for the API client
            session_secret: Secret key for session encryption
            session_max_age: Maximum session age in seconds
            session_https_only: Whether session cookies should be HTTPS only
            session_same_site: Same-site policy for cookies (lax, strict, none)
            cors_origins: List of allowed CORS origins
            cors_credentials: Whether to allow credentials in CORS
            ssl_enabled: Whether to enable SSL certificate verification
            ssl_cert_file: Path to SSL certificate file
            ssl_key_file: Path to SSL key file
            custom_swagger_title: Custom title for Swagger UI
            custom_swagger_css: Path to custom CSS file for Swagger UI
            load_from_env: Whether to load configuration from environment variables
            logger: Logger instance to use (creates a new one if not provided)
        """
        # Initialize logger
        self.logger = logger or logging.getLogger("fastapi-keycloak")
        self.logger.setLevel(logging.INFO)
        
        # Load configuration
        self.config = self._load_config(
            load_from_env=load_from_env,
            keycloak_url=keycloak_url,
            keycloak_realm=keycloak_realm,
            client_id=client_id,
            client_secret=client_secret,
            api_base_url=api_base_url,
            api_client_id=api_client_id,
            api_client_secret=api_client_secret,
            session_secret=session_secret,
            session_max_age=session_max_age,
            session_https_only=session_https_only,
            session_same_site=session_same_site,
            cors_origins=cors_origins or ["*"],
            cors_credentials=cors_credentials,
            ssl_enabled=ssl_enabled,
            ssl_cert_file=ssl_cert_file,
            ssl_key_file=ssl_key_file,
            custom_swagger_title=custom_swagger_title,
            custom_swagger_css=custom_swagger_css,
        )
        
        # Store app reference
        self.app = app
        
        # Set up SSL if enabled
        if self.config.ssl_enabled:
            self._setup_ssl()
        
        # Set up middleware
        self._setup_middleware(app)
        
        # Set up authentication
        self._setup_auth(app)
        
        # Set up Swagger UI
        self._setup_swagger_ui(app)
        
        # Initialize dependencies
        self._init_dependencies()
    
    def _load_config(self, load_from_env: bool = True, **kwargs) -> Config:
        """
        Load configuration from environment variables and/or keyword arguments.
        
        Args:
            load_from_env: Whether to load from environment variables
            **kwargs: Override configuration values
            
        Returns:
            Config: Configuration object
        """
        config = Config()
        
        if load_from_env:
            # Load values from environment
            env_config = load_config_from_env()
            config.update(env_config)
        
        # Override with kwargs
        for key, value in kwargs.items():
            if value is not None:  # Only set if not None
                setattr(config, key, value)
        
        # Validate required configuration
        required_fields = ["keycloak_url", "keycloak_realm", "client_id", "client_secret"]
        missing_fields = [field for field in required_fields if not getattr(config, field)]
        
        if missing_fields:
            fields_str = ", ".join(missing_fields)
            self.logger.error(f"Missing required configuration: {fields_str}")
            raise ValueError(
                f"Missing required configuration: {fields_str}. "
                f"Please provide these values through environment variables or constructor parameters."
            )
        
        # Generate default api_client_id and api_client_secret if not provided
        if not config.api_client_id:
            config.api_client_id = config.client_id
        
        if not config.api_client_secret:
            config.api_client_secret = config.client_secret
        
        # Generate session secret if not provided
        if not config.session_secret:
            config.session_secret = os.urandom(24).hex()
            self.logger.warning("No session secret provided, generated a random one. "
                               "This will cause sessions to be invalidated on restart.")
        
        return config
    
    def _setup_ssl(self):
        """Set up SSL certificate verification."""
        self.logger.info("Setting up SSL certificate verification")
        setup_ssl(
            ssl_cert_file=self.config.ssl_cert_file,
            ssl_key_file=self.config.ssl_key_file,
            logger=self.logger
        )
    
    def _setup_middleware(self, app: FastAPI):
        """
        Set up required middleware.
        
        Args:
            app: FastAPI application instance
        """
        self.logger.info("Setting up middleware")
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.cors_origins,
            allow_credentials=self.config.cors_credentials,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
            max_age=1800,
        )
        
        # Add session middleware for OAuth flows
        app.add_middleware(
            SessionMiddleware,
            secret_key=self.config.session_secret,
            max_age=self.config.session_max_age,
            same_site=self.config.session_same_site,
            https_only=self.config.session_https_only,
            path="/",
        )
    
    def _setup_auth(self, app: FastAPI):
        """
        Set up authentication routes and OAuth client.
        
        Args:
            app: FastAPI application instance
        """
        self.logger.info("Setting up authentication")
        
        # Initialize OAuth client
        self.oauth = setup_oauth(
            keycloak_url=self.config.keycloak_url,
            keycloak_realm=self.config.keycloak_realm,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            ssl_enabled=self.config.ssl_enabled,
            ssl_cert_file=self.config.ssl_cert_file,
            logger=self.logger
        )
        
        # Create token validator
        self.validator = create_validator(
            keycloak_url=self.config.keycloak_url,
            keycloak_realm=self.config.keycloak_realm,
            client_id=self.config.client_id,
            api_client_id=self.config.api_client_id,
            strict_client_check=self.config.strict_client_check,
            ssl_cert_file=self.config.ssl_cert_file if self.config.ssl_enabled else None,
            logger=self.logger
        )
        
        # Create auth router
        auth_router = create_auth_router(
            oauth=self.oauth,
            validator=self.validator,
            keycloak_url=self.config.keycloak_url,
            keycloak_realm=self.config.keycloak_realm,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            api_client_id=self.config.api_client_id,
            api_client_secret=self.config.api_client_secret,
            api_base_url=self.config.api_base_url,
            logger=self.logger
        )
        
        # Include auth router in app
        app.include_router(auth_router)
    
    def _setup_swagger_ui(self, app: FastAPI):
        """
        Set up custom Swagger UI.
        
        Args:
            app: FastAPI application instance
        """
        self.logger.info("Setting up Swagger UI")
        
        setup_swagger_ui(
            app=app,
            keycloak_url=self.config.keycloak_url,
            keycloak_realm=self.config.keycloak_realm,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            api_base_url=self.config.api_base_url,
            custom_title=self.config.custom_swagger_title,
            custom_css_path=self.config.custom_swagger_css,
            logger=self.logger
        )
    
    def _init_dependencies(self):
        """Initialize dependencies for route protection."""
        self.logger.info("Initializing authentication dependencies")
        
        # Set up security scheme
        self.security = HTTPBearer()
        
        # Create dependency functions
        get_token_header_func = create_get_token_header(
            security=self.security,
            validator=self.validator
        )
        
        self.get_current_user = create_get_current_user(
            get_token_header=get_token_header_func,
            logger=self.logger
        )
        
        self.require_roles = create_require_roles(
            get_current_user=self.get_current_user,
            logger=self.logger
        )

    def verify_token(self, token: str) -> Dict:
        """
        Verify a JWT token and return the decoded claims.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Dict: Decoded token claims
        
        Raises:
            HTTPException: If token verification fails
        """
        return self.validator.validate_token(token)
