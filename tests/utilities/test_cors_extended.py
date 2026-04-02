"""Extended tests for CORS utilities."""

from __future__ import annotations

import os
from typing import Any, List, Optional
from unittest.mock import patch, MagicMock

import pytest

from utilities.cors import CorsConfigUtility


class TestCorsConfigUtilityInit:
    """Test class for CorsConfigUtility initialization."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        util = CorsConfigUtility()
        assert util._urn is None
        assert util._user_urn is None

    def test_init_with_urn(self):
        """Test initialization with urn."""
        util = CorsConfigUtility(urn="test-urn")
        assert util._urn == "test-urn"

    def test_init_with_user_urn(self):
        """Test initialization with user_urn."""
        util = CorsConfigUtility(user_urn="user-123")
        assert util._user_urn == "user-123"

    def test_init_with_api_name(self):
        """Test initialization with api_name."""
        util = CorsConfigUtility(api_name="test-api")
        assert util._api_name == "api-test"

    def test_init_with_user_id(self):
        """Test initialization with user_id."""
        util = CorsConfigUtility(user_id="user-456")
        assert util._user_id == "user-456"


class TestParseAllowOrigins:
    """Tests for parse_allow_origins method."""

    def test_parse_origins_from_cors_origins(self, monkeypatch):
        """Test parsing origins from CORS_ORIGINS."""
        monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080")
        result = CorsConfigUtility.parse_allow_origins()
        assert result == ["http://localhost:3000", "http://localhost:8080"]

    def test_parse_origins_from_allowed_origins(self, monkeypatch):
        """Test parsing origins from CORS_ALLOWED_ORIGINS."""
        monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "http://example.com")
        result = CorsConfigUtility.parse_allow_origins()
        assert result == ["http://example.com"]

    def test_parse_origins_cors_origins_takes_precedence(self, monkeypatch):
        """Test CORS_ORIGINS takes precedence over CORS_ALLOWED_ORIGINS."""
        monkeypatch.setenv("CORS_ORIGINS", "http://first.com")
        monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "http://second.com")
        result = CorsConfigUtility.parse_allow_origins()
        assert result == ["http://first.com"]

    def test_parse_origins_not_set(self, monkeypatch):
        """Test parsing when not set returns fallback."""
        monkeypatch.delenv("CORS_ORIGINS", raising=False)
        monkeypatch.delenv("CORS_ALLOWED_ORIGINS", raising=False)
        result = CorsConfigUtility.parse_allow_origins()
        assert "*" in result

    def test_parse_origins_empty(self, monkeypatch):
        """Test parsing empty returns fallback."""
        monkeypatch.setenv("CORS_ORIGINS", "")
        result = CorsConfigUtility.parse_allow_origins()
        assert "*" in result

    def test_parse_origins_whitespace(self, monkeypatch):
        """Test parsing whitespace returns fallback."""
        monkeypatch.setenv("CORS_ORIGINS", "   ")
        result = CorsConfigUtility.parse_allow_origins()
        assert "*" in result

    def test_parse_origins_with_spaces(self, monkeypatch):
        """Test parsing origins with extra spaces."""
        monkeypatch.setenv("CORS_ORIGINS", " http://localhost:3000 , http://localhost:8080 ")
        result = CorsConfigUtility.parse_allow_origins()
        assert result == ["http://localhost:3000", "http://localhost:8080"]


class TestParseAllowHeaders:
    """Tests for parse_allow_headers method."""

    def test_parse_headers_custom(self, monkeypatch):
        """Test parsing custom headers."""
        monkeypatch.setenv("CORS_ALLOW_HEADERS", "X-Custom,Authorization")
        result = CorsConfigUtility.parse_allow_headers()
        assert result == ["X-Custom", "Authorization"]

    def test_parse_headers_wildcard(self, monkeypatch):
        """Test parsing wildcard headers returns fallback."""
        monkeypatch.setenv("CORS_ALLOW_HEADERS", "*")
        result = CorsConfigUtility.parse_allow_headers()
        # Should return fallback headers
        assert "Content-Type" in result

    def test_parse_headers_not_set(self, monkeypatch):
        """Test parsing when not set returns fallback."""
        monkeypatch.delenv("CORS_ALLOW_HEADERS", raising=False)
        result = CorsConfigUtility.parse_allow_headers()
        assert "Content-Type" in result

    def test_parse_headers_empty(self, monkeypatch):
        """Test parsing empty returns fallback."""
        monkeypatch.setenv("CORS_ALLOW_HEADERS", "")
        result = CorsConfigUtility.parse_allow_headers()
        assert "Content-Type" in result


class TestLoadSettingsFromEnv:
    """Tests for load_settings_from_env method."""

    def test_load_settings_returns_dto(self, monkeypatch):
        """Test load_settings returns CorsSettingsDTO."""
        monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000")
        result = CorsConfigUtility.load_settings_from_env()
        assert result is not None
        assert hasattr(result, "allow_origins")

    def test_load_settings_has_origins(self, monkeypatch):
        """Test loaded settings has origins."""
        monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000")
        result = CorsConfigUtility.load_settings_from_env()
        assert "http://localhost:3000" in result.allow_origins

    def test_load_settings_has_methods(self, monkeypatch):
        """Test loaded settings has methods."""
        monkeypatch.delenv("CORS_ALLOW_METHODS", raising=False)
        result = CorsConfigUtility.load_settings_from_env()
        assert len(result.allow_methods) > 0

    def test_load_settings_has_headers(self, monkeypatch):
        """Test loaded settings has headers."""
        monkeypatch.delenv("CORS_ALLOW_HEADERS", raising=False)
        result = CorsConfigUtility.load_settings_from_env()
        assert len(result.allow_headers) > 0

    def test_load_settings_has_credentials(self, monkeypatch):
        """Test loaded settings has credentials."""
        monkeypatch.delenv("CORS_ALLOW_CREDENTIALS", raising=False)
        result = CorsConfigUtility.load_settings_from_env()
        assert isinstance(result.allow_credentials, bool)

    def test_load_settings_has_max_age(self, monkeypatch):
        """Test loaded settings has max_age."""
        monkeypatch.delenv("CORS_MAX_AGE", raising=False)
        result = CorsConfigUtility.load_settings_from_env()
        assert isinstance(result.max_age, int)


class TestGetMiddlewareKwargs:
    """Tests for get_middleware_kwargs method."""

    def test_get_middleware_kwargs_returns_dict(self, monkeypatch):
        """Test get_middleware_kwargs returns dict."""
        monkeypatch.delenv("CORS_ORIGINS", raising=False)
        result = CorsConfigUtility.get_middleware_kwargs()
        assert isinstance(result, dict)

    def test_get_middleware_kwargs_has_required_keys(self, monkeypatch):
        """Test get_middleware_kwargs has required keys."""
        monkeypatch.delenv("CORS_ORIGINS", raising=False)
        result = CorsConfigUtility.get_middleware_kwargs()
        assert "allow_origins" in result
        assert "allow_methods" in result
        assert "allow_headers" in result


class TestCorsConfigUtilityProperties:
    """Test properties of CorsConfigUtility."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        util = CorsConfigUtility(urn="test-urn")
        assert util.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        util = CorsConfigUtility()
        util.urn = "new-urn"
        assert util.urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        util = CorsConfigUtility(user_urn="user-test")
        assert util.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        util = CorsConfigUtility()
        util.user_urn = "new-user"
        assert util.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        util = CorsConfigUtility(api_name="api-test")
        assert util.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        util = CorsConfigUtility()
        util.api_name = "new-api"
        assert util.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        util = CorsConfigUtility(user_id="id-test")
        assert util.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        util = CorsConfigUtility()
        util.user_id = "new-id"
        assert util.user_id == "new-id"

    def test_logger_property(self):
        """Test logger property."""
        util = CorsConfigUtility()
        assert util.logger is not None


class TestCorsConfigUtilityEdgeCases:
    """Test edge cases for CorsConfigUtility."""

    def test_empty_string_context(self):
        """Test empty string context values."""
        util = CorsConfigUtility(urn="", api_name="")
        assert util.urn == ""
        assert util.api_name == ""

    def test_unicode_context(self):
        """Test unicode in context."""
        util = CorsConfigUtility(urn="跨域-urn", api_name="api-测试")
        assert "跨域" in util.urn

    def test_special_characters(self):
        """Test special characters in context."""
        special = "test<>!@#$%^&*()"
        util = CorsConfigUtility(urn=special)
        assert util.urn == special

    def test_none_context(self):
        """Test None context values."""
        util = CorsConfigUtility(urn=None, api_name=None)
        assert util.urn is None
        assert util.api_name is None

    def test_multiple_instances_independent(self):
        """Test multiple instances are independent."""
        util1 = CorsConfigUtility(urn="urn1")
        util2 = CorsConfigUtility(urn="urn2")
        assert util1.urn != util2.urn
