"""
Pusher-based implementation of the channels backend (stub).

This backend demonstrates how you could integrate with Pusher's
publish API. It intentionally keeps the implementation minimal and
does not require the `pusher` library at runtime; you can extend it
in a generated project to use the official client.
"""

from typing import Any, AsyncGenerator

from loguru import logger

from core.channels.base import ChannelBackend


class PusherChannelBackend(ChannelBackend):
    def __init__(
        self,
        app_id: str,
        key: str,
        secret: str,
        cluster: str,
        use_tls: bool = True,
    ) -> None:
        self._app_id = app_id
        self._key = key
        self._secret = secret
        self._cluster = cluster
        self._use_tls = use_tls

    async def publish(self, topic: str, message: Any) -> None:
        """
        Publish a message to a Pusher channel.

        In a real implementation, this would call the Pusher HTTP API
        or use the official client library. Here we only log the intent
        to keep FastMVC lightweight by default.
        """

        logger.info(
            "PusherChannelBackend.publish called",
            channel=topic,
        )
        logger.debug(f"Pusher message payload: {message!r}")

    async def subscribe(self, topic: str) -> AsyncGenerator[str, None]:
        """
        Server-side subscription is typically handled by the Pusher
        service and client SDKs. For FastMVC, we expose this coroutine
        to satisfy the ChannelBackend interface, but we do not implement
        a streaming subscription here.
        """

        raise NotImplementedError(
            "PusherChannelBackend.subscribe is not implemented; "
            "use client-side subscriptions via Pusher SDKs."
        )

