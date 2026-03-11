"""
Singleton configuration loader for queue / messaging backends.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.queues import QueuesConfigurationDTO


class QueuesConfiguration:
    """
    Lazily loads queue configuration from ``config/queues/config.json``.
    """

    _instance: Optional["QueuesConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "queues" / "config.json"
        raw = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        self._config = QueuesConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "QueuesConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> QueuesConfigurationDTO:
        return self._config


__all__ = [
    "QueuesConfiguration",
]

