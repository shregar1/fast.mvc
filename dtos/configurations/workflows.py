"""
Configuration DTOs for workflow/orchestration backends.

Supports Temporal, Prefect, and Dagster as pluggable engines.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


class WorkflowsConfigurationDTO(BaseModel):
    enabled: bool = False
    engine: Literal["temporal", "prefect", "dagster"] = "temporal"

    # Temporal-specific
    temporal_address: str = "localhost:7233"
    temporal_namespace: str = "default"
    temporal_task_queue: str = "fastmvc-orders"

    # Prefect-specific
    prefect_api_url: Optional[str] = None
    prefect_default_deployment: Optional[str] = None

    # Dagster-specific
    dagster_grpc_endpoint: Optional[str] = None
    dagster_job_name: Optional[str] = None


__all__ = ["WorkflowsConfigurationDTO"]

