"""
Configuration DTOs for per-tenant rate limiting and quotas.
"""

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel


class RateLimitConfigDTO(BaseModel):
    enabled: bool = False
    default_per_minute: int = 60
    default_burst: int = 120
    # Optional per-tenant overrides: {tenant_id: per_minute}
    per_tenant_overrides: Dict[str, int] = {}


__all__ = ["RateLimitConfigDTO"]

