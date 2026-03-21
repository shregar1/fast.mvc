"""Backward-compatible re-exports; implementation is ``fast_core.services.events``."""

from fast_core.services.events import (
    IEventBus,
    INotificationBus,
    build_event_bus,
    build_notification_bus,
)

__all__ = [
    "IEventBus",
    "INotificationBus",
    "build_event_bus",
    "build_notification_bus",
]
