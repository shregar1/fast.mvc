"""
Supabase Realtime-based channels backend (stub).

Supabase Realtime uses PostgreSQL logical replication and websockets.
This backend is a placeholder to illustrate how you might route
publish operations through Supabase.
"""

from typing import Any, AsyncGenerator

from loguru import logger

from core.channels.base import ChannelBackend


class SupabaseRealtimeBackend(ChannelBackend):
    def __init__(self, url: str, api_key: str) -> None:
        self._url = url
        self._api_key = api_key

    async def publish(self, topic: str, message: Any) -> None:
        """
        In Supabase Realtime, messages are generally written to database
        tables and streamed via replication to connected clients.

        This stub does not perform any network I/O; it simply logs the
        intent. Generated projects can replace this with a concrete
        implementation (e.g. via HTTP or a Postgres client).
        """

        logger.info(
            "SupabaseRealtimeBackend.publish called",
            channel=topic,
        )
        logger.debug(f"Supabase message payload: {message!r}")

    async def subscribe(self, topic: str) -> AsyncGenerator[str, None]:
        """
        Subscription is typically driven by Supabase client SDKs over
        websockets. This stub does not implement server-side streaming.
        """

        raise NotImplementedError(
            "SupabaseRealtimeBackend.subscribe is not implemented; "
            "use client-side subscriptions via Supabase clients."
        )

