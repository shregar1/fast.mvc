"""Request ID Context Management.

Provides context variables for tracking request IDs across async contexts.
"""

from contextvars import ContextVar, Token
from typing import Optional

# Context variable for storing the current request ID
_request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


class RequestIdContext:
    """Manager for request ID context variables.

    This class provides a way to store and retrieve the current request ID
    in an async-safe manner using context variables.

    Example:
        >>> token = RequestIdContext.set("req-123")
        >>> current_id = RequestIdContext.get()
        >>> print(current_id)  # "req-123"
        >>> RequestIdContext.reset(token)

    """

    @staticmethod
    def get() -> Optional[str]:
        """Get the current request ID from context."""
        return _request_id_var.get()

    @staticmethod
    def set(request_id: Optional[str]) -> Token[Optional[str]]:
        """Bind *request_id* for the current async task.

        Returns:
            A token for use with :meth:`reset`.
        """
        return _request_id_var.set(request_id)

    @staticmethod
    def reset(token: Token[Optional[str]]) -> None:
        """Restore the previous value (call in ``finally`` after :meth:`set`)."""
        _request_id_var.reset(token)
