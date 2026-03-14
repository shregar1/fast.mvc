"""Queue and messaging services (re-exported from fastmvc_core)."""

from fastmvc_core.services.queues import (
    QueueMessage,
    IQueueBackend,
    QueueBroker,
)

__all__ = [
    "QueueMessage",
    "IQueueBackend",
    "QueueBroker",
]
