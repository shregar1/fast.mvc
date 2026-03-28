"""Default CORS middleware lists (aligned with :class:`dtos.configuration.CorsSettingsDTO`)."""

from typing import ClassVar, Final

from constants.http_header import HttpHeader
from constants.http_method import HttpMethod


class CorsDefaults:
    """Default CORS allow-methods and expose-headers lists (env overrides in :mod:`utilities.cors`)."""

    ALLOW_METHODS: ClassVar[tuple[str, ...]] = (
        HttpMethod.GET,
        HttpMethod.POST,
        HttpMethod.PUT,
        HttpMethod.DELETE,
        HttpMethod.OPTIONS,
        HttpMethod.PATCH,
    )
    EXPOSE_HEADERS: ClassVar[tuple[str, ...]] = (
        HttpHeader.X_REQUEST_ID,
        HttpHeader.X_PROCESS_TIME,
        HttpHeader.X_TRANSACTION_URN,
        HttpHeader.X_REFERENCE_URN,
    )


    CORS_DEFAULT_ALLOW_METHODS: Final[tuple[str, ...]] = ALLOW_METHODS
    CORS_DEFAULT_EXPOSE_HEADERS: Final[tuple[str, ...]] = EXPOSE_HEADERS
