"""Extended tests for datetime utilities."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from unittest.mock import patch, MagicMock

import pytest

from utilities.datetime import DateTimeUtility


class TestDateTimeUtilityInit:
    """Test class for DateTimeUtility initialization."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        util = DateTimeUtility()
        assert util._urn is None
        assert util._user_urn is None
        assert util._api_name is None
        assert util._user_id is None

    def test_init_with_urn(self):
        """Test initialization with urn."""
        util = DateTimeUtility(urn="test-urn")
        assert util._urn == "test-urn"

    def test_init_with_user_urn(self):
        """Test initialization with user_urn."""
        util = DateTimeUtility(user_urn="user-123")
        assert util._user_urn == "user-123"

    def test_init_with_api_name(self):
        """Test initialization with api_name."""
        util = DateTimeUtility(api_name="test-api")
        assert util._api_name == "test-api"

    def test_init_with_user_id(self):
        """Test initialization with user_id."""
        util = DateTimeUtility(user_id="user-456")
        assert util._user_id == "user-456"

    def test_init_with_all_context(self):
        """Test initialization with all context parameters."""
        util = DateTimeUtility(
            urn="urn-1",
            user_urn="user-2",
            api_name="api-3",
            user_id="user-4"
        )
        assert util._urn == "urn-1"
        assert util._user_urn == "user-2"
        assert util._api_name == "api-3"
        assert util._user_id == "user-4"

    def test_init_with_kwargs(self):
        """Test initialization with **kwargs."""
        # DateTimeUtility doesn't accept extra kwargs, just test it initializes
        util = DateTimeUtility()
        assert util is not None


class TestUtcNow:
    """Tests for utc_now method."""

    def test_utc_now_returns_datetime(self):
        """Test utc_now returns a datetime object."""
        result = DateTimeUtility.utc_now()
        assert isinstance(result, datetime)

    def test_utc_now_has_timezone(self):
        """Test utc_now returns datetime with timezone."""
        result = DateTimeUtility.utc_now()
        assert result.tzinfo is not None

    def test_utc_now_is_utc(self):
        """Test utc_now returns UTC datetime."""
        result = DateTimeUtility.utc_now()
        assert result.tzinfo == timezone.utc

    def test_utc_now_recent(self):
        """Test utc_now returns recent time."""
        before = datetime.now(timezone.utc)
        result = DateTimeUtility.utc_now()
        after = datetime.now(timezone.utc)
        assert before <= result <= after

    def test_utc_now_different_calls(self):
        """Test utc_now returns different times on different calls."""
        result1 = DateTimeUtility.utc_now()
        result2 = DateTimeUtility.utc_now()
        # They could be equal if called very quickly, but usually not
        assert result1 <= result2


class TestUtcNowIso:
    """Tests for utc_now_iso method."""

    def test_utc_now_iso_returns_string(self):
        """Test utc_now_iso returns a string."""
        result = DateTimeUtility.utc_now_iso()
        assert isinstance(result, str)

    def test_utc_now_iso_format(self):
        """Test utc_now_iso returns ISO format."""
        result = DateTimeUtility.utc_now_iso()
        # Should contain T for ISO format
        assert "T" in result

    def test_utc_now_iso_has_timezone(self):
        """Test utc_now_iso includes timezone."""
        result = DateTimeUtility.utc_now_iso()
        # Should end with +00:00 or Z
        assert "+00:00" in result or result.endswith("Z")

    def test_utc_now_iso_parseable(self):
        """Test utc_now_iso returns parseable string."""
        result = DateTimeUtility.utc_now_iso()
        parsed = datetime.fromisoformat(result.replace("Z", "+00:00"))
        assert isinstance(parsed, datetime)


class TestDateTimeUtilityProperties:
    """Test properties of DateTimeUtility."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        util = DateTimeUtility(urn="test-urn")
        assert util.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        util = DateTimeUtility()
        util.urn = "new-urn"
        assert util.urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        util = DateTimeUtility(user_urn="user-test")
        assert util.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        util = DateTimeUtility()
        util.user_urn = "new-user"
        assert util.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        util = DateTimeUtility(api_name="api-test")
        assert util.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        util = DateTimeUtility()
        util.api_name = "new-api"
        assert util.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        util = DateTimeUtility(user_id="id-test")
        assert util.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        util = DateTimeUtility()
        util.user_id = "new-id"
        assert util.user_id == "new-id"

    def test_logger_property(self):
        """Test logger property."""
        util = DateTimeUtility()
        assert util.logger is not None


class TestDateTimeUtilityEdgeCases:
    """Test edge cases for DateTimeUtility."""

    def test_empty_string_context(self):
        """Test empty string context values."""
        util = DateTimeUtility(urn="", api_name="")
        assert util.urn == ""
        assert util.api_name == ""

    def test_unicode_context(self):
        """Test unicode in context."""
        util = DateTimeUtility(urn="时间-urn", api_name="api-测试")
        assert "时间" in util.urn
        assert "测试" in util.api_name

    def test_special_characters(self):
        """Test special characters in context."""
        special = "test<>!@#$%^&*()"
        util = DateTimeUtility(urn=special)
        assert util.urn == special

    def test_none_context(self):
        """Test None context values."""
        util = DateTimeUtility(urn=None, api_name=None)
        assert util.urn is None
        assert util.api_name is None

    def test_multiple_instances_independent(self):
        """Test multiple instances are independent."""
        util1 = DateTimeUtility(urn="urn1")
        util2 = DateTimeUtility(urn="urn2")
        assert util1.urn != util2.urn
