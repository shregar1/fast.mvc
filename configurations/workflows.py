from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.workflows import WorkflowsConfigurationDTO


class WorkflowsConfiguration:
    _instance: Optional["WorkflowsConfiguration"] = None

    def __init__(self) -> None:
        base = Path(__file__).resolve().parent.parent
        config_path = base / "config" / "workflows" / "config.json"
        if not config_path.exists():
            self._config = WorkflowsConfigurationDTO()
            return
        with config_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        self._config = WorkflowsConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "WorkflowsConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> WorkflowsConfigurationDTO:
        return self._config


__all__ = ["WorkflowsConfiguration"]

