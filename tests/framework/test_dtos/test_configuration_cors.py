"""Tests for CORS configuration DTO."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from dtos.configuration.cors import CorsSettingsDTO


class TestCorsSettingsDTO:
    """Tests for CorsSettingsDTO."""

    def test_default_creation(self):
        """Test creating with default values."""
        dto = CorsSettingsDTO()
        assert dto is not None

    def test_allow_origins_default(self):
        """Test allow_origins default value."""
        dto = CorsSettingsDTO()
        assert "*" in dto.allow_origins

    def test_allow_credentials_default(self):
        """Test allow_credentials default value."""
        dto = CorsSettingsDTO()
        assert dto.allow_credentials is True

    def test_allow_methods_default(self):
        """Test allow_methods default value."""
        dto = CorsSettingsDTO()
        assert "GET" in dto.allow_methods
        assert "POST" in dto.allow_methods

    def test_allow_headers_default(self):
        """Test allow_headers default value."""
        dto = CorsSettingsDTO()
        assert "*" in dto.allow_headers

    def test_expose_headers_default(self):
        """Test expose_headers default value."""
        dto = CorsSettingsDTO()
        assert isinstance(dto.expose_headers, list)

    def test_allow_origin_regex_default(self):
        """Test allow_origin_regex default value."""
        dto = CorsSettingsDTO()
        assert dto.allow_origin_regex is None

    def test_max_age_default(self):
        """Test max_age default value."""
        dto = CorsSettingsDTO()
        assert dto.max_age == 600


class TestCorsSettingsDTOCustomValues:
    """Tests for CorsSettingsDTO with custom values."""

    def test_custom_allow_origins(self):
        """Test setting custom allow_origins."""
        dto = CorsSettingsDTO(allow_origins=["http://localhost:3000"])
        assert dto.allow_origins == ["http://localhost:3000"]

    def test_custom_allow_credentials(self):
        """Test setting custom allow_credentials."""
        dto = CorsSettingsDTO(allow_credentials=False)
        assert dto.allow_credentials is False

    def test_custom_allow_methods(self):
        """Test setting custom allow_methods."""
        dto = CorsSettingsDTO(allow_methods=["GET", "POST"])
        assert dto.allow_methods == ["GET", "POST"]

    def test_custom_allow_headers(self):
        """Test setting custom allow_headers."""
        dto = CorsSettingsDTO(allow_headers=["Content-Type", "Authorization"])
        assert dto.allow_headers == ["Content-Type", "Authorization"]

    def test_custom_expose_headers(self):
        """Test setting custom expose_headers."""
        dto = CorsSettingsDTO(expose_headers=["X-Custom-Header"])
        assert dto.expose_headers == ["X-Custom-Header"]

    def test_custom_allow_origin_regex(self):
        """Test setting custom allow_origin_regex."""
        dto = CorsSettingsDTO(allow_origin_regex="https://.*\\.example\\.com")
        assert dto.allow_origin_regex == "https://.*\\.example\\.com"

    def test_custom_max_age(self):
        """Test setting custom max_age."""
        dto = CorsSettingsDTO(max_age=3600)
        assert dto.max_age == 3600


class TestCorsSettingsDTOValidation:
    """Tests for CorsSettingsDTO validation."""

    def test_max_age_negative(self):
        """Test max_age cannot be negative."""
        with pytest.raises(ValidationError):
            CorsSettingsDTO(max_age=-1)

    def test_max_age_zero(self):
        """Test max_age can be zero."""
        dto = CorsSettingsDTO(max_age=0)
        assert dto.max_age == 0


class TestCorsSettingsDTOMiddlewareKwargs:
    """Tests for to_middleware_kwargs method."""

    def test_to_middleware_kwargs_returns_dict(self):
        """Test to_middleware_kwargs returns dict."""
        dto = CorsSettingsDTO()
        result = dto.to_middleware_kwargs()
        assert isinstance(result, dict)

    def test_to_middleware_kwargs_has_allow_origins(self):
        """Test to_middleware_kwargs has allow_origins."""
        dto = CorsSettingsDTO()
        result = dto.to_middleware_kwargs()
        assert "allow_origins" in result

    def test_to_middleware_kwargs_has_allow_credentials(self):
        """Test to_middleware_kwargs has allow_credentials."""
        dto = CorsSettingsDTO()
        result = dto.to_middleware_kwargs()
        assert "allow_credentials" in result

    def test_to_middleware_kwargs_has_allow_methods(self):
        """Test to_middleware_kwargs has allow_methods."""
        dto = CorsSettingsDTO()
        result = dto.to_middleware_kwargs()
        assert "allow_methods" in result

    def test_to_middleware_kwargs_has_allow_headers(self):
        """Test to_middleware_kwargs has allow_headers."""
        dto = CorsSettingsDTO()
        result = dto.to_middleware_kwargs()
        assert "allow_headers" in result

    def test_to_middleware_kwargs_has_expose_headers(self):
        """Test to_middleware_kwargs has expose_headers."""
        dto = CorsSettingsDTO()
        result = dto.to_middleware_kwargs()
        assert "expose_headers" in result

    def test_to_middleware_kwargs_has_max_age(self):
        """Test to_middleware_kwargs has max_age."""
        dto = CorsSettingsDTO()
        result = dto.to_middleware_kwargs()
        assert "max_age" in result

    def test_to_middleware_kwargs_with_regex(self):
        """Test to_middleware_kwargs includes regex when set."""
        dto = CorsSettingsDTO(allow_origin_regex="https://.*\\.example\\.com")
        result = dto.to_middleware_kwargs()
        assert "allow_origin_regex" in result

    def test_to_middleware_kwargs_without_regex(self):
        """Test to_middleware_kwargs excludes regex when not set."""
        dto = CorsSettingsDTO(allow_origin_regex=None)
        result = dto.to_middleware_kwargs()
        assert "allow_origin_regex" not in result
