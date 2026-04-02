"""Tests for security headers constants."""

from __future__ import annotations

import pytest

from constants.security_headers import SecurityHeadersEnvVar, SecurityHeadersConstants


class TestSecurityHeadersEnvVar:
    """Tests for SecurityHeadersEnvVar class."""

    def test_x_content_type_options_env_var(self):
        """Test SECURITY_X_CONTENT_TYPE_OPTIONS environment variable name."""
        assert SecurityHeadersEnvVar.X_CONTENT_TYPE_OPTIONS == "SECURITY_X_CONTENT_TYPE_OPTIONS"

    def test_x_frame_options_env_var(self):
        """Test SECURITY_X_FRAME_OPTIONS environment variable name."""
        assert SecurityHeadersEnvVar.X_FRAME_OPTIONS == "SECURITY_X_FRAME_OPTIONS"

    def test_x_xss_protection_env_var(self):
        """Test SECURITY_X_XSS_PROTECTION environment variable name."""
        assert SecurityHeadersEnvVar.X_XSS_PROTECTION == "SECURITY_X_XSS_PROTECTION"

    def test_referrer_policy_env_var(self):
        """Test SECURITY_REFERRER_POLICY environment variable name."""
        assert SecurityHeadersEnvVar.REFERRER_POLICY == "SECURITY_REFERRER_POLICY"

    def test_enable_hsts_env_var(self):
        """Test SECURITY_ENABLE_HSTS environment variable name."""
        assert SecurityHeadersEnvVar.ENABLE_HSTS == "SECURITY_ENABLE_HSTS"

    def test_hsts_max_age_env_var(self):
        """Test SECURITY_HSTS_MAX_AGE environment variable name."""
        assert SecurityHeadersEnvVar.HSTS_MAX_AGE == "SECURITY_HSTS_MAX_AGE"

    def test_hsts_include_subdomains_env_var(self):
        """Test SECURITY_HSTS_INCLUDE_SUBDOMAINS environment variable name."""
        assert SecurityHeadersEnvVar.HSTS_INCLUDE_SUBDOMAINS == "SECURITY_HSTS_INCLUDE_SUBDOMAINS"

    def test_hsts_preload_env_var(self):
        """Test SECURITY_HSTS_PRELOAD environment variable name."""
        assert SecurityHeadersEnvVar.HSTS_PRELOAD == "SECURITY_HSTS_PRELOAD"

    def test_content_security_policy_env_var(self):
        """Test SECURITY_CONTENT_SECURITY_POLICY environment variable name."""
        assert SecurityHeadersEnvVar.CONTENT_SECURITY_POLICY == "SECURITY_CONTENT_SECURITY_POLICY"

    def test_permissions_policy_env_var(self):
        """Test SECURITY_PERMISSIONS_POLICY environment variable name."""
        assert SecurityHeadersEnvVar.PERMISSIONS_POLICY == "SECURITY_PERMISSIONS_POLICY"

    def test_cross_origin_opener_policy_env_var(self):
        """Test SECURITY_CROSS_ORIGIN_OPENER_POLICY environment variable name."""
        assert SecurityHeadersEnvVar.CROSS_ORIGIN_OPENER_POLICY == "SECURITY_CROSS_ORIGIN_OPENER_POLICY"

    def test_cross_origin_resource_policy_env_var(self):
        """Test SECURITY_CROSS_ORIGIN_RESOURCE_POLICY environment variable name."""
        assert SecurityHeadersEnvVar.CROSS_ORIGIN_RESOURCE_POLICY == "SECURITY_CROSS_ORIGIN_RESOURCE_POLICY"

    def test_cross_origin_embedder_policy_env_var(self):
        """Test SECURITY_CROSS_ORIGIN_EMBEDDER_POLICY environment variable name."""
        assert SecurityHeadersEnvVar.CROSS_ORIGIN_EMBEDDER_POLICY == "SECURITY_CROSS_ORIGIN_EMBEDDER_POLICY"

    def test_remove_server_header_env_var(self):
        """Test SECURITY_REMOVE_SERVER_HEADER environment variable name."""
        assert SecurityHeadersEnvVar.REMOVE_SERVER_HEADER == "SECURITY_REMOVE_SERVER_HEADER"


