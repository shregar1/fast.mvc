"""Extended tests for auth utilities."""

from __future__ import annotations

import base64
import secrets
from typing import Optional, Tuple
from unittest.mock import patch, MagicMock

import pytest

from utilities.auth import AuthUtility


class TestAuthUtilityInit:
    """Test class for AuthUtility initialization."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        util = AuthUtility()
        assert util._urn is None
        assert util._user_urn is None

    def test_init_with_urn(self):
        """Test initialization with urn."""
        util = AuthUtility(urn="test-urn")
        assert util._urn == "test-urn"

    def test_init_with_user_urn(self):
        """Test initialization with user_urn."""
        util = AuthUtility(user_urn="user-123")
        assert util._user_urn == "user-123"

    def test_init_with_api_name(self):
        """Test initialization with api_name."""
        util = AuthUtility(api_name="test-api")
        assert util._api_name == "api-test"

    def test_init_with_user_id(self):
        """Test initialization with user_id."""
        util = AuthUtility(user_id="user-456")
        assert util._user_id == "user-456"


class TestParseBasicAuthorization:
    """Tests for parse_basic_authorization method."""

    def test_parse_basic_auth_valid(self):
        """Test parsing valid basic authorization."""
        credentials = base64.b64encode(b"user:pass").decode()
        header = f"Basic {credentials}"
        result = AuthUtility.parse_basic_authorization(header)
        assert result == ("user", "pass")

    def test_parse_basic_auth_none(self):
        """Test parsing None returns None."""
        result = AuthUtility.parse_basic_authorization(None)
        assert result is None

    def test_parse_basic_auth_empty(self):
        """Test parsing empty string returns None."""
        result = AuthUtility.parse_basic_authorization("")
        assert result is None

    def test_parse_basic_auth_not_basic(self):
        """Test parsing non-Basic header returns None."""
        result = AuthUtility.parse_basic_authorization("Bearer token123")
        assert result is None

    def test_parse_basic_auth_invalid_base64(self):
        """Test parsing invalid base64 returns None."""
        result = AuthUtility.parse_basic_authorization("Basic not_valid_base64!!!")
        assert result is None

    def test_parse_basic_auth_no_colon(self):
        """Test parsing credentials without colon returns None."""
        credentials = base64.b64encode(b"nocolon").decode()
        header = f"Basic {credentials}"
        result = AuthUtility.parse_basic_authorization(header)
        assert result is None

    def test_parse_basic_auth_multiple_colons(self):
        """Test parsing credentials with multiple colons."""
        credentials = base64.b64encode(b"user:pass:word").decode()
        header = f"Basic {credentials}"
        result = AuthUtility.parse_basic_authorization(header)
        assert result == ("user", "pass:word")

    def test_parse_basic_auth_empty_password(self):
        """Test parsing credentials with empty password."""
        credentials = base64.b64encode(b"user:").decode()
        header = f"Basic {credentials}"
        result = AuthUtility.parse_basic_authorization(header)
        assert result == ("user", "")

    def test_parse_basic_auth_empty_username(self):
        """Test parsing credentials with empty username."""
        credentials = base64.b64encode(b":pass").decode()
        header = f"Basic {credentials}"
        result = AuthUtility.parse_basic_authorization(header)
        assert result == ("", "pass")

    def test_parse_basic_auth_unicode(self):
        """Test parsing credentials with unicode."""
        credentials = base64.b64encode("用户:密码".encode("utf-8")).decode()
        header = f"Basic {credentials}"
        result = AuthUtility.parse_basic_authorization(header)
        assert result == ("用户", "密码")


class TestConstantTimeCompare:
    """Tests for constant_time_compare method."""

    def test_compare_equal_strings(self):
        """Test comparing equal strings."""
        assert AuthUtility.constant_time_compare("hello", "hello") is True

    def test_compare_different_strings(self):
        """Test comparing different strings."""
        assert AuthUtility.constant_time_compare("hello", "world") is False

    def test_compare_different_lengths(self):
        """Test comparing strings of different lengths."""
        assert AuthUtility.constant_time_compare("hi", "hello") is False

    def test_compare_empty_strings(self):
        """Test comparing empty strings."""
        assert AuthUtility.constant_time_compare("", "") is True

    def test_compare_empty_and_nonempty(self):
        """Test comparing empty and non-empty strings."""
        assert AuthUtility.constant_time_compare("", "hello") is False

    def test_compare_unicode(self):
        """Test comparing unicode strings."""
        assert AuthUtility.constant_time_compare("你好", "你好") is True
        assert AuthUtility.constant_time_compare("你好", "世界") is False

    def test_compare_special_chars(self):
        """Test comparing strings with special characters."""
        assert AuthUtility.constant_time_compare("!@#$%", "!@#$%") is True
        assert AuthUtility.constant_time_compare("!@#$%", "^&*()") is False


class TestAuthUtilityProperties:
    """Test properties of AuthUtility."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        util = AuthUtility(urn="test-urn")
        assert util.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        util = AuthUtility()
        util.urn = "new-urn"
        assert util.urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        util = AuthUtility(user_urn="user-test")
        assert util.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        util = AuthUtility()
        util.user_urn = "new-user"
        assert util.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        util = AuthUtility(api_name="api-test")
        assert util.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        util = AuthUtility()
        util.api_name = "new-api"
        assert util.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        util = AuthUtility(user_id="id-test")
        assert util.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        util = AuthUtility()
        util.user_id = "new-id"
        assert util.user_id == "new-id"

    def test_logger_property(self):
        """Test logger property."""
        util = AuthUtility()
        assert util.logger is not None


class TestAuthUtilityEdgeCases:
    """Test edge cases for AuthUtility."""

    def test_empty_string_context(self):
        """Test empty string context values."""
        util = AuthUtility(urn="", api_name="")
        assert util.urn == ""
        assert util.api_name == ""

    def test_unicode_context(self):
        """Test unicode in context."""
        util = AuthUtility(urn="认证-urn", api_name="api-测试")
        assert "认证" in util.urn

    def test_special_characters(self):
        """Test special characters in context."""
        special = "test<>!@#$%^&*()"
        util = AuthUtility(urn=special)
        assert util.urn == special

    def test_none_context(self):
        """Test None context values."""
        util = AuthUtility(urn=None, api_name=None)
        assert util.urn is None
        assert util.api_name is None

    def test_multiple_instances_independent(self):
        """Test multiple instances are independent."""
        util1 = AuthUtility(urn="urn1")
        util2 = AuthUtility(urn="urn2")
        assert util1.urn != util2.urn
