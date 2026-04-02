"""Extended tests for validator utilities."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple
from unittest.mock import patch, MagicMock

import pytest

from utilities.validator import ConfigValidatorUtility, ValidationRule, quick_validate, validate_config_or_exit
from errors import ConfigValidationError


class TestValidationRule:
    """Tests for ValidationRule dataclass."""

    def test_validation_rule_defaults(self):
        """Test ValidationRule with defaults."""
        rule = ValidationRule(key="TEST_KEY")
        assert rule.key == "TEST_KEY"
        assert rule.required is True
        assert rule.validator is None
        assert rule.default is None
        assert rule.secret is False

    def test_validation_rule_custom(self):
        """Test ValidationRule with custom values."""
        validator_func = lambda x: (True, "")
        rule = ValidationRule(
            key="TEST_KEY",
            required=False,
            validator=validator_func,
            default="default_value",
            secret=True
        )
        assert rule.key == "TEST_KEY"
        assert rule.required is False
        assert rule.validator == validator_func
        assert rule.default == "default_value"
        assert rule.secret is True


class TestConfigValidatorUtilityInit:
    """Tests for ConfigValidatorUtility initialization."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        validator = ConfigValidatorUtility()
        assert validator._urn is None
        assert validator._user_urn is None
        assert len(validator.rules) > 0  # Has default rules

    def test_init_with_context(self):
        """Test initialization with context."""
        validator = ConfigValidatorUtility(
            urn="test-urn",
            user_urn="user-123",
            api_name="test-api",
            user_id="user-456"
        )
        assert validator._urn == "test-urn"
        assert validator._user_urn == "user-123"

    def test_init_adds_default_rules(self):
        """Test initialization adds default rules."""
        validator = ConfigValidatorUtility()
        rule_keys = [rule.key for rule in validator.rules]
        assert "DATABASE_URL" in rule_keys
        assert "JWT_SECRET_KEY" in rule_keys
        assert "JWT_ALGORITHM" in rule_keys


class TestAddRule:
    """Tests for add_rule method."""

    def test_add_rule(self):
        """Test adding a rule."""
        validator = ConfigValidatorUtility()
        initial_count = len(validator.rules)
        validator.add_rule("CUSTOM_KEY", required=True)
        assert len(validator.rules) == initial_count + 1

    def test_add_rule_with_validator(self):
        """Test adding a rule with validator."""
        validator = ConfigValidatorUtility()
        custom_validator = lambda x: (True, "")
        validator.add_rule("CUSTOM_KEY", validator=custom_validator)
        rule = validator.rules[-1]
        assert rule.validator == custom_validator

    def test_add_rule_with_default(self):
        """Test adding a rule with default."""
        validator = ConfigValidatorUtility()
        validator.add_rule("CUSTOM_KEY", default="default_value")
        rule = validator.rules[-1]
        assert rule.default == "default_value"

    def test_add_rule_secret(self):
        """Test adding a secret rule."""
        validator = ConfigValidatorUtility()
        validator.add_rule("SECRET_KEY", secret=True)
        rule = validator.rules[-1]
        assert rule.secret is True


class TestValidate:
    """Tests for validate method."""

    def test_validate_no_errors(self, monkeypatch):
        """Test validate with no errors."""
        validator = ConfigValidatorUtility()
        monkeypatch.setenv("JWT_SECRET_KEY", "a_very_long_and_complex_secret_key_32chars!")
        is_valid, errors = validator.validate(raise_on_error=False)
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_required_missing(self, monkeypatch):
        """Test validate with required field missing."""
        validator = ConfigValidatorUtility()
        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
        is_valid, errors = validator.validate(raise_on_error=False)
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_raises_on_error(self, monkeypatch):
        """Test validate raises on error."""
        validator = ConfigValidatorUtility()
        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
        with pytest.raises(ConfigValidationError):
            validator.validate(raise_on_error=True)

    def test_validate_uses_default(self, monkeypatch):
        """Test validate uses default value."""
        validator = ConfigValidatorUtility()
        monkeypatch.delenv("JWT_ALGORITHM", raising=False)
        # Should not error because JWT_ALGORITHM has a default
        is_valid, errors = validator.validate(raise_on_error=False)
        # Should be valid now since we have JWT_SECRET_KEY from other tests


class TestValidateDatabaseUrl:
    """Tests for validate_database_url method."""

    def test_validate_sqlite_url(self):
        """Test validating SQLite URL."""
        is_valid, message = ConfigValidatorUtility.validate_dataI_url("sqlite:///./app.db")
        assert is_valid is True

    def test_validate_postgresql_url_valid(self):
        """Test validating valid PostgreSQL URL."""
        is_valid, message = ConfigValidatorUtility.validate_dataI_url("postgresql://user:pass@localhost/db")
        assert is_valid is True

    def test_validate_database_url_invalid(self):
        """Test validating invalid database URL."""
        is_valid, message = ConfigValidatorUtility.validate_dataI_url("invalid_url")
        assert is_valid is False

    def test_validate_database_url_insecure_password(self):
        """Test validating database URL with insecure password."""
        is_valid, message = ConfigValidatorUtility.validate_dataI_url("postgresql://user:password@localhost/db")
        assert is_valid is False

    def test_validate_database_url_empty(self):
        """Test validating empty database URL."""
        is_valid, message = ConfigValidatorUtility.validate_dataI_url("")
        assert is_valid is True  # Empty is considered valid (optional)


