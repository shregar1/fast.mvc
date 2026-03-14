from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple

from fastapi import HTTPException, status
from loguru import logger

from fastmvc_core import RateLimitConfiguration
from core.utils.optional_imports import optional_import

_redis_mod, _redis_cls = optional_import("redis.asyncio", "Redis")


class InMemoryRateLimiter:
    """
    Simple token-bucket style in-memory rate limiter keyed by tenant + route.

    This is best-effort and primarily useful for development; production
    deployments should prefer the Redis-based limiter.
    """

    def __init__(self, per_minute: int, burst: int) -> None:
        self._per_minute = per_minute
        self._burst = burst
        # key -> (tokens, last_refill_ts)
        self._buckets: Dict[str, Tuple[float, float]] = {}

    def _refill(self, key: str, now: float) -> None:
        rate_per_sec = self._per_minute / 60.0
        tokens, last = self._buckets.get(key, (self._burst, now))
        elapsed = max(0.0, now - last)
        tokens = min(self._burst, tokens + elapsed * rate_per_sec)
        self._buckets[key] = (tokens, now)

    def allow(self, key: str, cost: float = 1.0) -> bool:
        now = time.time()
        self._refill(key, now)
        tokens, _ = self._buckets.get(key, (self._burst, now))
        if tokens >= cost:
            self._buckets[key] = (tokens - cost, now)
            return True
        return False


class RedisRateLimiter:
    """
    Redis-backed rate limiter using a token bucket implemented with INCR + EXPIRE.
    """

    def __init__(self, per_minute: int, burst: int, redis_url: str, namespace: str) -> None:
        if _redis_cls is None:  # pragma: no cover - optional
            raise RuntimeError("redis.asyncio is not installed")
        self._per_minute = per_minute
        self._burst = burst
        self._redis = _redis_cls.from_url(redis_url)  # type: ignore[operator]
        self._ns = namespace.rstrip(":") + ":rl:"

    def _k(self, tenant_id: str, route: str) -> str:
        return f"{self._ns}{tenant_id}:{route}"

    async def allow(self, tenant_id: str, route: str, cost: int = 1) -> bool:
        key = self._k(tenant_id, route)
        pipe = self._redis.pipeline()
        pipe.incrby(key, cost)
        pipe.expire(key, 60)
        current, _ = await pipe.execute()
        if int(current) > self._burst:
            return False
        # Simple per-minute cap approximation; burst controls hard ceiling.
        return True


class RateLimiter:
    def __init__(self) -> None:
        cfg = RateLimitConfiguration.instance().get_config()
        self._enabled = cfg.enabled
        self._default_per_min = cfg.default_per_minute
        self._default_burst = cfg.default_burst
        self._overrides = cfg.per_tenant_overrides or {}

        # For now, always start with in-memory; Redis can be wired by the app.
        self._memory = InMemoryRateLimiter(
            per_minute=self._default_per_min,
            burst=self._default_burst,
        )

    def _limit_for_tenant(self, tenant_id: str) -> Tuple[int, int]:
        per_min = self._overrides.get(tenant_id, self._default_per_min)
        return per_min, max(per_min * 2, self._default_burst)

    async def ensure_allowed(self, tenant_id: str, route_id: str) -> None:
        if not self._enabled:
            return
        per_min, burst = self._limit_for_tenant(tenant_id)
        # Adjust memory limiter parameters on the fly
        self._memory._per_minute = per_min  # type: ignore[attr-defined]
        self._memory._burst = burst  # type: ignore[attr-defined]
        key = f"{tenant_id}:{route_id}"
        if not self._memory.allow(key):
            logger.warning("Rate limit exceeded for tenant=%s route=%s", tenant_id, route_id)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )


_RL_SINGLETON: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    global _RL_SINGLETON
    if _RL_SINGLETON is None:
        _RL_SINGLETON = RateLimiter()
    return _RL_SINGLETON


__all__ = [
    "InMemoryRateLimiter",
    "RedisRateLimiter",
    "RateLimiter",
    "get_rate_limiter",
]

