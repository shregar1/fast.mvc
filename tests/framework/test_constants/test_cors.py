"""Tests for CORS constants."""

from __future__ import annotations

import pytest

from constants.cors import CorsEnvVar, CorsDefaults
from constants.http_method import HttpMethod
from constants.http_header import HttpHeader


class TestCorsEnvVar:
    """Tests for CorsEnvVar class."""

    def test_origins_env_var(self):
        """Test CORS_ORIGINS environment variable name."""
        assert CorsEnvVar.ORIGINS == "CORS_ORIGINS"

    def test_allowed_origins_env_var(self):
        """Test ALLOWED_ORIGINS environment variable name."""
        assert CorsEnvVar.ALLOWED_ORIGINS == "ALLOWED_ORIGINS"

    def test_allow_credentials_env_var(self):
        """Test CORS_ALLOW_CREDENTIALS environment variable name."""
        assert CorsEnvVar.ALLOW_CREDENTIALS == "CORS_ALLOW_CREDENTIALS"

    def test_allow_methods_env_var(self):
        """Test CORS_ALLOW_METHODS environment variable name."""
        assert CorsEnvVar.ALLOW_METHODS == "CORS_ALLOW_METHODS"

    def test_allow_headers_env_var(self):
        """Test CORS_ALLOW_HEADERS environment variable name."""
        assert CorsEnvVar.ALLOW_HEADERS == "CORS_ALLOW_HEADERS"

    def test_expose_headers_env_var(self):
        """Test CORS_EXPOSE_HEADERS environment variable name."""
        assert CorsEnvVar.EXPOSE_HEADERS == "CORS_EXPOSE_HEADERS"

    def test_allow_origin_regex_env_var(self):
        """Test CORS_ALLOW_ORIGIN_REGEX environment variable name."""
        assert CorsEnvVar.ALLOW_ORIGIN_REGEX == "CORS_ALLOW_ORIGIN_REGEX"

    def test_max_age_env_var(self):
        """Test CORS_MAX_AGE environment variable name."""
        assert CorsEnvVar.MAX_AGE == "CORS_MAX_AGE"


class TestCorsDefaults:
    """Tests for CorsDefaults class."""

    def test_wildcard(self):
        """Test WILDCARD constant."""
        assert CorsDefaults.WILDCARD == "*"

    def test_fallback_allow_origins(self):
        """Test FALLBACK_ALLOW_ORIGINS constant."""
        assert CorsDefaults.FALLBACK_ALLOW_ORIGINS == ("*",)

    def test_fallback_allow_headers(self):
        """Test FALLBACK_ALLOW_HEADERS constant."""
        assert CorsDefaults.FALLBACK_ALLOW_HEADERS == ("*",)

    def test_default_allow_credentials(self):
        """Test DEFAULT_ALLOW_CREDENTIALS constant."""
        assert CorsDefaults.DEFAULT_ALLOW_CREDENTIALS is True

    def test_default_max_age_seconds(self):
        """Test DEFAULT_MAX_AGE_SECONDS constant."""
        assert CorsDefaults.DEFAULT_MAX_AGE_SECONDS == 600

    def test_allow_methods(self):
        """Test ALLOW_METHODS constant."""
        expected_methods = (
            HttpMethod.GET,
            HttpMethod.POST,
            HttpMethod.PUT,
            HttpMethod.DELETE,
            HttpMethod.OPTIONS,
            HttpMethod.PATCH,
        )
        assert CorsDefaults.ALLOW_METHODS == expected_methods

    def test_allow_methods_contains_get(self):
        """Test ALLOW_METHODS contains GET."""
        assert HttpMethod.GET in CorsDefaults.ALLOW_METHODS

    def test_allow_methods_contains_post(self):
        """Test ALLOW_METHODS contains POST."""
        assert HttpMethod.POST in CorsDefaults.ALLOW_METHODS

    def test_allow_methods_contains_put(self):
        """Test ALLOW_METHODS contains PUT."""
        assert HttpMethod.PUT in CorsDefaults.ALLOW_METHODS

    def test_allow_methods_contains_delete(self):
        """Test ALLOW_METHODS contains DELETE."""
        assert HttpMethod.DELETE in CorsDefaults.ALLOW_METHODS

    def test_allow_methods_contains_options(self):
        """Test ALLOW_METHODS contains OPTIONS."""
        assert HttpMethod.OPTIONS in CorsDefaults.ALLOW_METHODS

    def test_allow_methods_contains_patch(self):
        """Test ALLOW_METHODS contains PATCH."""
        assert HttpMethod.PATCH in CorsDefaults.ALLOW_METHODS

    def test_expose_headers(self):
        """Test EXPOSE_HEADERS constant."""
        expected_headers = (
            HttpHeader.X_REQUEST_ID,
            HttpHeader.X_PROCESS_TIME,
            HttpHeader.X_TRANSACTION_URN,
            HttpHeader.X_REFERENCE_URN,
        )
        assert CorsDefaults.EXPOSE_HEADERS == expected_headers

    def test_cors_default_allow_methods_alias(self):
        """Test CORS_DEFAULT_ALLOW_METHODS is alias for ALLOW_METHODS."""
        assert CorsDefaults.CORS_DEFAULT_ALLOW_METHODS == CorsDefaults.ALLOW_METHODS

    def test_cors_default_expose_headers_alias(self):
        """Test CORS_DEFAULT_EXPOSE_HEADERS is alias for EXPOSE_HEADERS."""
        assert CorsDefaults.CORS_DEFAULT_EXPOSE_HEADERS == CorsDefaults.EXPOSE_HEADERS


class TestCorsConstantsTypes:
    """Tests for CORS constant types."""

    def test_wildcard_is_string(self):
        """Test WILDCARD is a string."""
        assert isinstance(CorsDefaults.WILDCARD, str)

    def test_fallback_allow_origins_is_tuple(self):
        """Test FALLBACK_ALLOW_ORIGINS is a tuple."""
        assert isinstance(CorsDefaults.FALLBACK_ALLOW_ORIGINS, tuple)

    def test_fallback_allow_headers_is_tuple(self):
        """Test FALLBACK_ALLOW_HEADERS is a tuple."""
        assert isinstance(CorsDefaults.FALLBACK_ALLOW_HEADERS, tuple)

    def test_default_allow_credentials_is_bool(self):
        """Test DEFAULT_ALLOW_CREDENTIALS is a bool."""
        assert isinstance(CorsDefaults.DEFAULT_ALLOW_CREDENTIALS, bool)

    def test_default_max_age_seconds_is_int(self):
        """Test DEFAULT_MAX_AGE_SECONDS is an int."""
        assert isinstance(CorsDefaults.DEFAULT_MAX_AGE_SECONDS, int)

    def test_allow_methods_is_tuple(self):
        """Test ALLOW_METHODS is a tuple."""
        assert isinstance(CorsDefaults.ALLOW_METHODS, tuple)

    def test_expose_headers_is_tuple(self):
        """Test EXPOSE_HEADERS is a tuple."""
        assert isinstance(CorsDefaults.EXPOSE_HEADERS, tuple)
