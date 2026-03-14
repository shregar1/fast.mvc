"""Cache backends and decorator (re-exported from fastmvc_core)."""

from fastmvc_core.services.cache import (
    ICache,
    InMemoryCache,
    RedisCache,
    get_cache,
    cache_result,
)

__all__ = [
    "ICache",
    "InMemoryCache",
    "RedisCache",
    "get_cache",
    "cache_result",
]
