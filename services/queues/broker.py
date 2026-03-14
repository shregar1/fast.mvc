"""Re-export from fastmvc_core for backward compatibility."""

from fastmvc_core.services.queues.broker import (
    QueueMessage,
    IQueueBackend,
    QueueBroker,
)

__all__ = [
    "QueueMessage",
    "IQueueBackend",
    "QueueBroker",
]
