"""Tests for HTTP method constants."""

from __future__ import annotations

import pytest

from constants.http_method import HttpMethod


class TestHttpMethod:
    """Tests for HttpMethod class."""

    def test_get(self):
        """Test GET method constant."""
        assert HttpMethod.GET == "GET"

    def test_post(self):
        """Test POST method constant."""
        assert HttpMethod.POST == "POST"

    def test_put(self):
        """Test PUT method constant."""
        assert HttpMethod.PUT == "PUT"

    def test_delete(self):
        """Test DELETE method constant."""
        assert HttpMethod.DELETE == "DELETE"

    def test_options(self):
        """Test OPTIONS method constant."""
        assert HttpMethod.OPTIONS == "OPTIONS"

    def test_patch(self):
        """Test PATCH method constant."""
        assert HttpMethod.PATCH == "PATCH"


class TestHttpMethodTypes:
    """Tests for HTTP method constant types."""

    def test_get_is_string(self):
        """Test GET is a string."""
        assert isinstance(HttpMethod.GET, str)

    def test_post_is_string(self):
        """Test POST is a string."""
        assert isinstance(HttpMethod.POST, str)

    def test_put_is_string(self):
        """Test PUT is a string."""
        assert isinstance(HttpMethod.PUT, str)

    def test_delete_is_string(self):
        """Test DELETE is a string."""
        assert isinstance(HttpMethod.DELETE, str)

    def test_options_is_string(self):
        """Test OPTIONS is a string."""
        assert isinstance(HttpMethod.OPTIONS, str)

    def test_patch_is_string(self):
        """Test PATCH is a string."""
        assert isinstance(HttpMethod.PATCH, str)


class TestHttpMethodValues:
    """Tests for HTTP method constant values."""

    def test_get_value(self):
        """Test GET value is uppercase."""
        assert HttpMethod.GET.isupper()

    def test_post_value(self):
        """Test POST value is uppercase."""
        assert HttpMethod.POST.isupper()

    def test_put_value(self):
        """Test PUT value is uppercase."""
        assert HttpMethod.PUT.isupper()

    def test_delete_value(self):
        """Test DELETE value is uppercase."""
        assert HttpMethod.DELETE.isupper()

    def test_options_value(self):
        """Test OPTIONS value is uppercase."""
        assert HttpMethod.OPTIONS.isupper()

    def test_patch_value(self):
        """Test PATCH value is uppercase."""
        assert HttpMethod.PATCH.isupper()


class TestHttpMethodUniqueness:
    """Tests for HTTP method constant uniqueness."""

    def test_all_methods_unique(self):
        """Test all HTTP methods are unique."""
        methods = [
            HttpMethod.GET,
            HttpMethod.POST,
            HttpMethod.PUT,
            HttpMethod.DELETE,
            HttpMethod.OPTIONS,
            HttpMethod.PATCH,
        ]
        assert len(methods) == len(set(methods))

    def test_no_duplicate_values(self):
        """Test no duplicate method values."""
        methods = {
            HttpMethod.GET,
            HttpMethod.POST,
            HttpMethod.PUT,
            HttpMethod.DELETE,
            HttpMethod.OPTIONS,
            HttpMethod.PATCH,
        }
        assert len(methods) == 6
