"""
Singleton configuration loader for feature flags.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.feature_flags import FeatureFlagsConfigurationDTO


class FeatureFlagsConfiguration:
    """
    Lazily loads feature flag configuration from
    ``config/feature_flags/config.json``.
    """

    _instance: Optional["FeatureFlagsConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "feature_flags" / "config.json"
        raw = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        self._config = FeatureFlagsConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "FeatureFlagsConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> FeatureFlagsConfigurationDTO:
        return self._config


__all__ = [
    "FeatureFlagsConfiguration",
]

