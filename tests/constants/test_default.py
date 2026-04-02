"""Tests for default constants."""

from __future__ import annotations

import pytest

from constants.default import (
    ApplicationDefault,
    JwtDefault,
    RateLimitDefault,
    AuthenticationDefault,
    RateLimitingDefault,
    SecurityHeadersDefault,
    InputValidationDefault,
    CorsSectionDefault,
    Default,
)


class TestApplicationDefault:
    """Tests for ApplicationDefault class."""

    def test_app_name(self):
        """Test APP_NAME constant."""
        assert ApplicationDefault.APP_NAME == "FastMVC"

    def test_app_version(self):
        """Test APP_VERSION constant."""
        assert ApplicationDefault.APP_VERSION == "1.0.1"

    def test_debug(self):
        """Test DEBUG constant."""
        assert ApplicationDefault.DEBUG is False

    def test_log_level(self):
        """Test LOG_LEVEL constant."""
        assert ApplicationDefault.LOG_LEVEL == "INFO"

    def test_channel_backend(self):
        """Test CHANNEL_BACKEND constant."""
        assert ApplicationDefault.CHANNEL_BACKEND == "redis"

    def test_allow_origin_regex(self):
        """Test ALLOW_ORIGIN_REGEX constant."""
        assert ApplicationDefault.ALLOW_ORIGIN_REGEX == ""


class TestJwtDefault:
    """Tests for JwtDefault class."""

    def test_algorithm(self):
        """Test ALGORITHM constant."""
        assert JwtDefault.ALGORITHM == "HS256"

    def test_jwt_auth_enabled(self):
        """Test JWT_AUTH_ENABLED constant."""
        assert JwtDefault.JWT_AUTH_ENABLED is False

    def test_secret_key(self):
        """Test SECRET_KEY constant."""
        assert JwtDefault.SECRET_KEY == ""

    def test_access_token_expire_minute(self):
        """Test ACCESS_TOKEN_EXPIRE_MINUTE constant."""
        assert JwtDefault.ACCESS_TOKEN_EXPIRE_MINUTE == 1440

    def test_access_token_expire_minutes_alias(self):
        """Test ACCESS_TOKEN_EXPIRE_MINUTES is alias."""
        assert JwtDefault.ACCESS_TOKEN_EXPIRE_MINUTES == JwtDefault.ACCESS_TOKEN_EXPIRE_MINUTE

    def test_refresh_token_expire_days(self):
        """Test REFRESH_TOKEN_EXPIRE_DAYS constant."""
        assert JwtDefault.REFRESH_TOKEN_EXPIRE_DAYS == 7


class TestRateLimitDefault:
    """Tests for RateLimitDefault class."""

    def test_rate_limit_max_requests(self):
        """Test RATE_LIMIT_MAX_REQUESTS constant."""
        assert RateLimitDefault.RATE_LIMIT_MAX_REQUESTS == 2

    def test_rate_limit_window_seconds(self):
        """Test RATE_LIMIT_WINDOW_SECONDS constant."""
        assert RateLimitDefault.RATE_LIMIT_WINDOW_SECONDS == 60

    def test_rate_limit_requests_per_minute(self):
        """Test RATE_LIMIT_REQUESTS_PER_MINUTE constant."""
        assert RateLimitDefault.RATE_LIMIT_REQUESTS_PER_MINUTE == 60

    def test_rate_limit_requests_per_hour(self):
        """Test RATE_LIMIT_REQUESTS_PER_HOUR constant."""
        assert RateLimitDefault.RATE_LIMIT_REQUESTS_PER_HOUR == 1000

    def test_rate_limit_burst_limit(self):
        """Test RATE_LIMIT_BURST_LIMIT constant."""
        assert RateLimitDefault.RATE_LIMIT_BURST_LIMIT == 10


