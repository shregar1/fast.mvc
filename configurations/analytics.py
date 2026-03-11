"""
Singleton configuration loader for analytics and event tracking.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.analytics import AnalyticsConfigurationDTO


class AnalyticsConfiguration:
    """
    Lazily loads analytics configuration from ``config/analytics/config.json``.
    """

    _instance: Optional["AnalyticsConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "analytics" / "config.json"
        raw = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        self._config = AnalyticsConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "AnalyticsConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> AnalyticsConfigurationDTO:
        return self._config


__all__ = [
    "AnalyticsConfiguration",
]

