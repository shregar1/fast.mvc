"""Tests for log level constants."""

from __future__ import annotations

import pytest

from constants.log_level import LogLevelName


class TestLogLevelName:
    """Tests for LogLevelName class."""

    def test_debug(self):
        """Test DEBUG constant."""
        assert LogLevelName.DEBUG == "debug"

    def test_info(self):
        """Test INFO constant."""
        assert LogLevelName.INFO == "info"

    def test_warning(self):
        """Test WARNING constant."""
        assert LogLevelName.WARNING == "warning"

    def test_error(self):
        """Test ERROR constant."""
        assert LogLevelName.ERROR == "error"


class TestLogLevelNameTypes:
    """Tests for log level constant types."""

    def test_debug_is_string(self):
        """Test DEBUG is a string."""
        assert isinstance(LogLevelName.DEBUG, str)

    def test_info_is_string(self):
        """Test INFO is a string."""
        assert isinstance(LogLevelName.INFO, str)

    def test_warning_is_string(self):
        """Test WARNING is a string."""
        assert isinstance(LogLevelName.WARNING, str)

    def test_error_is_string(self):
        """Test ERROR is a string."""
        assert isinstance(LogLevelName.ERROR, str)


class TestLogLevelNameValues:
    """Tests for log level constant values."""

    def test_debug_is_lowercase(self):
        """Test DEBUG is lowercase."""
        assert LogLevelName.DEBUG.islower()

    def test_info_is_lowercase(self):
        """Test INFO is lowercase."""
        assert LogLevelName.INFO.islower()

    def test_warning_is_lowercase(self):
        """Test WARNING is lowercase."""
        assert LogLevelName.WARNING.islower()

    def test_error_is_lowercase(self):
        """Test ERROR is lowercase."""
        assert LogLevelName.ERROR.islower()


class TestLogLevelNameUniqueness:
    """Tests for log level constant uniqueness."""

    def test_all_levels_unique(self):
        """Test all log levels are unique."""
        levels = [
            LogLevelName.DEBUG,
            LogLevelName.INFO,
            LogLevelName.WARNING,
            LogLevelName.ERROR,
        ]
        assert len(levels) == len(set(levels))

    def test_no_duplicate_values(self):
        """Test no duplicate level values."""
        levels = {
            LogLevelName.DEBUG,
            LogLevelName.INFO,
            LogLevelName.WARNING,
            LogLevelName.ERROR,
        }
        assert len(levels) == 4
