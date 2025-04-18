#!/usr/bin/env python3
"""
Main module for FastAPI-Authlib-Keycloak integration.

This module provides the KeycloakAuth class, which is the main entry point
for integrating FastAPI applications with Keycloak authentication.
"""

import os
import logging
import warnings
from typing import List, Optional, Dict, Callable, Any, Union

from fastapi import FastAPI, Depends, Request, Response
from fastapi.security import HTTPBearer
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from fastapi_authlib_keycloak.auth.oauth import setup_oauth
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

# Import enhanced JWT validator
from fastapi_authlib_keycloak.auth.enhanced_validator import (
    create_enhanced_validator,
    TokenValidationMethod
)

# Import the metrics module if available
try:
    from fastapi_authlib_keycloak.utils.metrics import (
        configure_metrics,
        create_fastapi_metrics_endpoint,
        MetricsMiddleware,
        MetricsBackend,
        get_metrics_status
    )
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False

# Import the debug module if available
try:
    from fastapi_authlib_keycloak.utils.debug import (
        create_debug_router,
        init_debug_environment,
        DebugLogger
    )
    DEBUG_AVAILABLE = True
except ImportError:
    DEBUG_AVAILABLE = False

# Import the rate limiting module if available
try:
    from fastapi_authlib_keycloak.utils.rate_limit import (
        create_rate_limiter,
        RateLimitMiddleware,
        RateLimitStrategy,
        RateLimitScope
    )
    RATE_LIMIT_AVAILABLE = True
except ImportError:
    RATE_LIMIT_AVAILABLE = False

# Import pydantic config if available
try:
    from fastapi_authlib_keycloak.pydantic_config import KeycloakAuthConfig
    PYDANTIC_CONFIG_AVAILABLE = True
except ImportError:
    PYDANTIC_CONFIG_AVAILABLE = False