class TestAuthenticationDefault:
    """Tests for AuthenticationDefault class."""

    def test_security_jwt_expiry_minutes(self):
        """Test SECURITY_JWT_EXPIRY_MINUTES constant."""
        assert AuthenticationDefault.SECURITY_JWT_EXPIRY_MINUTES == 30

    def test_max_login_attempts(self):
        """Test MAX_LOGIN_ATTEMPTS constant."""
        assert AuthenticationDefault.MAX_LOGIN_ATTEMPTS == 5

    def test_lockout_duration_minutes(self):
        """Test LOCKOUT_DURATION_MINUTES constant."""
        assert AuthenticationDefault.LOCKOUT_DURATION_MINUTES == 15

    def test_password_history_count(self):
        """Test PASSWORD_HISTORY_COUNT constant."""
        assert AuthenticationDefault.PASSWORD_HISTORY_COUNT == 5

    def test_require_strong_password(self):
        """Test REQUIRE_STRONG_PASSWORD constant."""
        assert AuthenticationDefault.REQUIRE_STRONG_PASSWORD is True

    def test_session_timeout_minutes(self):
        """Test SESSION_TIMEOUT_MINUTES constant."""
        assert AuthenticationDefault.SESSION_TIMEOUT_MINUTES == 60

    def test_authentication_configuration(self):
        """Test AUTHENTICATION_CONFIGURATION dict."""
        config = AuthenticationDefault.AUTHENTICATION_CONFIGURATION
        assert "jwt_expiry_minutes" in config
        assert "max_login_attempts" in config
        assert config["jwt_expiry_minutes"] == 30


class TestRateLimitingDefault:
    """Tests for RateLimitingDefault class."""

    def test_rate_limiting_enable_sliding_window(self):
        """Test RATE_LIMITING_ENABLE_SLIDING_WINDOW constant."""
        assert RateLimitingDefault.RATE_LIMITING_ENABLE_SLIDING_WINDOW is True

    def test_rate_limiting_enable_token_bucket(self):
        """Test RATE_LIMITING_ENABLE_TOKEN_BUCKET constant."""
        assert RateLimitingDefault.RATE_LIMITING_ENABLE_TOKEN_BUCKET is False

    def test_rate_limiting_enable_fixed_window(self):
        """Test RATE_LIMITING_ENABLE_FIXED_WINDOW constant."""
        assert RateLimitingDefault.RATE_LIMITING_ENABLE_FIXED_WINDOW is False

    def test_rate_limiting_excluded_paths(self):
        """Test RATE_LIMITING_EXCLUDED_PATHS constant."""
        assert "/health" in RateLimitingDefault.RATE_LIMITING_EXCLUDED_PATHS
        assert "/docs" in RateLimitingDefault.RATE_LIMITING_EXCLUDED_PATHS

    def test_rate_limiting_excluded_methods(self):
        """Test RATE_LIMITING_EXCLUDED_METHODS constant."""
        assert "OPTIONS" in RateLimitingDefault.RATE_LIMITING_EXCLUDED_METHODS

    def test_rate_limiting_configuration(self):
        """Test RATE_LIMITING_CONFIGURATION dict."""
        config = RateLimitingDefault.RATE_LIMITING_CONFIGURATION
        assert "requests_per_minute" in config
        assert "burst_limit" in config


class TestSecurityHeadersDefault:
    """Tests for SecurityHeadersDefault class."""

    def test_security_headers_enable_hsts(self):
        """Test SECURITY_HEADERS_ENABLE_HSTS constant."""
        assert SecurityHeadersDefault.SECURITY_HEADERS_ENABLE_HSTS is True

    def test_security_headers_enable_csp(self):
        """Test SECURITY_HEADERS_ENABLE_CSP constant."""
        assert SecurityHeadersDefault.SECURITY_HEADERS_ENABLE_CSP is True

    def test_security_headers_csp_report_only(self):
        """Test SECURITY_HEADERS_CSP_REPORT_ONLY constant."""
        assert SecurityHeadersDefault.SECURITY_HEADERS_CSP_REPORT_ONLY is False

    def test_security_headers_hsts_max_age(self):
        """Test SECURITY_HEADERS_HSTS_MAX_AGE constant."""
        assert SecurityHeadersDefault.SECURITY_HEADERS_HSTS_MAX_AGE == 31_536_000

    def test_security_headers_hsts_include_subdomains(self):
        """Test SECURITY_HEADERS_HSTS_INCLUDE_SUBDOMAINS constant."""
        assert SecurityHeadersDefault.SECURITY_HEADERS_HSTS_INCLUDE_SUBDOMAINS is True

    def test_security_headers_hsts_preload(self):
        """Test SECURITY_HEADERS_HSTS_PRELOAD constant."""
        assert SecurityHeadersDefault.SECURITY_HEADERS_HSTS_PRELOAD is False

    def test_security_headers_configuration(self):
        """Test SECURITY_HEADERS_CONFIGURATION dict."""
        config = SecurityHeadersDefault.SECURITY_HEADERS_CONFIGURATION
        assert "enable_hsts" in config
        assert "enable_csp" in config


