# JWT Auth Validator

A lightweight Python package for validating JWT tokens and checking user permissions using public keys fetched from a JWKS endpoint.

## Overview

This package provides a decorator-based approach to validate JWT tokens signed with RS256 and enforce permission-based access control for your views. It fetches public keys dynamically from your centralized authentication service via JWKS (JSON Web Key Set) and caches them internally for performance.

It is designed to be used in projects built with Django (REST or GraphQL), and keeps your authentication logic decoupled, reusable, and secure.

## Installation

Install the package using pip:

```bash
pip install jwt-auth-validator
```

## Configuration

Before using the decorators, configure the domain of your authentication service once at the beginning of your app (e.g., in `apps.py` or `urls.py`):

```python
from jwt_auth_validator import configure

# Set your base domain (the package handles the rest of the path internally)
configure(domain="https://your-user-service.com")
```

> Note: Only the base domain is required. The package automatically resolves the internal JWKS URL path. The full endpoint remains hidden from end users.

---

## Usage

### With Django REST Framework (DRF)

In your `views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from jwt_auth_validator.decorators import require_permission

class MyProtectedView(APIView):

    @require_permission("view_reports")
    def get(self, request):
        return Response({"message": "You have access!"})
```

### With GraphQL (Graphene-Django)

In your `schema.py`:

```python
import graphene
from jwt_auth_validator.decorators import require_permission

class Query(graphene.ObjectType):
    hello = graphene.String()

    @require_permission("read_hello")
    def resolve_hello(self, info):
        return "Hello, authenticated user!"
```

---

## How It Works

- The `require_permission` decorator extracts the JWT from the `Authorization` header.
- It decodes the token using the RS256 algorithm and verifies the signature using the public key obtained from your authentication service.
- The key is identified by the `kid` field in the JWT header and fetched from the JWKS endpoint.
- The key is cached in-memory for better performance.
- Finally, the decorator checks if the user has the required permission in the token payload.

---

## Token Payload Example

The JWT payload is expected to include a `permissions` array:

```json
{
  "sub": "1234567890",
  "permissions": ["read_hello", "edit_profile"],
  "exp": 1712345678,
  "iat": 1712341234,
  "kid": "abc123"
}
```

---

## Error Handling

- Missing or malformed token → 401 Unauthorized
- Token signature invalid or expired → 401 Unauthorized
- Permission not found in payload → 403 Forbidden

---

## License

MIT © Your Name

