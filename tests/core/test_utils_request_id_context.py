"""Tests for core utils request_id_context module."""

from __future__ import annotations

import pytest
from contextvars import Token

from core.utils.request_id_context import RequestIdContext, _request_id_var


class TestRequestIdContext:
    """Tests for RequestIdContext class."""

    def test_get_returns_none_by_default(self):
        """Test get returns None by default."""
        result = RequestIdContext.get()
        assert result is None

    def test_set_and_get(self):
        """Test set and get."""
        token = RequestIdContext.set("req-123")
        try:
            result = RequestIdContext.get()
            assert result == "req-123"
        finally:
            RequestIdContext.reset(token)

    def test_set_returns_token(self):
        """Test set returns a Token."""
        token = RequestIdContext.set("req-123")
        try:
            assert isinstance(token, Token)
        finally:
            RequestIdContext.reset(token)

    def test_reset_restores_previous_value(self):
        """Test reset restores previous value."""
        # Set initial value
        token1 = RequestIdContext.set("req-1")
        try:
            assert RequestIdContext.get() == "req-1"
            
            # Set new value
            token2 = RequestIdContext.set("req-2")
            assert RequestIdContext.get() == "req-2"
            
            # Reset to previous
            RequestIdContext.reset(token2)
            assert RequestIdContext.get() == "req-1"
        finally:
            RequestIdContext.reset(token1)

    def test_set_none(self):
        """Test set with None."""
        token = RequestIdContext.set(None)
        try:
            result = RequestIdContext.get()
            assert result is None
        finally:
            RequestIdContext.reset(token)

    def test_set_empty_string(self):
        """Test set with empty string."""
        token = RequestIdContext.set("")
        try:
            result = RequestIdContext.get()
            assert result == ""
        finally:
            RequestIdContext.reset(token)

    def test_set_unicode(self):
        """Test set with unicode string."""
        token = RequestIdContext.set("请求-123")
        try:
            result = RequestIdContext.get()
            assert result == "请求-123"
        finally:
            RequestIdContext.reset(token)

    def test_set_special_characters(self):
        """Test set with special characters."""
        special = "req-<>!@#$%^&*()"
        token = RequestIdContext.set(special)
        try:
            result = RequestIdContext.get()
            assert result == special
        finally:
            RequestIdContext.reset(token)

    def test_set_long_string(self):
        """Test set with long string."""
        long_id = "x" * 1000
        token = RequestIdContext.set(long_id)
        try:
            result = RequestIdContext.get()
            assert result == long_id
        finally:
            RequestIdContext.reset(token)


class TestRequestIdVar:
    """Tests for _request_id_var context variable."""

    def test_request_id_var_exists(self):
        """Test _request_id_var exists."""
        assert _request_id_var is not None

    def test_request_id_var_default(self):
        """Test _request_id_var default value."""
        assert _request_id_var.get() is None

    def test_request_id_var_name(self):
        """Test _request_id_var name."""
        assert _request_id_var.name == "request_id"