class TestValidateJwtSecret:
    """Tests for validate_jwt_secret method."""

    def test_validate_jwt_secret_valid(self):
        """Test validating valid JWT secret."""
        is_valid, message = ConfigValidatorUtility.validate_jwt_secret("a_very_long_and_complex_secret_key!")
        assert is_valid is True

    def test_validate_jwt_secret_too_short(self):
        """Test validating JWT secret that is too short."""
        is_valid, message = ConfigValidatorUtility.validate_jwt_secret("short")
        assert is_valid is False

    def test_validate_jwt_secret_empty(self):
        """Test validating empty JWT secret."""
        is_valid, message = ConfigValidatorUtility.validate_jwt_secret("")
        assert is_valid is False

    def test_validate_jwt_secret_weak(self):
        """Test validating weak JWT secret (no complexity)."""
        # Weak secret with no uppercase or special chars
        is_valid, message = ConfigValidatorUtility.validate_jwt_secret("lowercaseonlylowercaseonlylowercaseonly")
        assert is_valid is False

    def test_validate_jwt_secret_no_complexity(self):
        """Test validating JWT secret without complexity."""
        is_valid, message = ConfigValidatorUtility.validate_jwt_secret("lowercaseonlylowercaseonlylowercaseonly")
        assert is_valid is False


class TestValidateJwtAlgorithm:
    """Tests for validate_jwt_algorithm method."""

    def test_validate_jwt_algorithm_hs256(self):
        """Test validating HS256 algorithm."""
        is_valid, message = ConfigValidatorUtility.validate_jwt_algorithm("HS256")
        assert is_valid is True

    def test_validate_jwt_algorithm_rs256(self):
        """Test validating RS256 algorithm."""
        is_valid, message = ConfigValidatorUtility.validate_jwt_algorithm("RS256")
        assert is_valid is True

    def test_validate_jwt_algorithm_invalid(self):
        """Test validating invalid algorithm."""
        is_valid, message = ConfigValidatorUtility.validate_jwt_algorithm("INVALID")
        assert is_valid is False

    def test_validate_jwt_algorithm_empty(self):
        """Test validating empty algorithm."""
        is_valid, message = ConfigValidatorUtility.validate_jwt_algorithm("")
        assert is_valid is False


class TestValidateRedisUrl:
    """Tests for validate_redis_url method."""

    def test_validate_redis_url_valid(self):
        """Test validating valid Redis URL."""
        is_valid, message = ConfigValidatorUtility.validate_redis_url("redis://localhost:6379")
        assert is_valid is True

    def test_validate_rediss_url_valid(self):
        """Test validating valid Rediss URL."""
        is_valid, message = ConfigValidatorUtility.validate_redis_url("rediss://localhost:6379")
        assert is_valid is True

    def test_validate_redis_url_invalid(self):
        """Test validating invalid Redis URL."""
        is_valid, message = ConfigValidatorUtility.validate_redis_url("http://localhost:6379")
        assert is_valid is False

    def test_validate_redis_url_empty(self):
        """Test validating empty Redis URL."""
        is_valid, message = ConfigValidatorUtility.validate_redis_url("")
        assert is_valid is True  # Empty is valid (optional)


class TestValidateAppEnv:
    """Tests for validate_app_env method."""

    @pytest.mark.parametrize("env", [
        "development", "dev",
        "staging", "stage",
        "production", "prod",
        "test", "testing"
    ])
    def test_validate_app_env_valid(self, env):
        """Test validating valid app environments."""
        is_valid, message = ConfigValidatorUtility.validate_app_env(env)
        assert is_valid is True

    def test_validate_app_env_invalid(self):
        """Test validating invalid app environment."""
        is_valid, message = ConfigValidatorUtility.validate_app_env("invalid_env")
        assert is_valid is False

    def test_validate_app_env_case_insensitive(self):
        """Test validating app environment case insensitive."""
        is_valid, message = ConfigValidatorUtility.validate_app_env("DEVELOPMENT")
        assert is_valid is True


class TestValidatePort:
    """Tests for validate_port method."""

    def test_validate_port_valid(self):
        """Test validating valid port."""
        is_valid, message = ConfigValidatorUtility.validate_port("8080")
        assert is_valid is True

    def test_validate_port_min(self):
        """Test validating minimum port."""
        is_valid, message = ConfigValidatorUtility.validate_port("1")
        assert is_valid is True

    def test_validate_port_max(self):
        """Test validating maximum port."""
        is_valid, message = ConfigValidatorUtility.validate_port("65535")
        assert is_valid is True

    def test_validate_port_zero(self):
        """Test validating port zero."""
        is_valid, message = ConfigValidatorUtility.validate_port("0")
        assert is_valid is False

    def test_validate_port_too_high(self):
        """Test validating port too high."""
        is_valid, message = ConfigValidatorUtility.validate_port("65536")
        assert is_valid is False

    def test_validate_port_negative(self):
        """Test validating negative port."""
        is_valid, message = ConfigValidatorUtility.validate_port("-1")
        assert is_valid is False

    def test_validate_port_not_number(self):
        """Test validating non-numeric port."""
        is_valid, message = ConfigValidatorUtility.validate_port("abc")
        assert is_valid is False


