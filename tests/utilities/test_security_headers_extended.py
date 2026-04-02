"""Extended tests for security headers utilities."""

from __future__ import annotations

import os
from typing import Any, Optional
from unittest.mock import patch, MagicMock

import pytest

from utilities.security_headers import SecurityHeadersUtility


class TestSecurityHeadersUtilityInit:
    """Test class for SecurityHeadersUtility initialization."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        util = SecurityHeadersUtility()
        assert util._urn is None
        assert util._user_urn is None

    def test_init_with_urn(self):
        """Test initialization with urn."""
        util = SecurityHeadersUtility(urn="test-urn")
        assert util._urn == "test-urn"

    def test_init_with_user_urn(self):
        """Test initialization with user_urn."""
        util = SecurityHeadersUtility(user_urn="user-123")
        assert util._user_urn == "user-123"

    def test_init_with_api_name(self):
        """Test initialization with api_name."""
        util = SecurityHeadersUtility(api_name="test-api")
        assert util._api_name == "test-api"

    def test_init_with_user_id(self):
        """Test initialization with user_id."""
        util = SecurityHeadersUtility(user_id="user-456")
        assert util._user_id == "user-456"


class TestLoadSettingsFromEnv:
    """Tests for load_settings_from_env method."""

    def test_load_settings_returns_dto(self, monkeypatch):
        """Test load_settings returns SecurityHeadersSettingsDTO."""
        monkeypatch.delenv("SECURITY_CONTENT_SECURITY_POLICY", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result is not None
        assert hasattr(result, "x_frame_options")

    def test_load_settings_has_frame_options(self, monkeypatch):
        """Test loaded settings has frame options."""
        monkeypatch.delenv("SECURITY_X_FRAME_OPTIONS", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result.x_frame_options is not None

    def test_load_settings_has_content_type_options(self, monkeypatch):
        """Test loaded settings has content type options."""
        monkeypatch.delenv("SECURITY_X_CONTENT_TYPE_OPTIONS", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result.x_content_type_options is not None

    def test_load_settings_has_xss_protection(self, monkeypatch):
        """Test loaded settings has XSS protection."""
        monkeypatch.delenv("SECURITY_X_XSS_PROTECTION", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result.x_xss_protection is not None

    def test_load_settings_has_referrer_policy(self, monkeypatch):
        """Test loaded settings has referrer policy."""
        monkeypatch.delenv("SECURITY_REFERRER_POLICY", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result.referrer_policy is not None

    def test_load_settings_has_hsts_settings(self, monkeypatch):
        """Test loaded settings has HSTS settings."""
        monkeypatch.delenv("SECURITY_ENABLE_HSTS", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert isinstance(result.enable_hsts, bool)
        assert isinstance(result.hsts_max_age, int)
        assert isinstance(result.hsts_include_subdomains, bool)
        assert isinstance(result.hsts_preload, bool)

    def test_load_settings_has_csp(self, monkeypatch):
        """Test loaded settings has CSP."""
        monkeypatch.delenv("SECURITY_CONTENT_SECURITY_POLICY", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result.content_security_policy is not None

    def test_load_settings_custom_csp(self, monkeypatch):
        """Test loading custom CSP."""
        monkeypatch.setenv("SECURITY_CONTENT_SECURITY_POLICY", "default-src 'self'")
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result.content_security_policy == "default-src 'self'"

    def test_load_settings_has_coop(self, monkeypatch):
        """Test loaded settings has COOP."""
        monkeypatch.delenv("SECURITY_CROSS_ORIGIN_OPENER_POLICY", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result.cross_origin_opener_policy is not None

    def test_load_settings_has_corp(self, monkeypatch):
        """Test loaded settings has CORP."""
        monkeypatch.delenv("SECURITY_CROSS_ORIGIN_RESOURCE_POLICY", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert result.cross_origin_resource_policy is not None

    def test_load_settings_has_remove_server_header(self, monkeypatch):
        """Test loaded settings has remove_server_header."""
        monkeypatch.delenv("SECURITY_REMOVE_SERVER_HEADER", raising=False)
        result = SecurityHeadersUtility.load_settings_from_env()
        assert isinstance(result.remove_server_header, bool)


class TestGetMiddlewareConfig:
    """Tests for get_middleware_config method."""

    def test_get_middleware_config(self, monkeypatch):
        """Test get_middleware_config returns config."""
        monkeypatch.delenv("SECURITY_CONTENT_SECURITY_POLICY", raising=False)
        result = SecurityHeadersUtility.get_middleware_config()
        assert result is not None


class TestSecurityHeadersUtilityProperties:
    """Test properties of SecurityHeadersUtility."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        util = SecurityHeadersUtility(urn="test-urn")
        assert util.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        util = SecurityHeadersUtility()
        util.urn = "new-urn"
        assert util.urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        util = SecurityHeadersUtility(user_urn="user-test")
        assert util.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        util = SecurityHeadersUtility()
        util.user_urn = "new-user"
        assert util.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        util = SecurityHeadersUtility(api_name="api-test")
        assert util.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        util = SecurityHeadersUtility()
        util.api_name = "new-api"
        assert util.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        util = SecurityHeadersUtility(user_id="id-test")
        assert util.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        util = SecurityHeadersUtility()
        util.user_id = "new-id"
        assert util.user_id == "new-id"

    def test_logger_property(self):
        """Test logger property."""
        util = SecurityHeadersUtility()
        assert util.logger is not None


class TestSecurityHeadersUtilityEdgeCases:
    """Test edge cases for SecurityHeadersUtility."""

    def test_empty_string_context(self):
        """Test empty string context values."""
        util = SecurityHeadersUtility(urn="", api_name="")
        assert util.urn == ""
        assert util.api_name == ""

    def test_unicode_context(self):
        """Test unicode in context."""
        util = SecurityHeadersUtility(urn="安全-urn", api_name="api-测试")
        assert "安全" in util.urn

    def test_special_characters(self):
        """Test special characters in context."""
        special = "test<>!@#$%^&*()"
        util = SecurityHeadersUtility(urn=special)
        assert util.urn == special

    def test_none_context(self):
        """Test None context values."""
        util = SecurityHeadersUtility(urn=None, api_name=None)
        assert util.urn is None
        assert util.api_name is None

    def test_multiple_instances_independent(self):
        """Test multiple instances are independent."""
        util1 = SecurityHeadersUtility(urn="urn1")
        util2 = SecurityHeadersUtility(urn="urn2")
        assert util1.urn != util2.urn
