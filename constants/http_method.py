"""Standard HTTP method names (verbs)."""

from typing import ClassVar


class HttpMethod:
    """Canonical HTTP method strings."""

    GET: ClassVar[str] = "GET"
    POST: ClassVar[str] = "POST"
    PUT: ClassVar[str] = "PUT"
    DELETE: ClassVar[str] = "DELETE"
    OPTIONS: ClassVar[str] = "OPTIONS"
    PATCH: ClassVar[str] = "PATCH"
