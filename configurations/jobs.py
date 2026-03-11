"""
Singleton configuration loader for background job workers and schedulers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.jobs import JobsConfigurationDTO


class JobsConfiguration:
    """
    Lazily loads jobs configuration from ``config/jobs/config.json``.
    """

    _instance: Optional["JobsConfiguration"] = None

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent.parent
        config_path = base_path / "config" / "jobs" / "config.json"
        raw = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())

        self._config = JobsConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "JobsConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> JobsConfigurationDTO:
        return self._config


__all__ = [
    "JobsConfiguration",
]

