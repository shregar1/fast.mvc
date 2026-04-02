"""Tests for health constants."""

from __future__ import annotations

import pytest

from constants.health import (
    HEALTH_STATUS_HEALTHY,
    HEALTH_STATUS_UNHEALTHY,
    DEPENDENCY_NOT_CONFIGURED,
    DEPENDENCY_CONNECTED,
    DEPENDENCY_DISCONNECTED,
    READINESS_READY,
    READINESS_NOT_READY,
    LIVENESS_ALIVE,
    HEALTH_CHECK_SQL_PING,
    HealthMessageUtil,
)


class TestHealthStatusConstants:
    """Tests for health status constants."""

    def test_health_status_healthy(self):
        """Test HEALTH_STATUS_HEALTHY constant."""
        assert HEALTH_STATUS_HEALTHY == "healthy"

    def test_health_status_unhealthy(self):
        """Test HEALTH_STATUS_UNHEALTHY constant."""
        assert HEALTH_STATUS_UNHEALTHY == "unhealthy"


class TestDependencyConstants:
    """Tests for dependency constants."""

    def test_dependency_not_configured(self):
        """Test DEPENDENCY_NOT_CONFIGURED constant."""
        assert DEPENDENCY_NOT_CONFIGURED == "not_configured"

    def test_dependency_connected(self):
        """Test DEPENDENCY_CONNECTED constant."""
        assert DEPENDENCY_CONNECTED == "connected"

    def test_dependency_disconnected(self):
        """Test DEPENDENCY_DISCONNECTED constant."""
        assert DEPENDENCY_DISCONNECTED == "disconnected"


class TestReadinessConstants:
    """Tests for readiness constants."""

    def test_readiness_ready(self):
        """Test READINESS_READY constant."""
        assert READINESS_READY == "ready"

    def test_readiness_not_ready(self):
        """Test READINESS_NOT_READY constant."""
        assert READINESS_NOT_READY == "not_ready"


class TestLivenessConstants:
    """Tests for liveness constants."""

    def test_liveness_alive(self):
        """Test LIVENESS_ALIVE constant."""
        assert LIVENESS_ALIVE == "alive"


class TestHealthCheckConstants:
    """Tests for health check constants."""

    def test_health_check_sql_ping(self):
        """Test HEALTH_CHECK_SQL_PING constant."""
        assert HEALTH_CHECK_SQL_PING == "SELECT 1"


class TestHealthConstantsTypes:
    """Tests for health constant types."""

    def test_health_status_healthy_is_string(self):
        """Test HEALTH_STATUS_HEALTHY is a string."""
        assert isinstance(HEALTH_STATUS_HEALTHY, str)

    def test_health_status_unhealthy_is_string(self):
        """Test HEALTH_STATUS_UNHEALTHY is a string."""
        assert isinstance(HEALTH_STATUS_UNHEALTHY, str)

    def test_dependency_not_configured_is_string(self):
        """Test DEPENDENCY_NOT_CONFIGURED is a string."""
        assert isinstance(DEPENDENCY_NOT_CONFIGURED, str)

    def test_dependency_connected_is_string(self):
        """Test DEPENDENCY_CONNECTED is a string."""
        assert isinstance(DEPENDENCY_CONNECTED, str)

    def test_dependency_disconnected_is_string(self):
        """Test DEPENDENCY_DISCONNECTED is a string."""
        assert isinstance(DEPENDENCY_DISCONNECTED, str)

    def test_readiness_ready_is_string(self):
        """Test READINESS_READY is a string."""
        assert isinstance(READINESS_READY, str)

    def test_readiness_not_ready_is_string(self):
        """Test READINESS_NOT_READY is a string."""
        assert isinstance(READINESS_NOT_READY, str)

    def test_liveness_alive_is_string(self):
        """Test LIVENESS_ALIVE is a string."""
        assert isinstance(LIVENESS_ALIVE, str)

    def test_health_check_sql_ping_is_string(self):
        """Test HEALTH_CHECK_SQL_PING is a string."""
        assert isinstance(HEALTH_CHECK_SQL_PING, str)


class TestHealthMessageUtil:
    """Tests for HealthMessageUtil class."""

    def test_dependency_disconnected_message(self):
        """Test dependency_disconnected_message formatting."""
        exc = Exception("Connection refused")
        result = HealthMessageUtil.dependency_disconnected_message(exc)
        assert result == "disconnected: Connection refused"

    def test_dependency_disconnected_message_with_different_exception(self):
        """Test dependency_disconnected_message with different exception."""
        exc = Exception("Timeout after 30s")
        result = HealthMessageUtil.dependency_disconnected_message(exc)
        assert result == "disconnected: Timeout after 30s"

    def test_dependency_disconnected_message_with_empty_exception(self):
        """Test dependency_disconnected_message with empty exception."""
        exc = Exception("")
        result = HealthMessageUtil.dependency_disconnected_message(exc)
        assert result == "disconnected: "
