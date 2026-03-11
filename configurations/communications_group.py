"""
Communications Configuration Aggregator.

Provides a single access point (`CommunicationsConfiguration`) that
aggregates email, Slack, and push notification configuration into a
`CommunicationsConfigurationDTO`.
"""

from typing import Optional

from configurations.email import EmailConfiguration
from configurations.push import PushConfiguration
from configurations.slack import SlackConfiguration
from dtos.configurations.communications import CommunicationsConfigurationDTO


class CommunicationsConfiguration:
    """
    Aggregated configuration for communication channels.

    Example:
        cfg = CommunicationsConfiguration().get_config()
        email_cfg = cfg.email
        slack_cfg = cfg.slack
        push_cfg = cfg.push
    """

    _instance: Optional["CommunicationsConfiguration"] = None

    def __new__(cls) -> "CommunicationsConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_config(self) -> CommunicationsConfigurationDTO:
        """
        Load all communications configurations and return a grouped DTO.
        """
        return CommunicationsConfigurationDTO(
            email=EmailConfiguration().get_config(),
            slack=SlackConfiguration().get_config(),
            push=PushConfiguration().get_config(),
        )

