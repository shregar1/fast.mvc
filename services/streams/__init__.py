"""Backward-compatible re-exports; implementation is ``fast_core.services.streams``."""

from fast_core.services.streams import (
    IEventStream,
    IMarketDataFeed,
    MarketDataHub,
    OrderEvent,
    Tick,
    get_market_data_hub,
)

__all__ = [
    "Tick",
    "OrderEvent",
    "IMarketDataFeed",
    "IEventStream",
    "MarketDataHub",
    "get_market_data_hub",
]