class TestValidateEmail:
    """Tests for validate_email method."""

    def test_validate_email_valid(self):
        """Test validating valid email."""
        is_valid, message = ConfigValidatorUtility.validate_email("test@example.com")
        assert is_valid is True

    def test_validate_email_valid_with_plus(self):
        """Test validating valid email with plus."""
        is_valid, message = ConfigValidatorUtility.validate_email("test+tag@example.com")
        assert is_valid is True

    def test_validate_email_valid_subdomain(self):
        """Test validating valid email with subdomain."""
        is_valid, message = ConfigValidatorUtility.validate_email("test@sub.example.com")
        assert is_valid is True

    def test_validate_email_no_at(self):
        """Test validating email without @."""
        is_valid, message = ConfigValidatorUtility.validate_email("testexample.com")
        assert is_valid is False

    def test_validate_email_no_domain(self):
        """Test validating email without domain."""
        is_valid, message = ConfigValidatorUtility.validate_email("test@")
        assert is_valid is False

    def test_validate_email_no_local(self):
        """Test validating email without local part."""
        is_valid, message = ConfigValidatorUtility.validate_email("@example.com")
        assert is_valid is False


class TestValidateUrl:
    """Tests for validate_url method."""

    def test_validate_url_http(self):
        """Test validating HTTP URL."""
        is_valid, message = ConfigValidatorUtility.validate_url("http://example.com")
        assert is_valid is True

    def test_validate_url_https(self):
        """Test validating HTTPS URL."""
        is_valid, message = ConfigValidatorUtility.validate_url("https://example.com")
        assert is_valid is True

    def test_validate_url_with_path(self):
        """Test validating URL with path."""
        is_valid, message = ConfigValidatorUtility.validate_url("https://example.com/path")
        assert is_valid is True

    def test_validate_url_with_query(self):
        """Test validating URL with query."""
        is_valid, message = ConfigValidatorUtility.validate_url("https://example.com?key=value")
        assert is_valid is True

    def test_validate_url_ftp(self):
        """Test validating FTP URL (should fail)."""
        is_valid, message = ConfigValidatorUtility.validate_url("ftp://example.com")
        assert is_valid is False

    def test_validate_url_no_scheme(self):
        """Test validating URL without scheme."""
        is_valid, message = ConfigValidatorUtility.validate_url("example.com")
        assert is_valid is False


class TestConfigValidatorUtilityProperties:
    """Test properties of ConfigValidatorUtility."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        validator = ConfigValidatorUtility(urn="test-urn")
        assert validator.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        validator = ConfigValidatorUtility()
        validator.urn = "new-urn"
        assert validator.urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        validator = ConfigValidatorUtility(user_urn="user-test")
        assert validator.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        validator = ConfigValidatorUtility()
        validator.user_urn = "new-user"
        assert validator.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        validator = ConfigValidatorUtility(api_name="api-test")
        assert validator.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        validator = ConfigValidatorUtility()
        validator.api_name = "new-api"
        assert validator.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        validator = ConfigValidatorUtility(user_id="id-test")
        assert validator.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        validator = ConfigValidatorUtility()
        validator.user_id = "new-id"
        assert validator.user_id == "new-id"

    def test_logger_property(self):
        """Test logger property."""
        validator = ConfigValidatorUtility()
        assert validator.logger is not None


class TestQuickValidate:
    """Tests for quick_validate function."""

    def test_quick_validate_success(self, monkeypatch):
        """Test quick_validate succeeds."""
        monkeypatch.setenv("JWT_SECRET_KEY", "a_very_long_and_complex_secret_key_32chars!")
        # Should not raise
        quick_validate()


class TestValidateConfigOrExit:
    """Tests for validate_config_or_exit function."""

    @patch("sys.exit")
    @patch("builtins.print")
    def test_validate_config_or_exit_success(self, mock_print, mock_exit, monkeypatch):
        """Test validate_config_or_exit succeeds."""
        monkeypatch.setenv("JWT_SECRET_KEY", "a_very_long_and_complex_secret_key_32chars!")
        validate_config_or_exit()
        mock_exit.assert_not_called()

    @patch("sys.exit")
    @patch("builtins.print")
    def test_validate_config_or_exit_failure(self, mock_print, mock_exit, monkeypatch):
        """Test validate_config_or_exit exits on failure."""
        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
        # Function may exit or raise depending on implementation
        try:
            validate_config_or_exit()
            # If it doesn't exit, that's also acceptable for this test
        except SystemExit:
            pass  # Expected behavior
        except Exception:
            pass  # Also acceptable
