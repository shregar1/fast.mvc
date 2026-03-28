"""CORS middleware configuration (env → DTO → ``CORSMiddleware`` keyword args)."""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any

from constants.cors import CorsDefaults
from dtos.configuration import CorsSettingsDTO


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in ("true", "1", "yes", "on")


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or str(raw).strip() == "":
        return default
    return int(raw)


def _split_csv(name: str, default: Sequence[str]) -> list[str]:
    raw = os.getenv(name)
    if raw is None or str(raw).strip() == "":
        return list(default)
    parts = [p.strip() for p in str(raw).split(",") if p.strip()]
    return parts if parts else list(default)


def _parse_allow_origins() -> list[str]:
    """Comma-separated origins; ``CORS_ORIGINS`` wins, else ``ALLOWED_ORIGINS`` (Docker)."""
    raw = os.getenv("CORS_ORIGINS") or os.getenv("ALLOWED_ORIGINS")
    if raw is None or str(raw).strip() == "":
        return ["*"]
    parts = [p.strip() for p in str(raw).split(",") if p.strip()]
    return parts if parts else ["*"]


def _parse_allow_headers() -> list[str]:
    raw = os.getenv("CORS_ALLOW_HEADERS")
    if raw is None or str(raw).strip() == "":
        return ["*"]
    s = str(raw).strip()
    if s == "*":
        return ["*"]
    return [p.strip() for p in s.split(",") if p.strip()]


def load_cors_settings_from_env() -> CorsSettingsDTO:
    """Load :class:`CorsSettingsDTO` from environment.

    Variables (all optional):

    - ``CORS_ORIGINS`` — comma-separated allowed origins; if unset, ``ALLOWED_ORIGINS``
      is used (Compose); if both empty, ``["*"]`` (permissive dev default).
    - ``CORS_ALLOW_CREDENTIALS`` — ``true`` / ``false`` (default ``true``).
    - ``CORS_ALLOW_METHODS`` — comma-separated verbs (default GET,POST,…).
    - ``CORS_ALLOW_HEADERS`` — ``*`` or comma-separated names (default ``*``).
    - ``CORS_EXPOSE_HEADERS`` — comma-separated (default includes transaction/reference URNs).
    - ``CORS_ALLOW_ORIGIN_REGEX`` — optional regex string.
    - ``CORS_MAX_AGE`` — preflight cache seconds (default ``600``).
    """
    allow_origin_regex = os.getenv("CORS_ALLOW_ORIGIN_REGEX")
    if allow_origin_regex is not None and allow_origin_regex.strip() == "":
        allow_origin_regex = None

    return CorsSettingsDTO(
        allow_origins=_parse_allow_origins(),
        allow_credentials=_env_bool("CORS_ALLOW_CREDENTIALS", True),
        allow_methods=_split_csv("CORS_ALLOW_METHODS", CorsDefaults.ALLOW_METHODS),
        allow_headers=_parse_allow_headers(),
        expose_headers=_split_csv("CORS_EXPOSE_HEADERS", CorsDefaults.EXPOSE_HEADERS),
        allow_origin_regex=allow_origin_regex,
        max_age=_env_int("CORS_MAX_AGE", 600),
    )


def get_cors_middleware_kwargs() -> dict[str, Any]:
    """Return keyword arguments for ``app.add_middleware(CORSMiddleware, **kwargs)``."""
    return load_cors_settings_from_env().to_middleware_kwargs()
