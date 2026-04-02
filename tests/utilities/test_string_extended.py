"""Extended tests for string utilities."""

from __future__ import annotations

from typing import List, Optional, Sequence
from unittest.mock import patch, MagicMock

import pytest

from utilities.string import StringUtility


class TestStringUtilityInit:
    """Test class for StringUtility initialization."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        util = StringUtility()
        assert util._urn is None
        assert util._user_urn is None

    def test_init_with_urn(self):
        """Test initialization with urn."""
        util = StringUtility(urn="test-urn")
        assert util._urn == "test-urn"

    def test_init_with_user_urn(self):
        """Test initialization with user_urn."""
        util = StringUtility(user_urn="user-123")
        assert util._user_urn == "user-123"

    def test_init_with_api_name(self):
        """Test initialization with api_name."""
        util = StringUtility(api_name="test-api")
        assert util._api_name == "test-api"

    def test_init_with_user_id(self):
        """Test initialization with user_id."""
        util = StringUtility(user_id="user-456")
        assert util._user_id == "user-456"

    def test_init_with_all_context(self):
        """Test initialization with all context parameters."""
        util = StringUtility(
            urn="urn-1",
            user_urn="user-2",
            api_name="api-3",
            user_id="user-4"
        )
        assert util._urn == "urn-1"
        assert util._user_urn == "user-2"
        assert util._api_name == "api-3"
        assert util._user_id == "user-4"


class TestSplitCsv:
    """Tests for split_csv method."""

    def test_split_csv_single(self):
        """Test splitting single value."""
        result = StringUtility.split_csv("value1", [])
        assert result == ["value1"]

    def test_split_csv_multiple(self):
        """Test splitting multiple values."""
        result = StringUtility.split_csv("a,b,c", [])
        assert result == ["a", "b", "c"]

    def test_split_csv_with_spaces(self):
        """Test splitting values with spaces."""
        result = StringUtility.split_csv(" a , b , c ", [])
        assert result == ["a", "b", "c"]

    def test_split_csv_empty_parts(self):
        """Test splitting with empty parts."""
        result = StringUtility.split_csv("a,,b", [])
        assert result == ["a", "b"]

    def test_split_csv_whitespace_parts(self):
        """Test splitting with whitespace parts."""
        result = StringUtility.split_csv("a,  ,b", [])
        assert result == ["a", "b"]

    def test_split_csv_none(self):
        """Test splitting None returns default."""
        default = ["default"]
        result = StringUtility.split_csv(None, default)
        assert result == default

    def test_split_csv_empty_string(self):
        """Test splitting empty string returns default."""
        default = ["default"]
        result = StringUtility.split_csv("", default)
        assert result == default

    def test_split_csv_whitespace_only(self):
        """Test splitting whitespace only returns default."""
        default = ["default"]
        result = StringUtility.split_csv("   ", default)
        assert result == default

    def test_split_csv_all_blank_returns_default(self):
        """Test splitting all blank parts returns default."""
        default = ["default"]
        result = StringUtility.split_csv(", , ,", default)
        assert result == default


class TestNormalizePath:
    """Tests for normalize_path method."""

    def test_normalize_path_adds_leading_slash(self):
        """Test normalize_path adds leading slash."""
        result = StringUtility.normalize_path("api/v1")
        assert result == "/api/v1"

    def test_normalize_path_keeps_existing_slash(self):
        """Test normalize_path keeps existing leading slash."""
        result = StringUtility.normalize_path("/api/v1")
        assert result == "/api/v1"

    def test_normalize_path_no_leading_slash_disabled(self):
        """Test normalize_path with leading_slash=False."""
        result = StringUtility.normalize_path("api/v1", leading_slash=False)
        assert result == "api/v1"

    def test_normalize_path_removes_leading_slash_when_disabled(self):
        """Test normalize_path removes leading slash when disabled."""
        result = StringUtility.normalize_path("/api/v1", leading_slash=False)
        assert result == "/api/v1"

    def test_normalize_path_empty(self):
        """Test normalize_path with empty string."""
        result = StringUtility.normalize_path("")
        assert result == "/"

    def test_normalize_path_single_slash(self):
        """Test normalize_path with single slash."""
        result = StringUtility.normalize_path("/")
        assert result == "/"

    def test_normalize_path_idempotent(self):
        """Test normalize_path is idempotent."""
        result1 = StringUtility.normalize_path("api/v1")
        result2 = StringUtility.normalize_path(result1)
        assert result1 == result2


class TestStringUtilityProperties:
    """Test properties of StringUtility."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        util = StringUtility(urn="test-urn")
        assert util.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        util = StringUtility()
        util.urn = "new-urn"
        assert util.urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        util = StringUtility(user_urn="user-test")
        assert util.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        util = StringUtility()
        util.user_urn = "new-user"
        assert util.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        util = StringUtility(api_name="api-test")
        assert util.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        util = StringUtility()
        util.api_name = "new-api"
        assert util.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        util = StringUtility(user_id="id-test")
        assert util.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        util = StringUtility()
        util.user_id = "new-id"
        assert util.user_id == "new-id"

    def test_logger_property(self):
        """Test logger property."""
        util = StringUtility()
        assert util.logger is not None


class TestStringUtilityEdgeCases:
    """Test edge cases for StringUtility."""

    def test_empty_string_context(self):
        """Test empty string context values."""
        util = StringUtility(urn="", api_name="")
        assert util.urn == ""
        assert util.api_name == ""

    def test_unicode_context(self):
        """Test unicode in context."""
        util = StringUtility(urn="字符串-urn", api_name="api-测试")
        assert "字符串" in util.urn

    def test_special_characters(self):
        """Test special characters in context."""
        special = "test<>!@#$%^&*()"
        util = StringUtility(urn=special)
        assert util.urn == special

    def test_none_context(self):
        """Test None context values."""
        util = StringUtility(urn=None, api_name=None)
        assert util.urn is None
        assert util.api_name is None

    def test_multiple_instances_independent(self):
        """Test multiple instances are independent."""
        util1 = StringUtility(urn="urn1")
        util2 = StringUtility(urn="urn2")
        assert util1.urn != util2.urn
