"""HTTP Basic authentication for OpenAPI UI and schema (developer-only surfaces).

When ``DOCS_USERNAME`` and ``DOCS_PASSWORD`` are both set in the environment,
all Swagger/ReDoc/OpenAPI routes require valid ``Authorization: Basic …`` credentials,
including subpaths (e.g. ``/docs/oauth2-redirect``) and any configured OpenAPI URL.
If either variable is unset or empty, these routes stay open (typical local development).

Environment:

* ``OPENAPI_URL`` — Must match :class:`fastapi.FastAPI` ``openapi_url`` (default ``/openapi.json``).
* ``DOCS_EXTRA_PROTECTED_PATHS`` — Comma-separated extra paths to require the same auth (legacy aliases).
"""

from __future__ import annotations

import base64
import binascii
import os
import secrets
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response


def normalized_openapi_url() -> str:
    """Return the OpenAPI JSON path; keep in sync with ``FastAPI(openapi_url=...)``."""
    raw = os.environ.get("OPENAPI_URL", "/openapi.json").strip() or "/openapi.json"
    if not raw.startswith("/"):
        raw = "/" + raw
    return raw


def resolve_openapi_url_paths() -> frozenset[str]:
    """All URL paths that expose the OpenAPI schema (for auth + logging excludes)."""
    out: set[str] = {normalized_openapi_url()}
    extra = os.environ.get("DOCS_EXTRA_PROTECTED_PATHS", "")
    for part in extra.split(","):
        p = part.strip()
        if not p:
            continue
        if not p.startswith("/"):
            p = "/" + p
        out.add(p)
    return frozenset(out)


def docs_logging_exclude_paths() -> frozenset[str]:
    """Paths to skip in request logging (doc UI + schema URLs)."""
    base = frozenset(
        {
            "/",
            "/health",
            "/docs",
            "/redoc",
            *resolve_openapi_url_paths(),
        }
    )
    return base


def docs_auth_configured() -> bool:
    """Return True when Basic auth should be enforced for documentation routes."""
    u = os.environ.get("DOCS_USERNAME", "").strip()
    p = os.environ.get("DOCS_PASSWORD", "").strip()
    return bool(u and p)


def _parse_basic_authorization(header: str | None) -> tuple[str, str] | None:
    if not header or not header.startswith("Basic "):
        return None
    try:
        raw = base64.b64decode(header[6:].strip())
        decoded = raw.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None
    if ":" not in decoded:
        return None
    username, _, password = decoded.partition(":")
    return username, password


def _str_match_constant_time(got: str, expected: str) -> bool:
    if len(got) != len(expected):
        return False
    return secrets.compare_digest(got.encode("utf-8"), expected.encode("utf-8"))


def _unauthorized() -> PlainTextResponse:
    return PlainTextResponse(
        "Authentication required for API documentation.",
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="FastMVC API Documentation"'},
    )


def path_requires_docs_auth(path: str) -> bool:
    """Return True if ``path`` is a documentation or OpenAPI schema surface."""
    np = path.rstrip("/") or "/"
    for o in resolve_openapi_url_paths():
        if np == (o.rstrip("/") or "/"):
            return True
    pl = path.lower()
    if pl == "/docs" or pl.startswith("/docs/"):
        return True
    if pl == "/redoc" or pl.startswith("/redoc/"):
        return True
    return False


class DocsBasicAuthMiddleware(BaseHTTPMiddleware):
    """Require HTTP Basic auth for OpenAPI-related routes when credentials are configured."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if not docs_auth_configured():
            return await call_next(request)
        # CORS preflight must reach CORSMiddleware without a 401 challenge.
        if request.method == "OPTIONS":
            return await call_next(request)
        if not path_requires_docs_auth(request.url.path):
            return await call_next(request)

        expected_user = os.environ["DOCS_USERNAME"].strip()
        expected_pass = os.environ["DOCS_PASSWORD"].strip()
        parsed = _parse_basic_authorization(request.headers.get("Authorization"))
        if parsed is None:
            return _unauthorized()
        username, password = parsed
        if not (
            _str_match_constant_time(username, expected_user)
            and _str_match_constant_time(password, expected_pass)
        ):
            return _unauthorized()
        return await call_next(request)
