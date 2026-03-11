"""
Grouped DTOs for communication-related configuration (email, chat, push).
"""

from pydantic import BaseModel

from dtos.configurations.email import EmailConfigurationDTO
from dtos.configurations.push import PushConfigurationDTO
from dtos.configurations.slack import SlackConfigurationDTO


class CommunicationsConfigurationDTO(BaseModel):
    """
    Aggregate configuration for communication channels.

    Groups email, Slack/chat, and push-notification configuration DTOs.
    """

    email: EmailConfigurationDTO
    slack: SlackConfigurationDTO
    push: PushConfigurationDTO


__all__ = [
    "CommunicationsConfigurationDTO",
]

