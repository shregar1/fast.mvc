"""Tests for security headers configuration DTO."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from dtos.configuration.security_headers import (
    SecurityHeadersDefaults,
    SecurityHeadersSettingsDTO,
)


class TestSecurityHeadersDefaults:
    """Tests for SecurityHeadersDefaults class."""

    def test_x_content_type_options(self):
        """Test X_CONTENT_TYPE_OPTIONS constant."""
        assert SecurityHeadersDefaults.X_CONTENT_TYPE_OPTIONS == "nosniff"

    def test_x_frame_options(self):
        """Test X_FRAME_OPTIONS constant."""
        assert SecurityHeadersDefaults.X_FRAME_OPTIONS == "DENY"

    def test_x_xss_protection(self):
        """Test X_XSS_PROTECTION constant."""
        assert SecurityHeadersDefaults.X_XSS_PROTECTION == "1; mode=block"

    def test_referrer_policy(self):
        """Test REFERRER_POLICY constant."""
        assert SecurityHeadersDefaults.REFERRER_POLICY == "strict-origin-when-cross-origin"

    def test_enable_hsts(self):
        """Test ENABLE_HSTS constant."""
        assert SecurityHeadersDefaults.ENABLE_HSTS is True

    def test_hsts_max_age(self):
        """Test HSTS_MAX_AGE constant."""
        assert SecurityHeadersDefaults.HSTS_MAX_AGE == 31_536_000

    def test_hsts_include_subdomains(self):
        """Test HSTS_INCLUDE_SUBDOMAINS constant."""
        assert SecurityHeadersDefaults.HSTS_INCLUDE_SUBDOMAINS is True

    def test_hsts_preload(self):
        """Test HSTS_PRELOAD constant."""
        assert SecurityHeadersDefaults.HSTS_PRELOAD is False

    def test_content_security_policy(self):
        """Test CONTENT_SECURITY_POLICY constant."""
        assert SecurityHeadersDefaults.CONTENT_SECURITY_POLICY is None

    def test_permissions_policy(self):
        """Test PERMISSIONS_POLICY constant."""
        assert SecurityHeadersDefaults.PERMISSIONS_POLICY is None

    def test_cross_origin_opener_policy(self):
        """Test CROSS_ORIGIN_OPENER_POLICY constant."""
        assert SecurityHeadersDefaults.CROSS_ORIGIN_OPENER_POLICY == "same-origin"

    def test_cross_origin_resource_policy(self):
        """Test CROSS_ORIGIN_RESOURCE_POLICY constant."""
        assert SecurityHeadersDefaults.CROSS_ORIGIN_RESOURCE_POLICY == "same-origin"

    def test_cross_origin_embedder_policy(self):
        """Test CROSS_ORIGIN_EMBEDDER_POLICY constant."""
        assert SecurityHeadersDefaults.CROSS_ORIGIN_EMBEDDER_POLICY is None

    def test_remove_server_header(self):
        """Test REMOVE_SERVER_HEADER constant."""
        assert SecurityHeadersDefaults.REMOVE_SERVER_HEADER is True

    def test_builtin_content_security_policy(self):
        """Test BUILTIN_CONTENT_SECURITY_POLICY constant."""
        assert "default-src" in SecurityHeadersDefaults.BUILTIN_CONTENT_SECURITY_POLICY


class TestSecurityHeadersSettingsDTO:
    """Tests for SecurityHeadersSettingsDTO."""

    def test_default_creation(self):
        """Test creating with default values."""
        dto = SecurityHeadersSettingsDTO()
        assert dto is not None

    def test_x_content_type_options_default(self):
        """Test x_content_type_options default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.x_content_type_options == "nosniff"

    def test_x_frame_options_default(self):
        """Test x_frame_options default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.x_frame_options == "DENY"

    def test_x_xss_protection_default(self):
        """Test x_xss_protection default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.x_xss_protection == "1; mode=block"

    def test_referrer_policy_default(self):
        """Test referrer_policy default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.referrer_policy == "strict-origin-when-cross-origin"

    def test_enable_hsts_default(self):
        """Test enable_hsts default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.enable_hsts is True

    def test_hsts_max_age_default(self):
        """Test hsts_max_age default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.hsts_max_age == 31_536_000

    def test_hsts_include_subdomains_default(self):
        """Test hsts_include_subdomains default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.hsts_include_subdomains is True

    def test_hsts_preload_default(self):
        """Test hsts_preload default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.hsts_preload is False

    def test_content_security_policy_default(self):
        """Test content_security_policy default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.content_security_policy is None

    def test_permissions_policy_default(self):
        """Test permissions_policy default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.permissions_policy is None

    def test_cross_origin_opener_policy_default(self):
        """Test cross_origin_opener_policy default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.cross_origin_opener_policy == "same-origin"

    def test_cross_origin_resource_policy_default(self):
        """Test cross_origin_resource_policy default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.cross_origin_resource_policy == "same-origin"

    def test_cross_origin_embedder_policy_default(self):
        """Test cross_origin_embedder_policy default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.cross_origin_embedder_policy is None

    def test_remove_server_header_default(self):
        """Test remove_server_header default value."""
        dto = SecurityHeadersSettingsDTO()
        assert dto.remove_server_header is True


class TestSecurityHeadersSettingsDTOCustomValues:
    """Tests for SecurityHeadersSettingsDTO with custom values."""

    def test_custom_x_content_type_options(self):
        """Test setting custom x_content_type_options."""
        dto = SecurityHeadersSettingsDTO(x_content_type_options="nosniff")
        assert dto.x_content_type_options == "nosniff"

    def test_custom_x_frame_options(self):
        """Test setting custom x_frame_options."""
        dto = SecurityHeadersSettingsDTO(x_frame_options="SAMEORIGIN")
        assert dto.x_frame_options == "SAMEORIGIN"

    def test_custom_enable_hsts(self):
        """Test setting custom enable_hsts."""
        dto = SecurityHeadersSettingsDTO(enable_hsts=False)
        assert dto.enable_hsts is False

    def test_custom_hsts_max_age(self):
        """Test setting custom hsts_max_age."""
        dto = SecurityHeadersSettingsDTO(hsts_max_age=86400)
        assert dto.hsts_max_age == 86400

    def test_custom_content_security_policy(self):
        """Test setting custom content_security_policy."""
        csp = "default-src 'self'"
        dto = SecurityHeadersSettingsDTO(content_security_policy=csp)
        assert dto.content_security_policy == csp


class TestSecurityHeadersSettingsDTOValidation:
    """Tests for SecurityHeadersSettingsDTO validation."""

    def test_hsts_max_age_negative(self):
        """Test hsts_max_age cannot be negative."""
        with pytest.raises(ValidationError):
            SecurityHeadersSettingsDTO(hsts_max_age=-1)

    def test_hsts_max_age_zero(self):
        """Test hsts_max_age can be zero."""
        dto = SecurityHeadersSettingsDTO(hsts_max_age=0)
        assert dto.hsts_max_age == 0


class TestSecurityHeadersSettingsDTOMiddlewareConfig:
    """Tests for to_middleware_config method."""

    def test_to_middleware_config(self):
        """Test to_middleware_config returns config."""
        dto = SecurityHeadersSettingsDTO()
        result = dto.to_middleware_config()
        assert result is not None
