"""
Queue / messaging abstraction layer.

Provides a minimal interface over RabbitMQ, Amazon SQS, and NATS.
Concrete integrations use optional third-party libraries; if they are
not installed, calls will log warnings instead of crashing.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional

from loguru import logger

from configurations.queues import QueuesConfiguration

try:  # Optional dependencies
    import boto3
except Exception:  # pragma: no cover - optional
    boto3 = None  # type: ignore

try:
    import pika
except Exception:  # pragma: no cover - optional
    pika = None  # type: ignore

try:
    import nats
except Exception:  # pragma: no cover - optional
    nats = None  # type: ignore


@dataclass
class QueueMessage:
    body: bytes
    attributes: Dict[str, Any] | None = None


class IQueueBackend:
    """
    Minimal interface for queue backends.
    """

    name: str

    async def publish(self, message: QueueMessage, *, routing_key: Optional[str] = None) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class RabbitMQBackend(IQueueBackend):
    def __init__(self, url: str, exchange: str, default_routing_key: str) -> None:
        self.name = "rabbitmq"
        self._url = url
        self._exchange = exchange
        self._default_routing_key = default_routing_key

    async def publish(self, message: QueueMessage, *, routing_key: Optional[str] = None) -> None:
        if pika is None:  # pragma: no cover - optional
            logger.warning("pika is not installed; RabbitMQ publish skipped.")
            return

        routing_key = routing_key or self._default_routing_key

        def _publish_sync() -> None:
            params = pika.URLParameters(self._url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.exchange_declare(exchange=self._exchange, exchange_type="topic", durable=True)
            channel.basic_publish(
                exchange=self._exchange,
                routing_key=routing_key,
                body=message.body,
            )
            connection.close()

        await asyncio.to_thread(_publish_sync)


class SQSBackend(IQueueBackend):
    def __init__(
        self,
        region: str,
        queue_url: str,
        access_key_id: Optional[str],
        secret_access_key: Optional[str],
    ) -> None:
        self.name = "sqs"
        self._region = region
        self._queue_url = queue_url
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key

    async def publish(self, message: QueueMessage, *, routing_key: Optional[str] = None) -> None:  # routing_key unused
        if boto3 is None:  # pragma: no cover - optional
            logger.warning("boto3 is not installed; SQS publish skipped.")
            return

        def _send_sync() -> None:
            session_kwargs: Dict[str, Any] = {}
            if self._access_key_id and self._secret_access_key:
                session_kwargs.update(
                    aws_access_key_id=self._access_key_id,
                    aws_secret_access_key=self._secret_access_key,
                )
            sqs = boto3.client("sqs", region_name=self._region, **session_kwargs)
            sqs.send_message(
                QueueUrl=self._queue_url,
                MessageBody=message.body.decode("utf-8"),
                MessageAttributes={
                    k: {"StringValue": str(v), "DataType": "String"}
                    for k, v in (message.attributes or {}).items()
                },
            )

        await asyncio.to_thread(_send_sync)


class NATSBackend(IQueueBackend):
    def __init__(self, servers: list[str], subject: str) -> None:
        self.name = "nats"
        self._servers = servers
        self._subject = subject

    async def publish(self, message: QueueMessage, *, routing_key: Optional[str] = None) -> None:
        if nats is None:  # pragma: no cover - optional
            logger.warning("nats-py is not installed; NATS publish skipped.")
            return

        servers = ",".join(self._servers)
        nc = await nats.connect(servers=servers)
        await nc.publish(self._subject, message.body)
        await nc.drain()


class QueueBroker:
    """
    High-level facade over multiple queue backends.

    It instantiates enabled backends from configuration and lets callers
    publish messages by backend name.
    """

    def __init__(self) -> None:
        cfg = QueuesConfiguration.instance().get_config()
        self._backends: Dict[str, IQueueBackend] = {}

        if cfg.rabbitmq.enabled and cfg.rabbitmq.url:
            self._backends["rabbitmq"] = RabbitMQBackend(
                url=cfg.rabbitmq.url,
                exchange=cfg.rabbitmq.exchange,
                default_routing_key=cfg.rabbitmq.default_routing_key,
            )

        if cfg.sqs.enabled and cfg.sqs.queue_url:
            self._backends["sqs"] = SQSBackend(
                region=cfg.sqs.region,
                queue_url=cfg.sqs.queue_url,
                access_key_id=cfg.sqs.access_key_id,
                secret_access_key=cfg.sqs.secret_access_key,
            )

        if cfg.nats.enabled and cfg.nats.servers:
            self._backends["nats"] = NATSBackend(
                servers=cfg.nats.servers,
                subject=cfg.nats.subject,
            )

        if not self._backends:
            logger.info(
                "No queue backends are enabled. "
                "Configure config/queues/config.json to enable RabbitMQ/SQS/NATS.",
            )

    async def publish(
        self,
        backend: str,
        body: bytes | str,
        *,
        routing_key: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        if isinstance(body, str):
            body_bytes = body.encode("utf-8")
        else:
            body_bytes = body

        backend_instance = self._backends.get(backend)
        if not backend_instance:
            logger.warning("Queue backend %s is not configured/enabled.", backend)
            return

        await backend_instance.publish(
            QueueMessage(body=body_bytes, attributes=attributes),
            routing_key=routing_key,
        )


__all__ = [
    "QueueMessage",
    "IQueueBackend",
    "QueueBroker",
]

