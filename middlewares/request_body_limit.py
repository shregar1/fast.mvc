"""
Request body size limit middleware.

Rejects requests with Content-Length over a configured maximum to avoid
memory exhaustion and abuse. Only checks Content-Length; chunked requests
without Content-Length are not rejected here (server/ASGI may enforce limits).
"""

import os
from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from start_utils import logger

# Default 10 MiB; override with REQUEST_BODY_MAX_BYTES
DEFAULT_MAX_BYTES = 10 * 1024 * 1024


def _get_max_bytes() -> int:
    val = os.getenv("REQUEST_BODY_MAX_BYTES")
    if val is None:
        return DEFAULT_MAX_BYTES
    try:
        return int(val)
    except (TypeError, ValueError):
        logger.warning(
            f"Invalid REQUEST_BODY_MAX_BYTES={val!r}, using default {DEFAULT_MAX_BYTES}"
        )
        return DEFAULT_MAX_BYTES


class RequestBodyLimitMiddleware(BaseHTTPMiddleware):
    """Reject requests whose Content-Length exceeds the configured maximum."""

    def __init__(self, app, max_bytes: int | None = None):
        super().__init__(app)
        self._max_bytes = max_bytes if max_bytes is not None else _get_max_bytes()

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                length = int(content_length)
                if length > self._max_bytes:
                    urn = getattr(request.state, "urn", None) or ""
                    logger.warning(
                        f"Request body too large: {length} > {self._max_bytes}",
                        urn=urn,
                    )
                    return JSONResponse(
                        status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                        content={
                            "transactionUrn": urn,
                            "status": "FAILED",
                            "responseMessage": "Request body too large.",
                            "responseKey": "error_request_body_too_large",
                            "data": {},
                        },
                    )
            except ValueError:
                pass  # Invalid Content-Length; let downstream validation handle it
        return await call_next(request)
