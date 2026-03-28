"""Abstract base for environment-backed configuration DTOs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from abstractions.dto import IDTO


class IConfigurationDTO(BaseModel, IDTO):
    """Abstract base for all configuration DTOs under :mod:`dtos.configuration`.

    Inherits :class:`abstractions.dto.IDTO` and :class:`pydantic.BaseModel`.

    Subclasses model typed settings loaded from environment variables, files, or
    defaults, and typically expose helpers (e.g. ``to_middleware_config``) to
    bridge into runtime middleware or services.

    Shared rules:

    - Unknown fields are rejected (``extra="forbid"``).
    - String fields are not stripped by default (``str_strip_whitespace=False``)
      so values like CSP and header policies keep exact syntax.

    Do not instantiate this class directly; use concrete DTOs such as
    :class:`~dtos.configuration.cors.CorsSettingsDTO` or
    :class:`~dtos.configuration.security_headers.SecurityHeadersSettingsDTO`.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=False)
