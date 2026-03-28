"""Security headers middleware configuration (env → DTO → ``SecurityHeadersConfig``)."""

from __future__ import annotations

import os

from fastmiddleware import SecurityHeadersConfig

from dtos.configuration import SecurityHeadersSettingsDTO

# Default CSP: self-hosted API + Swagger/ReDoc assets (jsdelivr, Google Fonts).
DEFAULT_SECURITY_CONTENT_SECURITY_POLICY: str = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
    "font-src 'self' data: https://fonts.gstatic.com; "
    "img-src 'self' data: https: blob:; "
    "connect-src 'self'"
)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in ("true", "1", "yes", "on")


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return int(raw)


def _env_str(name: str, default: str) -> str:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw


def _env_optional_str(name: str) -> str | None:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return None
    return raw


def load_security_headers_settings_from_env() -> SecurityHeadersSettingsDTO:
    """Load :class:`SecurityHeadersSettingsDTO` from ``SECURITY_*`` environment variables.

    All variables are optional; omitted values use the same defaults as the previous
    inline ``SecurityHeadersConfig`` in ``app.py``.

    Variables:
        ``SECURITY_X_CONTENT_TYPE_OPTIONS``, ``SECURITY_X_FRAME_OPTIONS``,
        ``SECURITY_X_XSS_PROTECTION``, ``SECURITY_REFERRER_POLICY``,
        ``SECURITY_ENABLE_HSTS``, ``SECURITY_HSTS_MAX_AGE``,
        ``SECURITY_HSTS_INCLUDE_SUBDOMAINS``, ``SECURITY_HSTS_PRELOAD``,
        ``SECURITY_CONTENT_SECURITY_POLICY`` (full CSP string; empty → built-in default),
        ``SECURITY_PERMISSIONS_POLICY``,
        ``SECURITY_CROSS_ORIGIN_OPENER_POLICY``, ``SECURITY_CROSS_ORIGIN_RESOURCE_POLICY``,
        ``SECURITY_CROSS_ORIGIN_EMBEDDER_POLICY``,
        ``SECURITY_REMOVE_SERVER_HEADER``.
    """
    csp = _env_optional_str("SECURITY_CONTENT_SECURITY_POLICY")
    if csp is None:
        csp = DEFAULT_SECURITY_CONTENT_SECURITY_POLICY

    coop = _env_optional_str("SECURITY_CROSS_ORIGIN_OPENER_POLICY")
    if coop is None:
        coop = "same-origin"

    corp = _env_optional_str("SECURITY_CROSS_ORIGIN_RESOURCE_POLICY")
    if corp is None:
        corp = "same-origin"

    return SecurityHeadersSettingsDTO(
        x_content_type_options=_env_str(
            "SECURITY_X_CONTENT_TYPE_OPTIONS", "nosniff"
        ),
        x_frame_options=_env_str("SECURITY_X_FRAME_OPTIONS", "DENY"),
        x_xss_protection=_env_str(
            "SECURITY_X_XSS_PROTECTION", "1; mode=block"
        ),
        referrer_policy=_env_str(
            "SECURITY_REFERRER_POLICY", "strict-origin-when-cross-origin"
        ),
        enable_hsts=_env_bool("SECURITY_ENABLE_HSTS", True),
        hsts_max_age=_env_int("SECURITY_HSTS_MAX_AGE", 31_536_000),
        hsts_include_subdomains=_env_bool("SECURITY_HSTS_INCLUDE_SUBDOMAINS", True),
        hsts_preload=_env_bool("SECURITY_HSTS_PRELOAD", False),
        content_security_policy=csp,
        permissions_policy=_env_optional_str("SECURITY_PERMISSIONS_POLICY"),
        cross_origin_opener_policy=coop,
        cross_origin_resource_policy=corp,
        cross_origin_embedder_policy=_env_optional_str(
            "SECURITY_CROSS_ORIGIN_EMBEDDER_POLICY"
        ),
        remove_server_header=_env_bool("SECURITY_REMOVE_SERVER_HEADER", True),
    )


def get_security_headers_middleware_config() -> SecurityHeadersConfig:
    """Return a :class:`SecurityHeadersConfig` for ``SecurityHeadersMiddleware``."""
    return load_security_headers_settings_from_env().to_middleware_config()
