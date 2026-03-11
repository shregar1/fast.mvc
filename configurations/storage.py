"""
Singleton configuration loader for file/object storage providers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.storage import StorageConfigurationDTO


class StorageConfiguration:
    """
    Lazily loads storage configuration from ``config/storage/config.json``.
    """

    _instance: Optional["StorageConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "storage" / "config.json"
        raw = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        self._config = StorageConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "StorageConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> StorageConfigurationDTO:
        return self._config


__all__ = [
    "StorageConfiguration",
]

