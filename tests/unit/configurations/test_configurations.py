"""
Tests for main-repo configuration aggregators (DatastoresConfiguration, CommunicationsConfiguration).

Loader and DTO tests for DB, Cache, Security, etc. live in fast_platform.
"""

from unittest.mock import patch


@patch("fast_platform.config.resolver.load_config_json")
def test_datastores_configuration_get_config(mock_load):
    """DatastoresConfiguration.get_config() returns grouped DTO from fast_platform and main configs."""
    mock_load.return_value = {}
    from fast_platform import DatastoresConfiguration
    # Reset singleton for test
    DatastoresConfiguration._instance = None
    cfg = DatastoresConfiguration().get_config()
    assert cfg is not None
    assert cfg.db is not None
    assert cfg.cache is not None


@patch("fast_platform.config.resolver.load_config_json")
def test_communications_configuration_get_config(mock_load):
    """CommunicationsConfiguration.get_config() returns grouped DTO."""
    mock_load.return_value = {}
    from fast_platform import CommunicationsConfiguration
    CommunicationsConfiguration._instance = None
    cfg = CommunicationsConfiguration().get_config()
    assert cfg is not None
    assert cfg.email is not None
    assert cfg.slack is not None
    assert cfg.push is not None
