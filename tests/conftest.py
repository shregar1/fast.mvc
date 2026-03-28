"""Pytest Configuration and Shared Fixtures.

This file is automatically loaded by pytest and provides:
- Path setup for imports
- Shared fixtures for all tests
- Custom markers and configuration

Usage:
    Fixtures are automatically available in all test files.

    def test_something(item_client, test_item):
        # item_client and test_item are automatically injected
        pass

    def test_factories(fetch_example_request_payload):
        # Top-level factories package (see factories/README.md)
        assert "reference_number" in fetch_example_request_payload
"""

import os
import sys
from pathlib import Path

# =============================================================================
# PATH SETUP
# =============================================================================

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# ITEM API FIXTURES — registered via plugin (no duplicate import lists)
# =============================================================================

pytest_plugins = ["tests.fixtures.item"]

# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================


def pytest_configure(config):
    """Configure pytest with custom markers.

    These markers can be used to categorize and filter tests.
    """
    config.addinivalue_line("markers", "unit: Unit tests (fast, isolated)")
    config.addinivalue_line(
        "markers", "integration: Integration tests (may use database)"
    )
    config.addinivalue_line("markers", "e2e: End-to-end tests (full flow)")
    config.addinivalue_line("markers", "slow: Slow tests (skip in fast mode)")
    config.addinivalue_line("markers", "auth: Authentication-related tests")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "db: DataI-related tests")


# =============================================================================
# CUSTOM FIXTURES SPECIFIC TO TESTS
# =============================================================================

import pytest


@pytest.fixture(scope="session")
def test_settings():
    """Provide test-specific settings.

    Returns:
        Dictionary with test configuration.

    """
    return {
        "dataI_url": "sqlite:///./test.db",
        "jwt_secret": "test-secret-key-minimum-32-characters-long",
        "jwt_algorithm": "HS256",
        "jwt_expiration_hours": 24,
        "debug": True,
        "log_level": "DEBUG",
    }


@pytest.fixture(autouse=True)
def setup_test_env(test_settings, monkeypatch):
    """Set up environment for each test.

    Automatically configures environment variables for testing.
    """
    # Set test environment variables
    for key, value in test_settings.items():
        env_key = key.upper()
        monkeypatch.setenv(env_key, str(value))

    yield

    # Cleanup is handled by monkeypatch


@pytest.fixture
def captured_logs(caplog):
    """Provide captured log output for testing.

    Example:
        def test_logs(captured_logs):
            # Run code that logs
            assert "Expected message" in captured_logs.text

    """
    import logging

    caplog.set_level(logging.DEBUG)
    return caplog


# =============================================================================
# TOP-LEVEL FACTORIES (see factories/README.md)
# =============================================================================

from factories import ExampleFetchRequestFactory


@pytest.fixture
def fetch_example_request_payload() -> dict:
    """Valid ``FetchUserRequestDTO`` body fields as a dict (includes ``reference_number``)."""
    return ExampleFetchRequestFactory.build()
