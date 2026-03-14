"""
Middleware package.

Exports app-specific and shared middleware for the FastMVC application.
Use::

    from middlewares import (
        AuthenticationMiddleware,
        RequestBodyLimitMiddleware,
        SecurityHeadersConfig,
        SecurityHeadersMiddleware,
    )
"""

from middlewares.authetication import AuthenticationMiddleware
from middlewares.request_body_limit import (
    DEFAULT_MAX_BYTES,
    RequestBodyLimitMiddleware,
)
from middlewares.security_headers import (
    SecurityHeadersConfig,
    SecurityHeadersMiddleware,
)

__all__ = [
    "AuthenticationMiddleware",
    "DEFAULT_MAX_BYTES",
    "RequestBodyLimitMiddleware",
    "SecurityHeadersConfig",
    "SecurityHeadersMiddleware",
]
