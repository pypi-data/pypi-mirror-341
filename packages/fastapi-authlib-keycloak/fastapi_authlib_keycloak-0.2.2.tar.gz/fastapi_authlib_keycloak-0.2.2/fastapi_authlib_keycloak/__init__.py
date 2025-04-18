#!/usr/bin/env python3
"""
FastAPI-Authlib-Keycloak
------------------------

A comprehensive integration between FastAPI, Authlib, and Keycloak
for seamless authentication and authorization with enhanced features
including metrics collection, debugging utilities, and rate limiting.

This module provides a simple interface for adding Keycloak authentication
to FastAPI applications with enhanced Swagger UI integration.

Basic Usage:
```python
from fastapi import FastAPI, Depends
from fastapi_authlib_keycloak import KeycloakAuth

app = FastAPI()

# Initialize Keycloak Auth
auth = KeycloakAuth(
    app,
    keycloak_url="https://keycloak.example.com/auth",
    keycloak_realm="your-realm",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Use auth dependencies in your routes
@app.get("/protected")
async def protected_route(user = Depends(auth.get_current_user)):
    return {"message": f"Hello, {user.username}!"}

# For role-based access control
@app.get("/admin-only")
async def admin_route(user = Depends(auth.require_roles(["admin"]))):
    return {"message": "Admin access granted"}
```

Enhanced Features:
- Enhanced JWT validation with JWKS caching and rotation
- Metrics collection for monitoring and observability
- Debugging utilities for development
- Rate limiting for authentication endpoints

:copyright: (c) 2025 Harsha
:license: MIT
"""

__version__ = "0.2.2"  # Updated with improved CORS origins handling

# Export main classes
from fastapi_authlib_keycloak.keycloak_auth import KeycloakAuth
from fastapi_authlib_keycloak.models import User

# Export optional enhanced validator
try:
    from fastapi_authlib_keycloak.auth.enhanced_validator import (
        create_enhanced_validator,
        TokenValidationMethod
    )
except ImportError:
    pass

# Export optional metrics module
try:
    from fastapi_authlib_keycloak.utils.metrics import (
        configure_metrics,
        MetricsBackend
    )
except ImportError:
    pass

# Export optional rate limiting
try:
    from fastapi_authlib_keycloak.utils.rate_limit import (
        create_rate_limiter,
        RateLimitStrategy,
        RateLimitScope
    )
except ImportError:
    pass

__all__ = [
    "KeycloakAuth", 
    "User",
    # Enhanced validator (optional)
    "create_enhanced_validator",
    "TokenValidationMethod",
    # Metrics (optional)
    "configure_metrics",
    "MetricsBackend",
    # Rate limiting (optional)
    "create_rate_limiter",
    "RateLimitStrategy",
    "RateLimitScope"
]