class TestInputValidationDefault:
    """Tests for InputValidationDefault class."""

    def test_input_validation_max_string_length(self):
        """Test INPUT_VALIDATION_MAX_STRING_LENGTH constant."""
        assert InputValidationDefault.INPUT_VALIDATION_MAX_STRING_LENGTH == 1000

    def test_input_validation_max_password_length(self):
        """Test INPUT_VALIDATION_MAX_PASSWORD_LENGTH constant."""
        assert InputValidationDefault.INPUT_VALIDATION_MAX_PASSWORD_LENGTH == 128

    def test_input_validation_min_password_length(self):
        """Test INPUT_VALIDATION_MIN_PASSWORD_LENGTH constant."""
        assert InputValidationDefault.INPUT_VALIDATION_MIN_PASSWORD_LENGTH == 8

    def test_input_validation_max_email_length(self):
        """Test INPUT_VALIDATION_MAX_EMAIL_LENGTH constant."""
        assert InputValidationDefault.INPUT_VALIDATION_MAX_EMAIL_LENGTH == 254

    def test_input_validation_enable_sql_injection_check(self):
        """Test INPUT_VALIDATION_ENABLE_SQL_INJECTION_CHECK constant."""
        assert InputValidationDefault.INPUT_VALIDATION_ENABLE_SQL_INJECTION_CHECK is True

    def test_input_validation_enable_xss_check(self):
        """Test INPUT_VALIDATION_ENABLE_XSS_CHECK constant."""
        assert InputValidationDefault.INPUT_VALIDATION_ENABLE_XSS_CHECK is True

    def test_input_validation_enable_path_traversal_check(self):
        """Test INPUT_VALIDATION_ENABLE_PATH_TRAVERSAL_CHECK constant."""
        assert InputValidationDefault.INPUT_VALIDATION_ENABLE_PATH_TRAVERSAL_CHECK is True

    def test_input_validation_weak_passwords(self):
        """Test INPUT_VALIDATION_WEAK_PASSWORDS constant."""
        assert "password" in InputValidationDefault.INPUT_VALIDATION_WEAK_PASSWORDS
        assert "123456" in InputValidationDefault.INPUT_VALIDATION_WEAK_PASSWORDS

    def test_input_validation_configuration(self):
        """Test INPUT_VALIDATION_CONFIGURATION dict."""
        config = InputValidationDefault.INPUT_VALIDATION_CONFIGURATION
        assert "max_string_length" in config
        assert "min_password_length" in config


class TestCorsSectionDefault:
    """Tests for CorsSectionDefault class."""

    def test_cors_default_allowed_origins(self):
        """Test CORS_DEFAULT_ALLOWED_ORIGINS constant."""
        assert "*" in CorsSectionDefault.CORS_DEFAULT_ALLOWED_ORIGINS

    def test_cors_default_allowed_methods(self):
        """Test CORS_DEFAULT_ALLOWED_METHODS constant."""
        assert "GET" in CorsSectionDefault.CORS_DEFAULT_ALLOWED_METHODS
        assert "POST" in CorsSectionDefault.CORS_DEFAULT_ALLOWED_METHODS

    def test_cors_default_allowed_headers(self):
        """Test CORS_DEFAULT_ALLOWED_HEADERS constant."""
        assert "*" in CorsSectionDefault.CORS_DEFAULT_ALLOWED_HEADERS

    def test_cors_default_allow_credentials(self):
        """Test CORS_DEFAULT_ALLOW_CREDENTIALS constant."""
        assert CorsSectionDefault.CORS_DEFAULT_ALLOW_CREDENTIALS is True

    def test_cors_default_max_age(self):
        """Test CORS_DEFAULT_MAX_AGE constant."""
        assert CorsSectionDefault.CORS_DEFAULT_MAX_AGE == 3600

    def test_cors_configuration(self):
        """Test CORS_CONFIGURATION dict."""
        config = CorsSectionDefault.CORS_CONFIGURATION
        assert "allowed_origins" in config
        assert "allowed_methods" in config


