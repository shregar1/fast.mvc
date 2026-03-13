"""
Configuration DTOs for application-level caching.

Supports an in-process memory cache and optional Redis-backed cache.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


class CacheConfigurationDTO(BaseModel):
    enabled: bool = True
    backend: Literal["memory", "redis"] = "memory"
    default_ttl_seconds: int = 60
    redis_url: Optional[str] = "redis://localhost:6379/2"
    namespace: str = "fastmvc-cache"


__all__ = ["CacheConfigurationDTO"]

"""
DTO for cache configuration settings.
"""
from pydantic import BaseModel


class CacheConfigurationDTO(BaseModel):
    """
    DTO for cache configuration.
    Fields:
        host (str): Redis host.
        port (int): Redis port.
        password (str): Redis password.
    """
    host: str
    port: int
    password: str