class TestSecurityHeadersConstants:
    """Tests for SecurityHeadersConstants class."""

    def test_default_enable_hsts(self):
        """Test DEFAULT_ENABLE_HSTS constant."""
        assert SecurityHeadersConstants.DEFAULT_ENABLE_HSTS is True

    def test_default_hsts_max_age_seconds(self):
        """Test DEFAULT_HSTS_MAX_AGE_SECONDS constant."""
        assert SecurityHeadersConstants.DEFAULT_HSTS_MAX_AGE_SECONDS == 31_536_000

    def test_default_hsts_include_subdomains(self):
        """Test DEFAULT_HSTS_INCLUDE_SUBDOMAINS constant."""
        assert SecurityHeadersConstants.DEFAULT_HSTS_INCLUDE_SUBDOMAINS is True

    def test_default_hsts_preload(self):
        """Test DEFAULT_HSTS_PRELOAD constant."""
        assert SecurityHeadersConstants.DEFAULT_HSTS_PRELOAD is False

    def test_default_remove_server_header(self):
        """Test DEFAULT_REMOVE_SERVER_HEADER constant."""
        assert SecurityHeadersConstants.DEFAULT_REMOVE_SERVER_HEADER is True

    def test_content_security_policy(self):
        """Test CONTENT_SECURITY_POLICY constant."""
        assert "default-src" in SecurityHeadersConstants.CONTENT_SECURITY_POLICY
        assert "script-src" in SecurityHeadersConstants.CONTENT_SECURITY_POLICY

    def test_content_security_policy_contains_self(self):
        """Test CSP contains 'self'."""
        assert "'self'" in SecurityHeadersConstants.CONTENT_SECURITY_POLICY

    def test_cross_origin_opener_policy(self):
        """Test CROSS_ORIGIN_OPENER_POLICY constant."""
        assert SecurityHeadersConstants.CROSS_ORIGIN_OPENER_POLICY == "same-origin"

    def test_cross_origin_resource_policy(self):
        """Test CROSS_ORIGIN_RESOURCE_POLICY constant."""
        assert SecurityHeadersConstants.CROSS_ORIGIN_RESOURCE_POLICY == "same-origin"

    def test_x_content_type_options(self):
        """Test X_CONTENT_TYPE_OPTIONS constant."""
        assert SecurityHeadersConstants.X_CONTENT_TYPE_OPTIONS == "nosniff"

    def test_x_frame_options(self):
        """Test X_FRAME_OPTIONS constant."""
        assert SecurityHeadersConstants.X_FRAME_OPTIONS == "DENY"

    def test_x_xss_protection(self):
        """Test X_XSS_PROTECTION constant."""
        assert SecurityHeadersConstants.X_XSS_PROTECTION == "1; mode=block"

    def test_referrer_policy(self):
        """Test REFERRER_POLICY constant."""
        assert SecurityHeadersConstants.REFERRER_POLICY == "strict-origin-when-cross-origin"


class TestSecurityHeadersConstantsTypes:
    """Tests for security headers constant types."""

    def test_default_enable_hsts_is_bool(self):
        """Test DEFAULT_ENABLE_HSTS is a bool."""
        assert isinstance(SecurityHeadersConstants.DEFAULT_ENABLE_HSTS, bool)

    def test_default_hsts_max_age_seconds_is_int(self):
        """Test DEFAULT_HSTS_MAX_AGE_SECONDS is an int."""
        assert isinstance(SecurityHeadersConstants.DEFAULT_HSTS_MAX_AGE_SECONDS, int)

    def test_default_hsts_include_subdomains_is_bool(self):
        """Test DEFAULT_HSTS_INCLUDE_SUBDOMAINS is a bool."""
        assert isinstance(SecurityHeadersConstants.DEFAULT_HSTS_INCLUDE_SUBDOMAINS, bool)

    def test_default_hsts_preload_is_bool(self):
        """Test DEFAULT_HSTS_PRELOAD is a bool."""
        assert isinstance(SecurityHeadersConstants.DEFAULT_HSTS_PRELOAD, bool)

    def test_default_remove_server_header_is_bool(self):
        """Test DEFAULT_REMOVE_SERVER_HEADER is a bool."""
        assert isinstance(SecurityHeadersConstants.DEFAULT_REMOVE_SERVER_HEADER, bool)

    def test_content_security_policy_is_str(self):
        """Test CONTENT_SECURITY_POLICY is a string."""
        assert isinstance(SecurityHeadersConstants.CONTENT_SECURITY_POLICY, str)

    def test_cross_origin_opener_policy_is_str(self):
        """Test CROSS_ORIGIN_OPENER_POLICY is a string."""
        assert isinstance(SecurityHeadersConstants.CROSS_ORIGIN_OPENER_POLICY, str)

    def test_cross_origin_resource_policy_is_str(self):
        """Test CROSS_ORIGIN_RESOURCE_POLICY is a string."""
        assert isinstance(SecurityHeadersConstants.CROSS_ORIGIN_RESOURCE_POLICY, str)

    def test_x_content_type_options_is_str(self):
        """Test X_CONTENT_TYPE_OPTIONS is a string."""
        assert isinstance(SecurityHeadersConstants.X_CONTENT_TYPE_OPTIONS, str)

    def test_x_frame_options_is_str(self):
        """Test X_FRAME_OPTIONS is a string."""
        assert isinstance(SecurityHeadersConstants.X_FRAME_OPTIONS, str)

    def test_x_xss_protection_is_str(self):
        """Test X_XSS_PROTECTION is a string."""
        assert isinstance(SecurityHeadersConstants.X_XSS_PROTECTION, str)

    def test_referrer_policy_is_str(self):
        """Test REFERRER_POLICY is a string."""
        assert isinstance(SecurityHeadersConstants.REFERRER_POLICY, str)
