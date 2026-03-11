"""
Generic presence / rooms service.

This service can operate purely in-memory (per-process) or use Redis
for distributed presence tracking. It is designed to work alongside
the Channels hub and any of the configured realtime providers.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple

from loguru import logger

try:
    import redis.asyncio as aioredis  # type: ignore[import]
except Exception:  # pragma: no cover - optional dependency
    aioredis = None  # type: ignore[assignment]


@dataclass
class PresenceEntry:
    user_id: str
    last_seen: float


class InMemoryPresenceBackend:
    """
    Simple in-memory presence backend.

    Suitable for local development or single-process deployments.
    """

    def __init__(self, ttl_seconds: int = 60) -> None:
        self._ttl_seconds = ttl_seconds
        # room_id -> user_id -> PresenceEntry
        self._rooms: Dict[str, Dict[str, PresenceEntry]] = {}

    async def mark_present(self, room_id: str, user_id: str) -> None:
        now = time.time()
        room = self._rooms.setdefault(room_id, {})
        room[user_id] = PresenceEntry(user_id=user_id, last_seen=now)
        logger.debug(f"User {user_id} present in room {room_id}")

    async def mark_absent(self, room_id: str, user_id: str) -> None:
        room = self._rooms.get(room_id)
        if not room:
            return
        room.pop(user_id, None)
        if not room:
            self._rooms.pop(room_id, None)
        logger.debug(f"User {user_id} left room {room_id}")

    async def list_present(self, room_id: str) -> List[str]:
        self._evict_expired()
        room = self._rooms.get(room_id, {})
        return list(room.keys())

    async def list_rooms_for_user(self, user_id: str) -> List[str]:
        self._evict_expired()
        rooms: List[str] = []
        for room_id, members in self._rooms.items():
            if user_id in members:
                rooms.append(room_id)
        return rooms

    def _evict_expired(self) -> None:
        now = time.time()
        to_delete: List[Tuple[str, str]] = []
        for room_id, members in self._rooms.items():
            for user_id, entry in members.items():
                if now - entry.last_seen > self._ttl_seconds:
                    to_delete.append((room_id, user_id))
        for room_id, user_id in to_delete:
            members = self._rooms.get(room_id)
            if not members:
                continue
            members.pop(user_id, None)
            if not members:
                self._rooms.pop(room_id, None)


class RedisPresenceBackend:
    """
    Redis-backed presence backend.

    Uses Redis sets and key expirations to track active members in rooms:
      - presence:{room_id} -> set(user_ids)
    """

    def __init__(self, client: "aioredis.Redis", ttl_seconds: int = 60) -> None:
        self._client = client
        self._ttl_seconds = ttl_seconds

    def _room_key(self, room_id: str) -> str:
        return f"presence:{room_id}"

    async def mark_present(self, room_id: str, user_id: str) -> None:
        key = self._room_key(room_id)
        await self._client.sadd(key, user_id)
        await self._client.expire(key, self._ttl_seconds)
        logger.debug(f"[Redis] User {user_id} present in room {room_id}")

    async def mark_absent(self, room_id: str, user_id: str) -> None:
        key = self._room_key(room_id)
        await self._client.srem(key, user_id)
        logger.debug(f"[Redis] User {user_id} left room {room_id}")

    async def list_present(self, room_id: str) -> List[str]:
        key = self._room_key(room_id)
        members: Set[bytes] = await self._client.smembers(key)
        return [m.decode("utf-8") for m in members]

    async def list_rooms_for_user(self, user_id: str) -> List[str]:
        # This operation is non-trivial with plain Redis sets; we keep it
        # simple and log a hint for projects that need it.
        logger.debug(
            "RedisPresenceBackend.list_rooms_for_user is not optimized; "
            "consider implementing a reverse index in your project."
        )
        return []


class PresenceService:
    """
    High-level presence / rooms service.

    This service delegates to either an in-memory backend or a Redis
    backend, depending on how it is constructed by the application.
    """

    def __init__(
        self,
        backend: Optional[object] = None,
    ) -> None:
        # Backend is expected to implement the methods of
        # InMemoryPresenceBackend / RedisPresenceBackend.
        if backend is None:
            backend = InMemoryPresenceBackend()
        self._backend = backend

    async def mark_present(self, room_id: str, user_id: str) -> None:
        await self._backend.mark_present(room_id, user_id)

    async def mark_absent(self, room_id: str, user_id: str) -> None:
        await self._backend.mark_absent(room_id, user_id)

    async def list_present(self, room_id: str) -> List[str]:
        return await self._backend.list_present(room_id)

    async def list_rooms_for_user(self, user_id: str) -> List[str]:
        return await self._backend.list_rooms_for_user(user_id)

