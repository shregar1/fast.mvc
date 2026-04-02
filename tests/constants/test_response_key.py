"""Tests for response key constants."""

from __future__ import annotations

import pytest

from constants.response_key import ResponseKey


class TestResponseKey:
    """Tests for ResponseKey class."""

    def test_error_internal_server_error(self):
        """Test ERROR_INTERNAL_SERVER_ERROR constant."""
        assert ResponseKey.ERROR_INTERNAL_SERVER_ERROR == "error_internal_server_error"

    def test_success_health(self):
        """Test SUCCESS_HEALTH constant."""
        assert ResponseKey.SUCCESS_HEALTH == "success_health"

    def test_error_health_unhealthy(self):
        """Test ERROR_HEALTH_UNHEALTHY constant."""
        assert ResponseKey.ERROR_HEALTH_UNHEALTHY == "error_health_unhealthy"

    def test_success_health_live(self):
        """Test SUCCESS_HEALTH_LIVE constant."""
        assert ResponseKey.SUCCESS_HEALTH_LIVE == "success_health_live"

    def test_success_health_ready(self):
        """Test SUCCESS_HEALTH_READY constant."""
        assert ResponseKey.SUCCESS_HEALTH_READY == "success_health_ready"

    def test_error_health_not_ready(self):
        """Test ERROR_HEALTH_NOT_READY constant."""
        assert ResponseKey.ERROR_HEALTH_NOT_READY == "error_health_not_ready"


class TestResponseKeyTypes:
    """Tests for response key constant types."""

    def test_error_internal_server_error_is_string(self):
        """Test ERROR_INTERNAL_SERVER_ERROR is a string."""
        assert isinstance(ResponseKey.ERROR_INTERNAL_SERVER_ERROR, str)

    def test_success_health_is_string(self):
        """Test SUCCESS_HEALTH is a string."""
        assert isinstance(ResponseKey.SUCCESS_HEALTH, str)

    def test_error_health_unhealthy_is_string(self):
        """Test ERROR_HEALTH_UNHEALTHY is a string."""
        assert isinstance(ResponseKey.ERROR_HEALTH_UNHEALTHY, str)

    def test_success_health_live_is_string(self):
        """Test SUCCESS_HEALTH_LIVE is a string."""
        assert isinstance(ResponseKey.SUCCESS_HEALTH_LIVE, str)

    def test_success_health_ready_is_string(self):
        """Test SUCCESS_HEALTH_READY is a string."""
        assert isinstance(ResponseKey.SUCCESS_HEALTH_READY, str)

    def test_error_health_not_ready_is_string(self):
        """Test ERROR_HEALTH_NOT_READY is a string."""
        assert isinstance(ResponseKey.ERROR_HEALTH_NOT_READY, str)


class TestResponseKeyValues:
    """Tests for response key constant values."""

    def test_all_keys_start_with_success_or_error(self):
        """Test all keys start with 'success' or 'error'."""
        keys = [
            ResponseKey.ERROR_INTERNAL_SERVER_ERROR,
            ResponseKey.SUCCESS_HEALTH,
            ResponseKey.ERROR_HEALTH_UNHEALTHY,
            ResponseKey.SUCCESS_HEALTH_LIVE,
            ResponseKey.SUCCESS_HEALTH_READY,
            ResponseKey.ERROR_HEALTH_NOT_READY,
        ]
        for key in keys:
            assert key.startswith("success_") or key.startswith("error_")

    def test_all_keys_use_snake_case(self):
        """Test all keys use snake_case."""
        keys = [
            ResponseKey.ERROR_INTERNAL_SERVER_ERROR,
            ResponseKey.SUCCESS_HEALTH,
            ResponseKey.ERROR_HEALTH_UNHEALTHY,
            ResponseKey.SUCCESS_HEALTH_LIVE,
            ResponseKey.SUCCESS_HEALTH_READY,
            ResponseKey.ERROR_HEALTH_NOT_READY,
        ]
        for key in keys:
            assert "_" in key
            assert key == key.lower()

    def test_error_keys_contain_error(self):
        """Test error keys contain 'error'."""
        error_keys = [
            ResponseKey.ERROR_INTERNAL_SERVER_ERROR,
            ResponseKey.ERROR_HEALTH_UNHEALTHY,
            ResponseKey.ERROR_HEALTH_NOT_READY,
        ]
        for key in error_keys:
            assert "error" in key

    def test_success_keys_contain_success(self):
        """Test success keys contain 'success'."""
        success_keys = [
            ResponseKey.SUCCESS_HEALTH,
            ResponseKey.SUCCESS_HEALTH_LIVE,
            ResponseKey.SUCCESS_HEALTH_READY,
        ]
        for key in success_keys:
            assert "success" in key


class TestResponseKeyUniqueness:
    """Tests for response key constant uniqueness."""

    def test_all_keys_unique(self):
        """Test all response keys are unique."""
        keys = [
            ResponseKey.ERROR_INTERNAL_SERVER_ERROR,
            ResponseKey.SUCCESS_HEALTH,
            ResponseKey.ERROR_HEALTH_UNHEALTHY,
            ResponseKey.SUCCESS_HEALTH_LIVE,
            ResponseKey.SUCCESS_HEALTH_READY,
            ResponseKey.ERROR_HEALTH_NOT_READY,
        ]
        assert len(keys) == len(set(keys))
