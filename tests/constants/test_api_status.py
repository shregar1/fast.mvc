"""Tests for API status constants."""

from __future__ import annotations

import pytest

from constants.api_status import APIStatus


class TestAPIStatus:
    """Tests for APIStatus class."""

    def test_success(self):
        """Test SUCCESS constant."""
        assert APIStatus.SUCCESS == "SUCCESS"

    def test_failed(self):
        """Test FAILED constant."""
        assert APIStatus.FAILED == "FAILED"

    def test_pending(self):
        """Test PENDING constant."""
        assert APIStatus.PENDING == "PENDING"


class TestAPIStatusTypes:
    """Tests for API status constant types."""

    def test_success_is_string(self):
        """Test SUCCESS is a string."""
        assert isinstance(APIStatus.SUCCESS, str)

    def test_failed_is_string(self):
        """Test FAILED is a string."""
        assert isinstance(APIStatus.FAILED, str)

    def test_pending_is_string(self):
        """Test PENDING is a string."""
        assert isinstance(APIStatus.PENDING, str)


class TestAPIStatusValues:
    """Tests for API status constant values."""

    def test_success_is_uppercase(self):
        """Test SUCCESS is uppercase."""
        assert APIStatus.SUCCESS.isupper()

    def test_failed_is_uppercase(self):
        """Test FAILED is uppercase."""
        assert APIStatus.FAILED.isupper()

    def test_pending_is_uppercase(self):
        """Test PENDING is uppercase."""
        assert APIStatus.PENDING.isupper()


class TestAPIStatusUniqueness:
    """Tests for API status constant uniqueness."""

    def test_all_statuses_unique(self):
        """Test all API statuses are unique."""
        statuses = [
            APIStatus.SUCCESS,
            APIStatus.FAILED,
            APIStatus.PENDING,
        ]
        assert len(statuses) == len(set(statuses))

    def test_no_duplicate_values(self):
        """Test no duplicate status values."""
        statuses = {
            APIStatus.SUCCESS,
            APIStatus.FAILED,
            APIStatus.PENDING,
        }
        assert len(statuses) == 3
