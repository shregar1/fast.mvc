from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.graph import GraphConfigurationDTO


class GraphConfiguration:
    _instance: Optional["GraphConfiguration"] = None

    def __init__(self) -> None:
        base = Path(__file__).resolve().parent.parent
        config_path = base / "config" / "graph" / "config.json"
        if not config_path.exists():
            self._config = GraphConfigurationDTO()
            return
        with config_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        self._config = GraphConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "GraphConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> GraphConfigurationDTO:
        return self._config


__all__ = ["GraphConfiguration"]

