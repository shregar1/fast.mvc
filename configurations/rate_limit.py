from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from dtos.configurations.rate_limit import RateLimitConfigDTO


class RateLimitConfiguration:
    _instance: Optional["RateLimitConfiguration"] = None

    def __init__(self) -> None:
        base = Path(__file__).resolve().parent.parent
        config_path = base / "config" / "rate_limit" / "config.json"
        if not config_path.exists():
            self._config = RateLimitConfigDTO()
            return
        with config_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        self._config = RateLimitConfigDTO(**raw)

    @classmethod
    def instance(cls) -> "RateLimitConfiguration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_config(self) -> RateLimitConfigDTO:
        return self._config


__all__ = ["RateLimitConfiguration"]

