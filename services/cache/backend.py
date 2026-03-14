"""Re-export from fastmvc_core for backward compatibility."""

from fastmvc_core.services.cache.backend import (
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
