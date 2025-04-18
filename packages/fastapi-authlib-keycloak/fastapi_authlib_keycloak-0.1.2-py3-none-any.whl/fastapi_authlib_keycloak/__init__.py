#!/usr/bin/env python3
"""
FastAPI-Authlib-Keycloak
------------------------

A comprehensive integration between FastAPI, Authlib, and Keycloak
for seamless authentication and authorization.

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

:copyright: (c) 2025 Harsha
:license: MIT
"""

__version__ = "0.1.2"  # Updated version number

# Export main class
from fastapi_authlib_keycloak.keycloak_auth import KeycloakAuth
from fastapi_authlib_keycloak.models import User

__all__ = ["KeycloakAuth", "User"]
