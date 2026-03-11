"""
Configuration DTOs for feature flag providers.

Includes LaunchDarkly and Unleash, aggregated for convenience.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class LaunchDarklyConfigDTO(BaseModel):
    enabled: bool = False
    sdk_key: Optional[str] = None
    default_user_key: str = "anonymous"


class UnleashConfigDTO(BaseModel):
    enabled: bool = False
    url: str = "http://localhost:4242/api"
    app_name: str = "fastmvc"
    instance_id: str = "fastmvc-instance"
    api_key: Optional[str] = None


class FeatureFlagsConfigurationDTO(BaseModel):
    """
    Aggregated configuration for feature flag providers.
    """

    launchdarkly: LaunchDarklyConfigDTO = LaunchDarklyConfigDTO()
    unleash: UnleashConfigDTO = UnleashConfigDTO()


__all__ = [
    "LaunchDarklyConfigDTO",
    "UnleashConfigDTO",
    "FeatureFlagsConfigurationDTO",
]

