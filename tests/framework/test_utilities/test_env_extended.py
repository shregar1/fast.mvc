"""Extended tests for environment variable parsing utilities."""

from __future__ import annotations

import os
from typing import Sequence

import pytest

from utilities.env import EnvironmentParserUtility


class TestEnvironmentParserUtilityInit:
    """Test class for EnvironmentParserUtility initialization."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        parser = EnvironmentParserUtility()
        assert parser._urn is None
        assert parser._user_urn is None
        assert parser._api_name is None
        assert parser._user_id is None

    def test_init_with_urn(self):
        """Test initialization with urn."""
        parser = EnvironmentParserUtility(urn="test-urn")
        assert parser._urn == "test-urn"

    def test_init_with_user_urn(self):
        """Test initialization with user_urn."""
        parser = EnvironmentParserUtility(user_urn="user-123")
        assert parser._user_urn == "user-123"

    def test_init_with_api_name(self):
        """Test initialization with api_name."""
        parser = EnvironmentParserUtility(api_name="test-api")
        assert parser._api_name == "test-api"

    def test_init_with_user_id(self):
        """Test initialization with user_id."""
        parser = EnvironmentParserUtility(user_id="user-456")
        assert parser._user_id == "user-456"

    def test_init_with_all_context(self):
        """Test initialization with all context parameters."""
        parser = EnvironmentParserUtility(
            urn="urn-1",
            user_urn="user-2",
            api_name="api-3",
            user_id="user-4"
        )
        assert parser._urn == "urn-1"
        assert parser._user_urn == "user-2"
        assert parser._api_name == "api-3"
        assert parser._user_id == "user-4"

    def test_init_basic(self):
        """Test basic initialization."""
        parser = EnvironmentParserUtility()
        # Should not raise and should be initialized
        assert parser is not None


class TestParseBoolExtended:
    """Extended tests for parse_bool method."""

    def test_parse_bool_true_lowercase(self, monkeypatch):
        """Test parsing 'true' lowercase."""
        monkeypatch.setenv("TEST_BOOL", "true")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is True

    def test_parse_bool_true_uppercase(self, monkeypatch):
        """Test parsing 'TRUE' uppercase."""
        monkeypatch.setenv("TEST_BOOL", "TRUE")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is True

    def test_parse_bool_true_mixed_case(self, monkeypatch):
        """Test parsing 'True' mixed case."""
        monkeypatch.setenv("TEST_BOOL", "True")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is True

    def test_parse_bool_one(self, monkeypatch):
        """Test parsing '1'."""
        monkeypatch.setenv("TEST_BOOL", "1")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is True

    def test_parse_bool_yes(self, monkeypatch):
        """Test parsing 'yes'."""
        monkeypatch.setenv("TEST_BOOL", "yes")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is True

    def test_parse_bool_on(self, monkeypatch):
        """Test parsing 'on'."""
        monkeypatch.setenv("TEST_BOOL", "on")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is True

    def test_parse_bool_false_lowercase(self, monkeypatch):
        """Test parsing 'false' lowercase."""
        monkeypatch.setenv("TEST_BOOL", "false")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False

    def test_parse_bool_false_uppercase(self, monkeypatch):
        """Test parsing 'FALSE' uppercase."""
        monkeypatch.setenv("TEST_BOOL", "FALSE")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False

    def test_parse_bool_zero(self, monkeypatch):
        """Test parsing '0'."""
        monkeypatch.setenv("TEST_BOOL", "0")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False

    def test_parse_bool_no(self, monkeypatch):
        """Test parsing 'no'."""
        monkeypatch.setenv("TEST_BOOL", "no")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False

    def test_parse_bool_off(self, monkeypatch):
        """Test parsing 'off'."""
        monkeypatch.setenv("TEST_BOOL", "off")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False

    def test_parse_bool_empty_string(self, monkeypatch):
        """Test parsing empty string returns False (not in true values)."""
        monkeypatch.setenv("TEST_BOOL", "")
        # Empty string is not a true value, returns False
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is False

    def test_parse_bool_whitespace(self, monkeypatch):
        """Test parsing whitespace returns False (not in true values)."""
        monkeypatch.setenv("TEST_BOOL", "   ")
        # Whitespace is not a true value, returns False
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False

    def test_parse_bool_random_string(self, monkeypatch):
        """Test parsing random string returns False."""
        monkeypatch.setenv("TEST_BOOL", "random")
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is False

    def test_parse_bool_not_set(self, monkeypatch):
        """Test parsing when env var not set."""
        monkeypatch.delenv("TEST_BOOL", raising=False)
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", True) is True
        assert EnvironmentParserUtility.parse_bool("TEST_BOOL", False) is False


class TestParseIntExtended:
    """Extended tests for parse_int method."""

    def test_parse_int_positive(self, monkeypatch):
        """Test parsing positive integer."""
        monkeypatch.setenv("TEST_INT", "42")
        assert EnvironmentParserUtility.parse_int("TEST_INT", 0) == 42

    def test_parse_int_negative(self, monkeypatch):
        """Test parsing negative integer."""
        monkeypatch.setenv("TEST_INT", "-42")
        assert EnvironmentParserUtility.parse_int("TEST_INT", 0) == -42

    def test_parse_int_zero(self, monkeypatch):
        """Test parsing zero."""
        monkeypatch.setenv("TEST_INT", "0")
        assert EnvironmentParserUtility.parse_int("TEST_INT", 100) == 0

    def test_parse_int_large(self, monkeypatch):
        """Test parsing large integer."""
        monkeypatch.setenv("TEST_INT", "999999999")
        assert EnvironmentParserUtility.parse_int("TEST_INT", 0) == 999999999

    def test_parse_int_with_whitespace(self, monkeypatch):
        """Test parsing integer with whitespace."""
        monkeypatch.setenv("TEST_INT", "  42  ")
        assert EnvironmentParserUtility.parse_int("TEST_INT", 0) == 42

    def test_parse_int_empty(self, monkeypatch):
        """Test parsing empty returns default."""
        monkeypatch.setenv("TEST_INT", "")
        assert EnvironmentParserUtility.parse_int("TEST_INT", 100) == 100

    def test_parse_int_whitespace_only(self, monkeypatch):
        """Test parsing whitespace only returns default."""
        monkeypatch.setenv("TEST_INT", "   ")
        assert EnvironmentParserUtility.parse_int("TEST_INT", 100) == 100

    def test_parse_int_not_set(self, monkeypatch):
        """Test parsing when not set returns default."""
        monkeypatch.delenv("TEST_INT", raising=False)
        assert EnvironmentParserUtility.parse_int("TEST_INT", 100) == 100


class TestParseStrExtended:
    """Extended tests for parse_str method."""

    def test_parse_str_simple(self, monkeypatch):
        """Test parsing simple string."""
        monkeypatch.setenv("TEST_STR", "hello")
        assert EnvironmentParserUtility.parse_str("TEST_STR", "default") == "hello"

    def test_parse_str_with_spaces(self, monkeypatch):
        """Test parsing string with spaces."""
        monkeypatch.setenv("TEST_STR", "hello world")
        assert EnvironmentParserUtility.parse_str("TEST_STR", "default") == "hello world"

    def test_parse_str_empty(self, monkeypatch):
        """Test parsing empty string returns empty."""
        monkeypatch.setenv("TEST_STR", "")
        assert EnvironmentParserUtility.parse_str("TEST_STR", "default") == ""

    def test_parse_str_not_set(self, monkeypatch):
        """Test parsing when not set returns default."""
        monkeypatch.delenv("TEST_STR", raising=False)
        assert EnvironmentParserUtility.parse_str("TEST_STR", "default") == "default"

    def test_parse_str_special_chars(self, monkeypatch):
        """Test parsing string with special characters."""
        monkeypatch.setenv("TEST_STR", "hello!@#$%^&*()")
        assert EnvironmentParserUtility.parse_str("TEST_STR", "default") == "hello!@#$%^&*()"


class TestParseOptionalStrExtended:
    """Extended tests for parse_optional_str method."""

    def test_parse_optional_str_value(self, monkeypatch):
        """Test parsing optional string with value."""
        monkeypatch.setenv("TEST_OPT", "value")
        assert EnvironmentParserUtility.parse_optional_str("TEST_OPT") == "value"

    def test_parse_optional_str_not_set(self, monkeypatch):
        """Test parsing optional string when not set."""
        monkeypatch.delenv("TEST_OPT", raising=False)
        assert EnvironmentParserUtility.parse_optional_str("TEST_OPT") is None

    def test_parse_optional_str_empty(self, monkeypatch):
        """Test parsing optional string when empty."""
        monkeypatch.setenv("TEST_OPT", "")
        assert EnvironmentParserUtility.parse_optional_str("TEST_OPT") is None

    def test_parse_optional_str_whitespace(self, monkeypatch):
        """Test parsing optional string with only whitespace."""
        monkeypatch.setenv("TEST_OPT", "   ")
        assert EnvironmentParserUtility.parse_optional_str("TEST_OPT") is None

    def test_parse_optional_str_with_whitespace_value(self, monkeypatch):
        """Test parsing optional string with value surrounded by whitespace."""
        monkeypatch.setenv("TEST_OPT", "  value  ")
        assert EnvironmentParserUtility.parse_optional_str("TEST_OPT") == "  value  "


class TestParseCsvExtended:
    """Extended tests for parse_csv method."""

    def test_parse_csv_single(self, monkeypatch):
        """Test parsing single value."""
        monkeypatch.setenv("TEST_CSV", "value1")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["value1"]

    def test_parse_csv_multiple(self, monkeypatch):
        """Test parsing multiple values."""
        monkeypatch.setenv("TEST_CSV", "a,b,c")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["a", "b", "c"]

    def test_parse_csv_with_spaces(self, monkeypatch):
        """Test parsing values with spaces."""
        monkeypatch.setenv("TEST_CSV", " a , b , c ")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["a", "b", "c"]

    def test_parse_csv_empty_parts(self, monkeypatch):
        """Test parsing with empty parts."""
        monkeypatch.setenv("TEST_CSV", "a,,b")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["a", "b"]

    def test_parse_csv_whitespace_parts(self, monkeypatch):
        """Test parsing with whitespace parts."""
        monkeypatch.setenv("TEST_CSV", "a,  ,b")
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", [])
        assert result == ["a", "b"]

    def test_parse_csv_not_set(self, monkeypatch):
        """Test parsing when not set returns default."""
        monkeypatch.delenv("TEST_CSV", raising=False)
        default = ["default1", "default2"]
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", default)
        assert result == default

    def test_parse_csv_empty(self, monkeypatch):
        """Test parsing empty returns default."""
        monkeypatch.setenv("TEST_CSV", "")
        default = ["default1"]
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", default)
        assert result == default

    def test_parse_csv_whitespace_only(self, monkeypatch):
        """Test parsing whitespace only returns default."""
        monkeypatch.setenv("TEST_CSV", "   ")
        default = ["default1"]
        result = EnvironmentParserUtility.parse_csv("TEST_CSV", default)
        assert result == default


class TestGetIntWithLoggingExtended:
    """Extended tests for get_int_with_logging method."""

    def test_get_int_with_logging_valid(self, monkeypatch):
        """Test get_int_with_logging with valid value."""
        monkeypatch.setenv("TEST_INT", "42")
        assert EnvironmentParserUtility.get_int_with_logging("TEST_INT", 0) == 42

    def test_get_int_with_logging_not_set(self, monkeypatch):
        """Test get_int_with_logging when not set."""
        monkeypatch.delenv("TEST_INT", raising=False)
        assert EnvironmentParserUtility.get_int_with_logging("TEST_INT", 100) == 100

    def test_get_int_with_logging_invalid(self, monkeypatch):
        """Test get_int_with_logging with invalid value."""
        monkeypatch.setenv("TEST_INT", "not_a_number")
        assert EnvironmentParserUtility.get_int_with_logging("TEST_INT", 100) == 100


class TestGetBoolWithLoggingExtended:
    """Extended tests for get_bool_with_logging method."""

    def test_get_bool_with_logging_true(self, monkeypatch):
        """Test get_bool_with_logging with true value."""
        monkeypatch.setenv("TEST_BOOL", "true")
        assert EnvironmentParserUtility.get_bool_with_logging("TEST_BOOL", False) is True

    def test_get_bool_with_logging_false(self, monkeypatch):
        """Test get_bool_with_logging with false value."""
        monkeypatch.setenv("TEST_BOOL", "false")
        assert EnvironmentParserUtility.get_bool_with_logging("TEST_BOOL", True) is False

    def test_get_bool_with_logging_not_set(self, monkeypatch):
        """Test get_bool_with_logging when not set."""
        monkeypatch.delenv("TEST_BOOL", raising=False)
        assert EnvironmentParserUtility.get_bool_with_logging("TEST_BOOL", True) is True


class TestEnvironmentParserUtilityProperties:
    """Test properties of EnvironmentParserUtility."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        parser = EnvironmentParserUtility(urn="test-urn")
        assert parser.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        parser = EnvironmentParserUtility()
        parser.urn = "new-urn"
        assert parser.urn == "new-urn"
        assert parser._urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        parser = EnvironmentParserUtility(user_urn="user-test")
        assert parser.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        parser = EnvironmentParserUtility()
        parser.user_urn = "new-user"
        assert parser.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        parser = EnvironmentParserUtility(api_name="api-test")
        assert parser.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        parser = EnvironmentParserUtility()
        parser.api_name = "new-api"
        assert parser.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        parser = EnvironmentParserUtility(user_id="id-test")
        assert parser.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        parser = EnvironmentParserUtility()
        parser.user_id = "new-id"
        assert parser.user_id == "new-id"

    def test_logger_property(self):
        """Test logger property."""
        parser = EnvironmentParserUtility()
        assert parser.logger is not None


class TestEnvironmentParserUtilityEdgeCases:
    """Test edge cases for EnvironmentParserUtility."""

    def test_unicode_values(self):
        """Test unicode in context values."""
        parser = EnvironmentParserUtility(
            urn="urn-测试",
            user_urn="用户-123",
            api_name="api-测试"
        )
        assert parser.urn == "urn-测试"
        assert parser.user_urn == "用户-123"
        assert parser.api_name == "api-测试"

    def test_special_characters(self):
        """Test special characters in context values."""
        special = "test<>!@#$%^&*()_+-=[]{}|;':\",./<>?"
        parser = EnvironmentParserUtility(
            urn=special,
            user_urn=special,
            api_name=special
        )
        assert parser.urn == special

    def test_very_long_values(self):
        """Test very long context values."""
        long_value = "x" * 10000
        parser = EnvironmentParserUtility(urn=long_value)
        assert parser.urn == long_value

    def test_multiple_instances_independent(self):
        """Test multiple instances are independent."""
        parser1 = EnvironmentParserUtility(urn="urn1")
        parser2 = EnvironmentParserUtility(urn="urn2")
        assert parser1.urn != parser2.urn
        parser1.urn = "updated"
        assert parser1.urn == "updated"
        assert parser2.urn == "urn2"
