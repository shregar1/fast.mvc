"""
Configuration DTOs for background job workers and schedulers.

Includes Celery, RQ, Dramatiq, and a generic scheduler backend
that can represent APScheduler, Temporal, or Prefect.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


class CeleryConfigDTO(BaseModel):
    enabled: bool = False
    broker_url: str = "redis://localhost:6379/0"
    result_backend: str = "redis://localhost:6379/1"
    namespace: str = "fastmvc"


class RQConfigDTO(BaseModel):
    enabled: bool = False
    redis_url: str = "redis://localhost:6379/0"
    queue_name: str = "default"


class DramatiqConfigDTO(BaseModel):
    enabled: bool = False
    broker_url: str = "redis://localhost:6379/0"
    queue_name: str = "default"


SchedulerBackend = Literal["none", "apscheduler", "temporal", "prefect"]


class SchedulerConfigDTO(BaseModel):
    enabled: bool = False
    backend: SchedulerBackend = "none"
    timezone: str = "UTC"


class JobsConfigurationDTO(BaseModel):
    """
    Aggregated configuration for job workers and schedulers.
    """

    celery: CeleryConfigDTO = CeleryConfigDTO()
    rq: RQConfigDTO = RQConfigDTO()
    dramatiq: DramatiqConfigDTO = DramatiqConfigDTO()
    scheduler: SchedulerConfigDTO = SchedulerConfigDTO()


__all__ = [
    "CeleryConfigDTO",
    "RQConfigDTO",
    "DramatiqConfigDTO",
    "SchedulerConfigDTO",
    "SchedulerBackend",
    "JobsConfigurationDTO",
]

