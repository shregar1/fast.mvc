"""
Singleton configuration loader for secrets backends.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.secrets import SecretsConfigurationDTO


class SecretsConfiguration:
    """
    Lazily loads secrets configuration from ``config/secrets/config.json``.
    """

    _instance: Optional["SecretsConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "secrets" / "config.json"
        raw = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        self._config = SecretsConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "SecretsConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> SecretsConfigurationDTO:
        return self._config


__all__ = [
    "SecretsConfiguration",
]

