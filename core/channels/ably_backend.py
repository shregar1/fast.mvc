"""
Ably-based implementation of the channels backend (stub).

Real implementations should depend on the official Ably Python SDK.
This stub exists to show how Ably can fit into the generic
ChannelBackend abstraction.
"""

from typing import Any, AsyncGenerator

from loguru import logger

from core.channels.base import ChannelBackend


class AblyChannelBackend(ChannelBackend):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def publish(self, topic: str, message: Any) -> None:
        """
        Publish a message to an Ably channel.

        Replace this with a call to the Ably SDK in generated projects.
        """

        logger.info(
            "AblyChannelBackend.publish called",
            channel=topic,
        )
        logger.debug(f"Ably message payload: {message!r}")

    async def subscribe(self, topic: str) -> AsyncGenerator[str, None]:
        """
        Server-side streaming subscriptions are not implemented in this
        stub. Use Ably client libraries from your frontend or extend
        this class in your project.
        """

        raise NotImplementedError(
            "AblyChannelBackend.subscribe is not implemented; "
            "use client-side subscriptions via Ably SDKs."
        )