class TestDefault:
    """Tests for Default class (aggregated defaults)."""

    def test_default_inherits_application_default(self):
        """Test Default inherits from ApplicationDefault."""
        assert hasattr(Default, "APP_NAME")
        assert Default.APP_NAME == "FastMVC"

    def test_default_inherits_jwt_default(self):
        """Test Default inherits from JwtDefault."""
        assert hasattr(Default, "ALGORITHM")
        assert Default.ALGORITHM == "HS256"

    def test_default_inherits_rate_limit_default(self):
        """Test Default inherits from RateLimitDefault."""
        assert hasattr(Default, "RATE_LIMIT_MAX_REQUESTS")
        assert Default.RATE_LIMIT_MAX_REQUESTS == 2

    def test_default_security_configuration(self):
        """Test SECURITY_CONFIGURATION dict."""
        config = Default.SECURITY_CONFIGURATION
        assert "rate_limiting" in config
        assert "security_headers" in config
        assert "input_validation" in config
        assert "authentication" in config
        assert "cors" in config

    def test_default_rate_limiting_in_security_config(self):
        """Test rate_limiting in SECURITY_CONFIGURATION."""
        config = Default.SECURITY_CONFIGURATION["rate_limiting"]
        assert "requests_per_minute" in config

    def test_default_security_headers_in_security_config(self):
        """Test security_headers in SECURITY_CONFIGURATION."""
        config = Default.SECURITY_CONFIGURATION["security_headers"]
        assert "enable_hsts" in config

    def test_default_input_validation_in_security_config(self):
        """Test input_validation in SECURITY_CONFIGURATION."""
        config = Default.SECURITY_CONFIGURATION["input_validation"]
        assert "max_string_length" in config

    def test_default_authentication_in_security_config(self):
        """Test authentication in SECURITY_CONFIGURATION."""
        config = Default.SECURITY_CONFIGURATION["authentication"]
        assert "jwt_expiry_minutes" in config

    def test_default_cors_in_security_config(self):
        """Test cors in SECURITY_CONFIGURATION."""
        config = Default.SECURITY_CONFIGURATION["cors"]
        assert "allowed_origins" in config


class TestDefaultTypes:
    """Tests for default constant types."""

    def test_app_name_is_str(self):
        """Test APP_NAME is a string."""
        assert isinstance(Default.APP_NAME, str)

    def test_app_version_is_str(self):
        """Test APP_VERSION is a string."""
        assert isinstance(Default.APP_VERSION, str)

    def test_debug_is_bool(self):
        """Test DEBUG is a bool."""
        assert isinstance(Default.DEBUG, bool)

    def test_log_level_is_str(self):
        """Test LOG_LEVEL is a string."""
        assert isinstance(Default.LOG_LEVEL, str)

    def test_algorithm_is_str(self):
        """Test ALGORITHM is a string."""
        assert isinstance(Default.ALGORITHM, str)

    def test_jwt_auth_enabled_is_bool(self):
        """Test JWT_AUTH_ENABLED is a bool."""
        assert isinstance(Default.JWT_AUTH_ENABLED, bool)

    def test_rate_limit_max_requests_is_int(self):
        """Test RATE_LIMIT_MAX_REQUESTS is an int."""
        assert isinstance(Default.RATE_LIMIT_MAX_REQUESTS, int)

    def test_rate_limit_window_seconds_is_int(self):
        """Test RATE_LIMIT_WINDOW_SECONDS is an int."""
        assert isinstance(Default.RATE_LIMIT_WINDOW_SECONDS, int)

    def test_security_configuration_is_dict(self):
        """Test SECURITY_CONFIGURATION is a dict."""
        assert isinstance(Default.SECURITY_CONFIGURATION, dict)
