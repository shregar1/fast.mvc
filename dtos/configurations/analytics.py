"""
Configuration DTOs for analytics / BI and event tracking.

Includes ClickHouse, BigQuery, and a generic event pipeline with
HTTP/webhook sinks.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ClickHouseConfigDTO(BaseModel):
    enabled: bool = False
    url: str = "http://localhost:8123"
    database: str = "default"
    username: Optional[str] = None
    password: Optional[str] = None
    table: str = "events"


class BigQueryConfigDTO(BaseModel):
    enabled: bool = False
    project_id: Optional[str] = None
    dataset: str = "events"
    table: str = "events"
    credentials_json_path: Optional[str] = None


class HttpEventSinkConfigDTO(BaseModel):
    """
    Simple Segment-style HTTP sink.
    """

    enabled: bool = False
    endpoint: Optional[str] = None
    api_key: Optional[str] = None


class AnalyticsConfigurationDTO(BaseModel):
    """
    Aggregated configuration for analytics providers and event sinks.
    """

    clickhouse: ClickHouseConfigDTO = ClickHouseConfigDTO()
    bigquery: BigQueryConfigDTO = BigQueryConfigDTO()
    http_sink: HttpEventSinkConfigDTO = HttpEventSinkConfigDTO()


__all__ = [
    "ClickHouseConfigDTO",
    "BigQueryConfigDTO",
    "HttpEventSinkConfigDTO",
    "AnalyticsConfigurationDTO",
]

