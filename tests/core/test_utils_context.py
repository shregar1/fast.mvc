"""Tests for core utils context module."""

from __future__ import annotations

from typing import Any, Dict, Optional

import pytest

from core.utils.context import ContextMixin


class TestContextMixin:
    """Tests for ContextMixin class."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        mixin = ContextMixin()
        assert mixin._urn is None
        assert mixin._user_urn is None
        assert mixin._api_name is None
        assert mixin._user_id is None
        assert mixin._context == {}

    def test_init_with_urn(self):
        """Test initialization with urn."""
        mixin = ContextMixin(urn="test-urn")
        assert mixin._urn == "test-urn"

    def test_init_with_user_urn(self):
        """Test initialization with user_urn."""
        mixin = ContextMixin(user_urn="user-123")
        assert mixin._user_urn == "user-123"

    def test_init_with_api_name(self):
        """Test initialization with api_name."""
        mixin = ContextMixin(api_name="test-api")
        assert mixin._api_name == "test-api"

    def test_init_with_user_id(self):
        """Test initialization with user_id."""
        mixin = ContextMixin(user_id="user-456")
        assert mixin._user_id == "user-456"

    def test_init_with_all_context(self):
        """Test initialization with all context parameters."""
        mixin = ContextMixin(
            urn="urn-1",
            user_urn="user-2",
            api_name="api-3",
            user_id="user-4"
        )
        assert mixin._urn == "urn-1"
        assert mixin._user_urn == "user-2"
        assert mixin._api_name == "api-3"
        assert mixin._user_id == "user-4"

    def test_init_with_kwargs(self):
        """Test initialization with kwargs."""
        mixin = ContextMixin(custom_key="custom_value", another_key=123)
        assert mixin._context["custom_key"] == "custom_value"
        assert mixin._context["another_key"] == 123

    def test_init_with_logger(self):
        """Test initialization with custom logger."""
        custom_logger = object()
        mixin = ContextMixin(logger=custom_logger)
        assert mixin._logger is custom_logger


class TestContextMixinProperties:
    """Tests for ContextMixin properties."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        mixin = ContextMixin(urn="test-urn")
        assert mixin.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        mixin = ContextMixin()
        mixin.urn = "new-urn"
        assert mixin.urn == "new-urn"
        assert mixin._urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        mixin = ContextMixin(user_urn="user-test")
        assert mixin.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        mixin = ContextMixin()
        mixin.user_urn = "new-user"
        assert mixin.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        mixin = ContextMixin(api_name="api-test")
        assert mixin.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        mixin = ContextMixin()
        mixin.api_name = "new-api"
        assert mixin.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        mixin = ContextMixin(user_id="id-test")
        assert mixin.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        mixin = ContextMixin()
        mixin.user_id = "new-id"
        assert mixin.user_id == "new-id"

    def test_logger_property_getter(self):
        """Test logger property getter."""
        mixin = ContextMixin()
        assert mixin.logger is not None

    def test_logger_property_setter(self):
        """Test logger property setter."""
        mixin = ContextMixin()
        new_logger = object()
        mixin.logger = new_logger
        assert mixin.logger is new_logger

    def test_context_property(self):
        """Test context property."""
        mixin = ContextMixin(custom="value")
        assert mixin.context == {"custom": "value"}


class TestContextMixinMethods:
    """Tests for ContextMixin methods."""

    def test_set_context(self):
        """Test set_context method."""
        mixin = ContextMixin()
        mixin.set_context(key1="value1", key2="value2")
        assert mixin._context["key1"] == "value1"
        assert mixin._context["key2"] == "value2"

    def test_set_context_updates_existing(self):
        """Test set_context updates existing keys."""
        mixin = ContextMixin(existing="old")
        mixin.set_context(existing="new")
        assert mixin._context["existing"] == "new"

    def test_get_context_existing_key(self):
        """Test get_context with existing key."""
        mixin = ContextMixin(key="value")
        assert mixin.get_context("key") == "value"

    def test_get_context_missing_key(self):
        """Test get_context with missing key."""
        mixin = ContextMixin()
        assert mixin.get_context("missing") is None

    def test_get_context_with_default(self):
        """Test get_context with default value."""
        mixin = ContextMixin()
        assert mixin.get_context("missing", "default") == "default"


class TestContextMixinEdgeCases:
    """Test edge cases for ContextMixin."""

    def test_empty_string_values(self):
        """Test empty string values."""
        mixin = ContextMixin(urn="", api_name="")
        assert mixin.urn == ""
        assert mixin.api_name == ""

    def test_unicode_values(self):
        """Test unicode values."""
        mixin = ContextMixin(urn="urn-测试", user_urn="用户-123")
        assert mixin.urn == "urn-测试"
        assert mixin.user_urn == "用户-123"

    def test_special_characters(self):
        """Test special characters."""
        special = "test<>!@#$%^&*()"
        mixin = ContextMixin(urn=special)
        assert mixin.urn == special

    def test_very_long_values(self):
        """Test very long values."""
        long_value = "x" * 10000
        mixin = ContextMixin(urn=long_value)
        assert mixin.urn == long_value

    def test_multiple_instances_independent(self):
        """Test multiple instances are independent."""
        mixin1 = ContextMixin(urn="urn1")
        mixin2 = ContextMixin(urn="urn2")
        assert mixin1.urn != mixin2.urn
        mixin1.urn = "updated"
        assert mixin1.urn == "updated"
        assert mixin2.urn == "urn2"

    def test_context_isolation(self):
        """Test context isolation between instances."""
        mixin1 = ContextMixin(key="value1")
        mixin2 = ContextMixin(key="value2")
        assert mixin1.get_context("key") == "value1"
        assert mixin2.get_context("key") == "value2"
