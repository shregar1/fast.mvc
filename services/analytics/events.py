"""
Event tracking / analytics pipeline.

Provides a small abstraction over ClickHouse, BigQuery, and HTTP
webhook sinks, loosely inspired by Segment-style event tracking.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from loguru import logger

from configurations.analytics import AnalyticsConfiguration

try:  # Optional dependencies
    import httpx
except Exception:  # pragma: no cover - optional
    httpx = None  # type: ignore

try:
    import clickhouse_connect
except Exception:  # pragma: no cover - optional
    clickhouse_connect = None  # type: ignore

try:
    from google.cloud import bigquery
except Exception:  # pragma: no cover - optional
    bigquery = None  # type: ignore


@dataclass
class Event:
    user_id: Optional[str]
    event: str
    properties: Dict[str, Any]
    timestamp: datetime


class EventSink:
    async def send(self, event: Event) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class ClickHouseSink(EventSink):
    def __init__(self, url: str, database: str, table: str, username: Optional[str], password: Optional[str]) -> None:
        if clickhouse_connect is None:  # pragma: no cover - optional
            raise RuntimeError("clickhouse-connect is not installed")
        self._client = clickhouse_connect.get_client(
            url=url,
            username=username,
            password=password,
            database=database,
        )
        self._table = table

    async def send(self, event: Event) -> None:
        self._client.insert(
            self._table,
            [
                [
                    event.user_id,
                    event.event,
                    json.dumps(event.properties),
                    event.timestamp.replace(tzinfo=timezone.utc),
                ]
            ],
            column_names=["user_id", "event", "properties", "timestamp"],
        )


class BigQuerySink(EventSink):
    def __init__(
        self,
        project_id: str,
        dataset: str,
        table: str,
        credentials_json_path: Optional[str],
    ) -> None:
        if bigquery is None:  # pragma: no cover - optional
            raise RuntimeError("google-cloud-bigquery is not installed")
        if credentials_json_path:
            from google.oauth2 import service_account

            creds = service_account.Credentials.from_service_account_file(credentials_json_path)
            self._client = bigquery.Client(project=project_id, credentials=creds)
        else:
            self._client = bigquery.Client(project=project_id)
        self._table_ref = f"{project_id}.{dataset}.{table}"

    async def send(self, event: Event) -> None:
        row = {
            "user_id": event.user_id,
            "event": event.event,
            "properties": event.properties,
            "timestamp": event.timestamp.replace(tzinfo=timezone.utc).isoformat(),
        }
        errors = self._client.insert_rows_json(self._table_ref, [row])
        if errors:
            logger.warning("BigQuery insert errors: %s", errors)


class HttpEventSink(EventSink):
    def __init__(self, endpoint: str, api_key: Optional[str]) -> None:
        if httpx is None:  # pragma: no cover - optional
            raise RuntimeError("httpx is not installed")
        self._endpoint = endpoint
        self._api_key = api_key

    async def send(self, event: Event) -> None:
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        payload = {
            "userId": event.user_id,
            "event": event.event,
            "properties": event.properties,
            "timestamp": event.timestamp.replace(tzinfo=timezone.utc).isoformat(),
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(self._endpoint, json=payload, headers=headers, timeout=5)
            if resp.status_code >= 400:
                logger.warning("HTTP event sink error %s: %s", resp.status_code, resp.text)


class EventTracker:
    """
    High-level event tracking pipeline with pluggable sinks.
    """

    def __init__(self) -> None:
        cfg = AnalyticsConfiguration.instance().get_config()
        self._sinks: list[EventSink] = []

        if cfg.clickhouse.enabled:
            try:
                self._sinks.append(
                    ClickHouseSink(
                        url=cfg.clickhouse.url,
                        database=cfg.clickhouse.database,
                        table=cfg.clickhouse.table,
                        username=cfg.clickhouse.username,
                        password=cfg.clickhouse.password,
                    )
                )
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Failed to initialize ClickHouse sink: %s", exc)

        if cfg.bigquery.enabled and cfg.bigquery.project_id:
            try:
                self._sinks.append(
                    BigQuerySink(
                        project_id=cfg.bigquery.project_id,
                        dataset=cfg.bigquery.dataset,
                        table=cfg.bigquery.table,
                        credentials_json_path=cfg.bigquery.credentials_json_path,
                    )
                )
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Failed to initialize BigQuery sink: %s", exc)

        if cfg.http_sink.enabled and cfg.http_sink.endpoint:
            try:
                self._sinks.append(
                    HttpEventSink(
                        endpoint=cfg.http_sink.endpoint,
                        api_key=cfg.http_sink.api_key,
                    )
                )
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Failed to initialize HTTP event sink: %s", exc)

        if not self._sinks:
            logger.info("No analytics/event sinks are enabled.")

    async def track(
        self,
        event_name: str,
        *,
        user_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        e = Event(
            user_id=user_id,
            event=event_name,
            properties=properties or {},
            timestamp=timestamp or datetime.now(timezone.utc),
        )
        for sink in self._sinks:
            await sink.send(e)


__all__ = [
    "Event",
    "EventSink",
    "ClickHouseSink",
    "BigQuerySink",
    "HttpEventSink",
    "EventTracker",
]

