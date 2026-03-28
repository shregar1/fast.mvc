"""Middleware package.

Exports app-specific JWT authentication wired to ``fast_middleware``.

Generic HTTP middleware (security headers, body limits, CORS, timing, etc.) lives in
the ``fast-middleware`` distribution (import ``fast_middleware`` or ``fastmiddleware``
depending on your stack). This package only provides :class:`AuthenticationMiddleware`.

Use::

    from middlewares import AuthenticationMiddleware
"""

from .authentication import AuthenticationMiddleware
from .docs_auth import (
    DocsBasicAuthMiddleware,
    docs_auth_configured,
    docs_logging_exclude_paths,
    normalized_openapi_url,
)

__all__ = [
    "AuthenticationMiddleware",
    "DocsBasicAuthMiddleware",
    "docs_auth_configured",
    "docs_logging_exclude_paths",
    "normalized_openapi_url",
]
