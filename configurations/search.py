"""
Singleton configuration loader for additional search providers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.search import SearchConfigurationDTO


class SearchConfiguration:
    """
    Lazily loads search configuration from ``config/search/config.json``.
    """

    _instance: Optional["SearchConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "search" / "config.json"
        raw = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        self._config = SearchConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "SearchConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> SearchConfigurationDTO:
        return self._config


__all__ = [
    "SearchConfiguration",
]

