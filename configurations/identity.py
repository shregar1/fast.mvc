"""
Singleton configuration loader for identity providers / SSO.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.identity import IdentityProvidersConfigurationDTO


class IdentityProvidersConfiguration:
    """
    Lazily loads identity provider configuration from config/identity/config.json.
    """

    _instance: Optional["IdentityProvidersConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "identity" / "config.json"
        raw = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        self._config = IdentityProvidersConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "IdentityProvidersConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> IdentityProvidersConfigurationDTO:
        return self._config


__all__ = [
    "IdentityProvidersConfiguration",
]

