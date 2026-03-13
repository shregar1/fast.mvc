from __future__ import annotations

from pathlib import Path
from typing import Optional

import json

from dtos.configurations.events import EventsConfigurationDTO


class EventsConfiguration:
    _instance: Optional["EventsConfiguration"] = None

    def __init__(self) -> None:
        base = Path(__file__).resolve().parent.parent
        config_path = base / "config" / "events" / "config.json"
        if not config_path.exists():
            self._config = EventsConfigurationDTO()
            return
        with config_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        self._config = EventsConfigurationDTO(**raw)

    @classmethod
    def instance(cls) -> "EventsConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> EventsConfigurationDTO:
        return self._config


__all__ = ["EventsConfiguration"]

