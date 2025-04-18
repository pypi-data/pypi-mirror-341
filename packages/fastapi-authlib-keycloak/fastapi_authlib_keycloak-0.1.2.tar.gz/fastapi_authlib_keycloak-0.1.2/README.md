# FastAPI-Authlib-Keycloak

[![PyPI version](https://badge.fury.io/py/fastapi-authlib-keycloak.svg)](https://badge.fury.io/py/fastapi-authlib-keycloak)
[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-authlib-keycloak.svg)](https://pypi.org/project/fastapi-authlib-keycloak/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive integration between FastAPI, Authlib, and Keycloak for seamless authentication and authorization with an enhanced Swagger UI experience.

## Features

- 🔒 **Complete Keycloak Authentication** - OAuth2/OpenID Connect integration with minimal setup
- 🚀 **Enhanced Swagger UI** - Custom UI with authentication controls and token management
- 🔐 **Role-Based Access Control** - Simple dependencies for role-based endpoints
- 📄 **SSL Certificate Management** - Utilities for proper SSL verification
- 🔧 **Highly Configurable** - Customizable with sensible defaults
- 🧩 **Modular Design** - Use only what you need

## Installation

```bash
pip install fastapi-authlib-keycloak
```

## Quick Start

```python
from fastapi import FastAPI, Depends
from fastapi_authlib_keycloak import KeycloakAuth, User

app = FastAPI()

# Initialize Keycloak authentication
auth = KeycloakAuth(
    app,
    keycloak_url="https://your-keycloak-server.com/auth", 
    keycloak_realm="your-realm",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Public endpoint
@app.get("/public")
async def public_route():
    return {"message": "This is a public endpoint"}

# Protected endpoint requiring authentication
@app.get("/protected")
async def protected_route(user: User = Depends(auth.get_current_user)):
    return {
        "message": f"Hello, {user.username}!",
        "email": user.email,
        "roles": user.roles
    }

# Role-based endpoint
@app.get("/admin-only")
async def admin_route(user: User = Depends(auth.require_roles(["admin"]))):
    return {"message": "Admin access granted"}
```

## Documentation

Visit our [documentation](https://c0mpiler.github.io/fastapi-authlib-keycloak) for detailed guides, API reference, and examples.

### Features in Detail

#### Enhanced Swagger UI Integration

The package provides a custom Swagger UI that seamlessly integrates with Keycloak authentication. It includes:

- Login/logout functionality directly in the UI
- Token management and inspection
- Automatic token refresh handling
- Improved styling based on IBM Carbon Design System

#### Authentication Flow Support

- Authorization Code Flow
- Password Grant Flow
- Client Credentials Flow
- Support for refresh tokens

#### Role-Based Access Control

Simple dependency functions for requiring specific roles:

```python
@app.get("/admin-only")
async def admin_route(user = Depends(auth.require_roles(["admin"]))):
    return {"message": "Admin access granted"}

@app.get("/multiple-roles")
async def multi_role_route(user = Depends(auth.require_roles(["editor", "reviewer"]))):
    return {"message": "Access granted for editor or reviewer"}
```

#### SSL Certificate Verification

Utilities for proper SSL certificate verification with Keycloak:

- Automatic certificate installation in certifi bundle
- Environment variable configuration for proper verification
- Support for custom SSL certificates

## Configuration Options

The `KeycloakAuth` class accepts the following parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| app | FastAPI | FastAPI application instance |
| keycloak_url | str | URL of the Keycloak server |
| keycloak_realm | str | Keycloak realm name |
| client_id | str | Client ID for the UI client |
| client_secret | str | Client secret for the UI client |
| api_base_url | Optional[str] | Base URL for the API |
| api_client_id | Optional[str] | Client ID for the API client |
| api_client_secret | Optional[str] | Client secret for the API client |
| session_secret | Optional[str] | Secret key for session encryption |
| session_max_age | int | Maximum session age in seconds |
| session_https_only | bool | Whether session cookies should be HTTPS only |
| session_same_site | str | Same-site policy for cookies (lax, strict, none) |
| cors_origins | List[str] | List of allowed CORS origins |
| cors_credentials | bool | Whether to allow credentials in CORS |
| ssl_enabled | bool | Whether to enable SSL certificate verification |
| ssl_cert_file | Optional[str] | Path to SSL certificate file |
| ssl_key_file | Optional[str] | Path to SSL key file |
| custom_swagger_title | Optional[str] | Custom title for Swagger UI |
| custom_swagger_css | Optional[str] | Path to custom CSS file for Swagger UI |
| load_from_env | bool | Whether to load configuration from environment variables |

## Environment Variables

All configuration options can be set through environment variables:

```
KEYCLOAK_URL=https://your-keycloak-server.com/auth
KEYCLOAK_REALM=your-realm
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
API_CLIENT_ID=your-api-client-id
API_CLIENT_SECRET=your-api-client-secret
API_BASE_URL=https://your-api.com
SESSION_SECRET=your-session-secret
SESSION_MAX_AGE=3600
SESSION_HTTPS_ONLY=true
SESSION_SAME_SITE=lax
CORS_ORIGINS=https://domain1.com,https://domain2.com
CORS_CREDENTIALS=true
SSL_ENABLED=true
SSL_CERT_FILE=/path/to/cert.pem
SSL_KEY_FILE=/path/to/key.pem
```

## Examples

### Verify Tokens Manually

```python
# Manually verify a token
@app.post("/verify-token")
async def verify_token(token: str):
    try:
        claims = await auth.verify_token(token)
        return {
            "valid": True,
            "claims": claims
        }
    except HTTPException as e:
        return {
            "valid": False,
            "error": e.detail
        }
```

### User Information

```python
# Get detailed user information
@app.get("/me")
async def get_user_info(user: User = Depends(auth.get_current_user)):
    return {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "roles": user.roles,
        "is_admin": user.has_role("admin")
    }
```

## Advanced Usage

### Custom Swagger UI Styling

The package uses a default CSS based on IBM Carbon Design System, but you can provide your own CSS:

```python
auth = KeycloakAuth(
    app,
    keycloak_url="https://your-keycloak-server.com/auth",
    keycloak_realm="your-realm",
    client_id="your-client-id",
    client_secret="your-client-secret",
    custom_swagger_css="/path/to/your/custom.css"
)
```

### Working with SSL Certificates

If your Keycloak instance uses a custom SSL certificate:

```python
auth = KeycloakAuth(
    app,
    keycloak_url="https://your-keycloak-server.com/auth",
    keycloak_realm="your-realm",
    client_id="your-client-id",
    client_secret="your-client-secret",
    ssl_enabled=True,
    ssl_cert_file="/path/to/your/cert.pem"
)
```

## Contributing

Contributions are welcome! See our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing framework for building APIs
- [Authlib](https://authlib.org/) - Robust OAuth2/OpenID Connect implementation
- [Keycloak](https://www.keycloak.org/) - Powerful identity and access management
- [IBM Carbon Design System](https://carbondesignsystem.com/) - Design inspiration for the Swagger UI

## Author

Harsha ([@c0mpiler](https://github.com/c0mpiler))
