"""
Realtime Configuration Module.

Provides a singleton configuration manager for realtime / collaboration
providers such as Pusher, Ably, Supabase Realtime, Socket.IO, and
the generic presence / rooms service.
"""

import json
from typing import Optional

from dtos.configurations.realtime import RealtimeConfigurationDTO
from start_utils import logger


class RealtimeConfiguration:
    """
    Singleton configuration manager for realtime settings.

    Configuration is loaded from `config/realtime/config.json`.
    """

    _instance: Optional["RealtimeConfiguration"] = None

    def __new__(cls) -> "RealtimeConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load realtime configuration from JSON file.
        """
        try:
            with open("config/realtime/config.json") as file:
                self._config = json.load(file)
            logger.debug("Realtime config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Realtime config file not found.")
            self._config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding realtime config file.")
            self._config = {}

    def get_config(self) -> RealtimeConfigurationDTO:
        """
        Get realtime configuration as a validated DTO.
        """
        return RealtimeConfigurationDTO(**self._config)

