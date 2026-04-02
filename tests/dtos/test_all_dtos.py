"""Comprehensive tests for all DTOs."""

from __future__ import annotations

import pytest
from typing import Any, Optional


class TestDTOImports:
    """Test that all DTOs can be imported."""

    def test_import_cors_settings_dto(self):
        """Test CorsSettingsDTO can be imported."""
        from dtos.configuration.cors import CorsSettingsDTO
        assert CorsSettingsDTO is not None

    def test_import_security_headers_settings_dto(self):
        """Test SecurityHeadersSettingsDTO can be imported."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        assert SecurityHeadersSettingsDTO is not None

    def test_import_i_configuration_dto(self):
        """Test IConfigurationDTO can be imported."""
        from dtos.configuration.abstraction import IConfigurationDTO
        assert IConfigurationDTO is not None


class TestDTOInheritance:
    """Test that all DTOs have proper inheritance."""

    def test_cors_settings_dto_inheritance(self):
        """Test CorsSettingsDTO inheritance."""
        from dtos.configuration.cors import CorsSettingsDTO
        from dtos.configuration.abstraction import IConfigurationDTO
        assert issubclass(CorsSettingsDTO, IConfigurationDTO)

    def test_security_headers_settings_dto_inheritance(self):
        """Test SecurityHeadersSettingsDTO inheritance."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        from dtos.configuration.abstraction import IConfigurationDTO
        assert issubclass(SecurityHeadersSettingsDTO, IConfigurationDTO)


class TestDTOInstantiation:
    """Test that all DTOs can be instantiated."""

    def test_cors_settings_dto_instantiation(self):
        """Test CorsSettingsDTO can be instantiated."""
        from dtos.configuration.cors import CorsSettingsDTO
        dto = CorsSettingsDTO()
        assert dto is not None

    def test_security_headers_settings_dto_instantiation(self):
        """Test SecurityHeadersSettingsDTO can be instantiated."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        dto = SecurityHeadersSettingsDTO()
        assert dto is not None


class TestDTOFields:
    """Test that DTOs have expected fields."""

    def test_cors_settings_dto_fields(self):
        """Test CorsSettingsDTO has expected fields."""
        from dtos.configuration.cors import CorsSettingsDTO
        dto = CorsSettingsDTO()
        assert hasattr(dto, "allow_origins")
        assert hasattr(dto, "allow_credentials")
        assert hasattr(dto, "allow_methods")
        assert hasattr(dto, "allow_headers")
        assert hasattr(dto, "expose_headers")
        assert hasattr(dto, "max_age")

    def test_security_headers_settings_dto_fields(self):
        """Test SecurityHeadersSettingsDTO has expected fields."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        dto = SecurityHeadersSettingsDTO()
        assert hasattr(dto, "x_content_type_options")
        assert hasattr(dto, "x_frame_options")
        assert hasattr(dto, "x_xss_protection")
        assert hasattr(dto, "referrer_policy")
        assert hasattr(dto, "enable_hsts")
        assert hasattr(dto, "hsts_max_age")


class TestDTODefaults:
    """Test that DTOs have correct defaults."""

    def test_cors_settings_dto_defaults(self):
        """Test CorsSettingsDTO has correct defaults."""
        from dtos.configuration.cors import CorsSettingsDTO
        dto = CorsSettingsDTO()
        assert dto.allow_credentials is True
        assert dto.max_age == 600

    def test_security_headers_settings_dto_defaults(self):
        """Test SecurityHeadersSettingsDTO has correct defaults."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        dto = SecurityHeadersSettingsDTO()
        assert dto.x_content_type_options == "nosniff"
        assert dto.x_frame_options == "DENY"
        assert dto.enable_hsts is True
        assert dto.hsts_max_age == 31_536_000


class TestDTOMethods:
    """Test that DTOs have expected methods."""

    def test_cors_settings_dto_to_middleware_kwargs(self):
        """Test CorsSettingsDTO has to_middleware_kwargs method."""
        from dtos.configuration.cors import CorsSettingsDTO
        dto = CorsSettingsDTO()
        assert hasattr(dto, "to_middleware_kwargs")
        assert callable(dto.to_middleware_kwargs)

    def test_security_headers_settings_dto_to_middleware_config(self):
        """Test SecurityHeadersSettingsDTO has to_middleware_config method."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        dto = SecurityHeadersSettingsDTO()
        assert hasattr(dto, "to_middleware_config")
        assert callable(dto.to_middleware_config)


class TestCorsSettingsDTOValidation:
    """Test CorsSettingsDTO validation."""

    def test_cors_settings_dto_max_age_validation(self):
        """Test CorsSettingsDTO max_age validation."""
        from dtos.configuration.cors import CorsSettingsDTO
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            CorsSettingsDTO(max_age=-1)

    def test_cors_settings_dto_max_age_zero_valid(self):
        """Test CorsSettingsDTO max_age zero is valid."""
        from dtos.configuration.cors import CorsSettingsDTO
        dto = CorsSettingsDTO(max_age=0)
        assert dto.max_age == 0


class TestSecurityHeadersSettingsDTOValidation:
    """Test SecurityHeadersSettingsDTO validation."""

    def test_security_headers_settings_dto_hsts_max_age_validation(self):
        """Test SecurityHeadersSettingsDTO hsts_max_age validation."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            SecurityHeadersSettingsDTO(hsts_max_age=-1)

    def test_security_headers_settings_dto_hsts_max_age_zero_valid(self):
        """Test SecurityHeadersSettingsDTO hsts_max_age zero is valid."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        dto = SecurityHeadersSettingsDTO(hsts_max_age=0)
        assert dto.hsts_max_age == 0


class TestDTOCustomValues:
    """Test DTOs with custom values."""

    def test_cors_settings_dto_custom_origins(self):
        """Test CorsSettingsDTO with custom origins."""
        from dtos.configuration.cors import CorsSettingsDTO
        dto = CorsSettingsDTO(allow_origins=["http://localhost:3000"])
        assert dto.allow_origins == ["http://localhost:3000"]

    def test_cors_settings_dto_custom_credentials(self):
        """Test CorsSettingsDTO with custom credentials."""
        from dtos.configuration.cors import CorsSettingsDTO
        dto = CorsSettingsDTO(allow_credentials=False)
        assert dto.allow_credentials is False

    def test_security_headers_settings_dto_custom_frame_options(self):
        """Test SecurityHeadersSettingsDTO with custom frame options."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        dto = SecurityHeadersSettingsDTO(x_frame_options="SAMEORIGIN")
        assert dto.x_frame_options == "SAMEORIGIN"

    def test_security_headers_settings_dto_custom_csp(self):
        """Test SecurityHeadersSettingsDTO with custom CSP."""
        from dtos.configuration.security_headers import SecurityHeadersSettingsDTO
        csp = "default-src 'self'"
        dto = SecurityHeadersSettingsDTO(content_security_policy=csp)
        assert dto.content_security_policy == csp
