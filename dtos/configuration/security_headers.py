"""HTTP security headers configuration DTO."""

from __future__ import annotations

from fastmiddleware import SecurityHeadersConfig  # pyright: ignore[reportMissingImports]
from pydantic import Field

from dtos.configuration.abstraction import IConfigurationDTO


class SecurityHeadersSettingsDTO(IConfigurationDTO):
    """Typed settings for ``SecurityHeadersMiddleware`` (CSP, HSTS, frame options, …).

    Values are typically populated from environment variables; see
    :func:`utilities.security_headers.load_security_headers_settings_from_env`.
    """

    x_content_type_options: str = Field(
        default="nosniff",
        description="``X-Content-Type-Options`` (MIME sniffing).",
    )
    x_frame_options: str = Field(
        default="DENY",
        description="``X-Frame-Options`` (e.g. DENY, SAMEORIGIN).",
    )
    x_xss_protection: str = Field(
        default="1; mode=block",
        description="Legacy ``X-XSS-Protection`` value.",
    )
    referrer_policy: str = Field(
        default="strict-origin-when-cross-origin",
        description="``Referrer-Policy`` value.",
    )
    enable_hsts: bool = Field(
        default=True,
        description="Enable HTTP Strict Transport Security.",
    )
    hsts_max_age: int = Field(
        default=31_536_000,
        ge=0,
        description="HSTS ``max-age`` in seconds (default one year).",
    )
    hsts_include_subdomains: bool = Field(
        default=True,
        description="Include ``includeSubDomains`` in HSTS.",
    )
    hsts_preload: bool = Field(
        default=False,
        description="Enable HSTS preload list submission semantics.",
    )
    content_security_policy: str | None = Field(
        default=None,
        description=(
            "Full ``Content-Security-Policy`` header value. "
            "When omitted at load time, the default in :mod:`utilities.security_headers` is used."
        ),
    )
    permissions_policy: str | None = Field(
        default=None,
        description="Optional ``Permissions-Policy`` header value.",
    )
    cross_origin_opener_policy: str | None = Field(
        default="same-origin",
        description="``Cross-Origin-Opener-Policy`` (COOP).",
    )
    cross_origin_resource_policy: str | None = Field(
        default="same-origin",
        description="``Cross-Origin-Resource-Policy`` (CORP).",
    )
    cross_origin_embedder_policy: str | None = Field(
        default=None,
        description="Optional ``Cross-Origin-Embedder-Policy`` (COEP).",
    )
    remove_server_header: bool = Field(
        default=True,
        description="Strip the ``Server`` header from responses.",
    )

    def to_middleware_config(self) -> SecurityHeadersConfig:
        """Build the fast-middleware :class:`~fastmiddleware.SecurityHeadersConfig` instance."""
        csp = self.content_security_policy
        return SecurityHeadersConfig(
            x_content_type_options=self.x_content_type_options,
            x_frame_options=self.x_frame_options,
            x_xss_protection=self.x_xss_protection,
            referrer_policy=self.referrer_policy,
            enable_hsts=self.enable_hsts,
            hsts_max_age=self.hsts_max_age,
            hsts_include_subdomains=self.hsts_include_subdomains,
            hsts_preload=self.hsts_preload,
            content_security_policy=csp,
            permissions_policy=self.permissions_policy,
            cross_origin_opener_policy=self.cross_origin_opener_policy,
            cross_origin_resource_policy=self.cross_origin_resource_policy,
            cross_origin_embedder_policy=self.cross_origin_embedder_policy,
            remove_server_header=self.remove_server_header,
        )