class KeycloakAuth:
    """
    Main class for FastAPI + Keycloak integration.
    
    This class provides a simple interface for adding Keycloak authentication
    to FastAPI applications with enhanced Swagger UI integration, metrics
    collection, and debugging utilities.
    
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
        ssl_verify: Union[bool, str] = True,
        development_mode: bool = False,
        allow_http: bool = False,
        jwks_cache_ttl: int = 3600,
        jwks_file: Optional[str] = None,
        on_ssl_error: str = "raise",
        custom_swagger_title: Optional[str] = None,
        custom_swagger_css: Optional[str] = None,
        validation_method: str = "jwt",
        strict_client_check: bool = False,
        metrics_enabled: bool = False,
        metrics_route: str = "/metrics",
        health_route: str = "/health/keycloak",
        debug_endpoints_enabled: bool = False,
        log_level: str = "INFO",
        introspection_cache_ttl: int = 300,
        rate_limit_enabled: bool = False,
        rate_limit_max_requests: int = 100,
        rate_limit_window_seconds: int = 60,
        rate_limit_strategy: str = "sliding",
        rate_limit_scope: str = "ip",
        rate_limit_use_redis: bool = False,
        rate_limit_redis_url: str = "redis://localhost:6379/0",
        load_from_env: bool = True,
        config_object: Optional[Any] = None,
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
            ssl_verify: SSL verification mode (True for standard verification,
                False to disable verification, or string path to a CA bundle)
            development_mode: Whether to enable development-friendly defaults
            allow_http: Allow HTTP for Keycloak URL (insecure, for development only)
            jwks_cache_ttl: Cache time for JWKS in seconds
            jwks_file: Path to a local JWKS file (for offline verification)
            on_ssl_error: How to handle SSL errors ('raise', 'warn', or 'ignore')
            custom_swagger_title: Custom title for Swagger UI
            custom_swagger_css: Path to custom CSS file for Swagger UI
            validation_method: Method for token validation (jwt, introspection, both)
            strict_client_check: Whether to strictly enforce client ID matching in tokens
            metrics_enabled: Whether to enable metrics collection
            metrics_route: Route for metrics endpoint
            health_route: Route for health check endpoint
            debug_endpoints_enabled: Whether to enable debug endpoints
            log_level: Logging level
            introspection_cache_ttl: Cache time for introspection results in seconds
            rate_limit_enabled: Whether to enable rate limiting
            rate_limit_max_requests: Maximum number of requests per window
            rate_limit_window_seconds: Time window for rate limiting in seconds
            rate_limit_strategy: Rate limiting strategy (fixed, sliding, token_bucket)
            rate_limit_scope: Scope for rate limiting (ip, client, user)
            rate_limit_use_redis: Whether to use Redis for rate limiting storage
            rate_limit_redis_url: Redis URL for rate limiting storage
            load_from_env: Whether to load configuration from environment variables
            config_object: Optional configuration object to use instead of parameters
            logger: Logger instance to use (creates a new one if not provided)
        """
        # Initialize logger
        self.logger = logger or logging.getLogger("fastapi-keycloak")
        self.logger.setLevel(getattr(logging, log_level))
        
        # Initialize debug logger if available
        self.debug_logger = None
        if DEBUG_AVAILABLE:
            self.debug_logger = DebugLogger(
                name="fastapi-keycloak.debug",
                level=log_level,
                include_timestamp=True,
                include_trace_id=True
            )
        
        # Load configuration
        if config_object is not None:
            # Use provided config object
            if PYDANTIC_CONFIG_AVAILABLE and isinstance(config_object, KeycloakAuthConfig):
                # Convert to legacy config for now
                # TODO: Update to use pydantic config directly in future versions
                self.config = config_object.get_legacy_config()
            else:
                self.config = config_object
        else:
            # Load from parameters and environment
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
                ssl_verify=ssl_verify,
                development_mode=development_mode,
                allow_http=allow_http,
                jwks_cache_ttl=jwks_cache_ttl,
                jwks_file=jwks_file,
                on_ssl_error=on_ssl_error,
                custom_swagger_title=custom_swagger_title,
                custom_swagger_css=custom_swagger_css,
                validation_method=validation_method,
                strict_client_check=strict_client_check,
                debug_endpoints_enabled=debug_endpoints_enabled,
                metrics_enabled=metrics_enabled,
                metrics_route=metrics_route,
                health_route=health_route,
                log_level=log_level,
                introspection_cache_ttl=introspection_cache_ttl,
                rate_limit_enabled=rate_limit_enabled,
                rate_limit_max_requests=rate_limit_max_requests,
                rate_limit_window_seconds=rate_limit_window_seconds,
                rate_limit_strategy=rate_limit_strategy,
                rate_limit_scope=rate_limit_scope,
                rate_limit_use_redis=rate_limit_use_redis,
                rate_limit_redis_url=rate_limit_redis_url,
            )
        
        # Store app reference
        self.app = app
        
        # Configure metrics if available
        self._setup_metrics()
        
        # Configure rate limiting if available
        self._setup_rate_limiting()
        
        # Initialize debug environment if in development mode
        self.mock_auth = None
        if self.config.development_mode and DEBUG_AVAILABLE:
            self.mock_auth = init_debug_environment(
                development_mode=self.config.development_mode,
                mock_issuer=f"{self.config.keycloak_url}/realms/{self.config.keycloak_realm}"
            )
        
        # Handle development mode
        if self.config.development_mode:
            self._setup_development_mode()
        
        # Set up SSL if enabled
        if self.config.ssl_enabled:
            self._setup_ssl()
        
        # Set up middleware
        self._setup_middleware(app)
        
        # Set up authentication
        self._setup_auth(app)
        
        # Set up Swagger UI
        self._setup_swagger_ui(app)
        
        # Set up health endpoints
        self._setup_health_endpoints(app)
        
        # Set up debug endpoints if enabled
        if self.config.debug_endpoints_enabled and DEBUG_AVAILABLE:
            self._setup_debug_endpoints(app)
        
        # Initialize dependencies
        self._init_dependencies()
        
        # Log initialization
        self.logger.info(
            f"FastAPI-Authlib-Keycloak initialized for Keycloak realm: "
            f"{self.config.keycloak_realm} at {self.config.keycloak_url}"
        )
    
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
        
        # Handle development mode settings
        if config.development_mode:
            # Log warning about development mode
            self.logger.warning(
                "Development mode enabled. This mode is not secure and should only be used in "
                "development environments. Do not use in production!"
            )
            
            # Set sensible development defaults if not explicitly overridden
            if not kwargs.get('allow_http'):
                config.allow_http = True
                self.logger.info("Development mode: Setting allow_http=True")
            
            if not kwargs.get('ssl_verify'):
                config.ssl_verify = False
                self.logger.info("Development mode: Setting ssl_verify=False")
            
            if not kwargs.get('on_ssl_error'):
                config.on_ssl_error = "warn"
                self.logger.info("Development mode: Setting on_ssl_error='warn'")
                
            if not kwargs.get('debug_endpoints_enabled'):
                config.debug_endpoints_enabled = True
                self.logger.info("Development mode: Setting debug_endpoints_enabled=True")
        
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
    
    def _setup_metrics(self):
        """Set up metrics collection if enabled."""
        if not hasattr(self.config, 'metrics_enabled') or not self.config.metrics_enabled:
            return
            
        if not METRICS_AVAILABLE:
            self.logger.warning("Metrics module not available, metrics collection disabled")
            return
            
        try:
            # Configure metrics
            backend = MetricsBackend.PROMETHEUS if METRICS_AVAILABLE else MetricsBackend.LOGGER
            
            configure_metrics(
                backend=backend,
                enabled=True,
                prefix="keycloak_auth_",
                labels={
                    "realm": self.config.keycloak_realm,
                    "client_id": self.config.client_id
                },
                log_level=getattr(self.config, 'log_level', "INFO")
            )
            
            # Create metrics endpoint
            metrics_route = getattr(self.config, 'metrics_route', "/metrics")
            metrics_endpoint = create_fastapi_metrics_endpoint(metrics_route)
            
            if metrics_endpoint:
                self.app.add_api_route(
                    metrics_route,
                    metrics_endpoint,
                    methods=["GET"],
                    tags=["metrics"],
                    summary="Prometheus metrics",
                    description="Expose Prometheus metrics for monitoring"
                )
                
                self.logger.info(f"Metrics endpoint registered at {metrics_route}")
                
            # Add metrics middleware
            self.app.add_middleware(MetricsMiddleware, enable_timing=True)
            
            self.logger.info("Metrics collection enabled")
        except Exception as e:
            self.logger.error(f"Failed to set up metrics: {str(e)}")
            
    def _setup_rate_limiting(self):
        """Set up rate limiting if enabled."""
        if not hasattr(self.config, 'rate_limit_enabled') or not self.config.rate_limit_enabled:
            return
            
        if not RATE_LIMIT_AVAILABLE:
            self.logger.warning("Rate limiting module not available, rate limiting disabled")
            return
            
        try:
            # Get configuration
            strategy = getattr(self.config, 'rate_limit_strategy', "sliding")
            max_requests = getattr(self.config, 'rate_limit_max_requests', 100)
            window_seconds = getattr(self.config, 'rate_limit_window_seconds', 60)
            scope = getattr(self.config, 'rate_limit_scope', "ip")
            use_redis = getattr(self.config, 'rate_limit_use_redis', False)
            redis_url = getattr(self.config, 'rate_limit_redis_url', "redis://localhost:6379/0")
            
            # Create rate limiter
            self.rate_limiter = create_rate_limiter(
                strategy=strategy,
                max_requests=max_requests,
                window_seconds=window_seconds,
                scope=scope,
                enabled=True,
                use_redis=use_redis,
                redis_url=redis_url,
                key_prefix="keycloak_auth_rate_limit:",
                strict_mode=True,
                logger=self.logger
            )
            
            # Define paths for rate limiting (token validation endpoints)
            include_paths = [
                "/auth/token",
                "/auth/token/validate",
                "/auth/userinfo",
                "/auth/login",
                "/auth/logout",
                "/auth/refresh"
            ]
            
            # Add rate limiting middleware for token validation endpoints
            self.app.add_middleware(
                RateLimitMiddleware,
                rate_limiter=self.rate_limiter,
                include_paths=include_paths
            )
            
            # Store the rate limiter for use in dependencies
            self.app.state.rate_limiter = self.rate_limiter
            
            self.logger.info(
                f"Rate limiting enabled: strategy={strategy}, max_requests={max_requests}, "
                f"window_seconds={window_seconds}, scope={scope}"
            )
        except Exception as e:
            self.logger.error(f"Failed to set up rate limiting: {str(e)}")
    
    def _setup_development_mode(self):
        """Set up development-friendly defaults for the application."""
        self.logger.warning("Setting up development mode environment")
        
        # Check if Keycloak URL uses HTTP
        if self.config.allow_http and self.config.keycloak_url.startswith('http://'):
            self.logger.warning(
                "Using HTTP for Keycloak URL. This is insecure and should only be used "
                "in development environments."
            )
        elif self.config.keycloak_url.startswith('http://') and not self.config.allow_http:
            self.logger.warning(
                "Keycloak URL uses HTTP but allow_http is False. This may cause issues. "
                "Set allow_http=True when using HTTP in development environments."
            )
    
    def _setup_ssl(self):
        """Set up SSL certificate verification."""
        self.logger.info("Setting up SSL certificate verification")
        
        # Determine SSL verification mode
        verify_mode = self.config.ssl_verify
        cert_file = self.config.ssl_cert_file
        
        # Log SSL verification mode
        if verify_mode is True:
            self.logger.info("SSL verification mode: Standard verification against trusted CAs")
        elif verify_mode is False:
            self.logger.warning(
                "SSL verification DISABLED. This is insecure and should only be used "
                "in development environments."
            )
        elif isinstance(verify_mode, str):
            self.logger.info(f"SSL verification mode: Using custom certificate at {verify_mode}")
            cert_file = verify_mode
        
        # Set up SSL verification
        setup_ssl(
            ssl_cert_file=cert_file,
            ssl_key_file=self.config.ssl_key_file,
            ssl_verify=verify_mode,
            on_ssl_error=self.config.on_ssl_error,
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
            ssl_verify=self.config.ssl_verify,
            ssl_cert_file=self.config.ssl_cert_file,
            allow_http=self.config.allow_http,
            development_mode=self.config.development_mode,
            logger=self.logger
        )
        
        # Create enhanced token validator
        token_validation_method = getattr(self.config, 'validation_method', "jwt")
        introspection_cache_ttl = getattr(self.config, 'introspection_cache_ttl', 300)
        
        self.validator = create_enhanced_validator(
            keycloak_url=self.config.keycloak_url,
            keycloak_realm=self.config.keycloak_realm,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            api_client_id=self.config.api_client_id,
            api_client_secret=self.config.api_client_secret,
            validation_method=token_validation_method,
            strict_client_check=self.config.strict_client_check,
            ssl_verify=self.config.ssl_verify,
            ssl_cert_file=self.config.ssl_cert_file,
            jwks_cache_ttl=self.config.jwks_cache_ttl,
            jwks_file=self.config.jwks_file,
            on_ssl_error=self.config.on_ssl_error,
            development_mode=self.config.development_mode,
            introspection_cache_ttl=introspection_cache_ttl,
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
    
    def _setup_health_endpoints(self, app: FastAPI):
        """
        Set up health check endpoints.
        
        Args:
            app: FastAPI application instance
        """
        health_route = getattr(self.config, 'health_route', "/health/keycloak")
        
        @app.get(
            health_route,
            tags=["health"],
            summary="Keycloak health check",
            description="Check the health and connectivity of the Keycloak server"
        )
        async def health_check():
            try:
                # Check validator health
                health_status = await self.validator.health_check()
                return health_status
            except Exception as e:
                self.logger.error(f"Health check failed: {str(e)}")
                return {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        self.logger.info(f"Health check endpoint registered at {health_route}")
        
    def _setup_debug_endpoints(self, app: FastAPI):
        """
        Set up debug endpoints for development.
        
        Args:
            app: FastAPI application instance
        """
        if not DEBUG_AVAILABLE:
            self.logger.warning("Debug module not available, debug endpoints disabled")
            return
            
        if not self.config.development_mode:
            self.logger.warning("Debug endpoints are only available in development mode")
            return
            
        try:
            # Create debug router
            debug_router = create_debug_router(
                development_mode=self.config.development_mode,
                mock_auth=self.mock_auth
            )
            
            # Include debug router in app
            app.include_router(debug_router)
            
            self.logger.info("Debug endpoints registered")
        except Exception as e:
            self.logger.error(f"Failed to set up debug endpoints: {str(e)}")
    
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
        
        # Add rate limiter as a dependency if enabled
        if hasattr(self, 'rate_limiter'):
            self.rate_limit = self.rate_limiter.get_dependency()
            self.logger.info("Rate limiting dependency initialized")

    async def verify_token(self, token: str) -> Dict:
        """
        Verify a JWT token and return the decoded claims.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Dict: Decoded token claims
        
        Raises:
            HTTPException: If token verification fails
        """
        return await self.validator.validate_token(token)
        
    async def close(self):
        """
        Close resources and connections.
        
        This method should be called when the KeycloakAuth instance is no longer needed
        to ensure proper resource cleanup.
        """
        try:
            # Close validator
            if hasattr(self, 'validator'):
                await self.validator.close()
                
            self.logger.info("KeycloakAuth resources closed")
        except Exception as e:
            self.logger.error(f"Error closing resources: {str(e)}")

    def get_rate_limiter(self):
        """
        Get the rate limiter instance if available.
        
        Returns:
            Optional: Rate limiter instance or None if not available
        """
        return getattr(self, 'rate_limiter', None)
        
    def reset_rate_limits(self, identifier: str = "*"):
        """
        Reset rate limits for an identifier or pattern.
        
        Args:
            identifier: Identifier to reset, or pattern to match (default: all)
            
        Returns:
            bool: Whether reset was successful
        """
        if not hasattr(self, 'rate_limiter'):
            self.logger.warning("Rate limiting not enabled, cannot reset limits")
            return False
            
        try:
            # Reset rate limits
            # This is a coroutine, so we need to run it in an event loop
            import asyncio
            asyncio.run(self.rate_limiter.reset(identifier))
            
            self.logger.info(f"Rate limits reset for {identifier}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to reset rate limits: {str(e)}")
            return False
