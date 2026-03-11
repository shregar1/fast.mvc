"""
Socket.IO-based channels backend (stub).

For more advanced realtime use cases, you can run a Socket.IO server
using `python-socketio` and integrate it with FastAPI / ASGI. This
backend provides a thin abstraction to fit that into the generic
ChannelBackend interface.
"""

from typing import Any, AsyncGenerator, Optional

from loguru import logger

from core.channels.base import ChannelBackend


try:
    import socketio  # type: ignore[import]
except Exception:  # pragma: no cover - optional dependency
    socketio = None  # type: ignore[assignment]


class SocketIOChannelBackend(ChannelBackend):
    def __init__(self, sio_server: Optional["socketio.AsyncServer"] = None) -> None:
        """
        If `sio_server` is provided, it will be used to emit events.
        Otherwise, this backend will only log publish attempts.
        """

        self._sio = sio_server

    async def publish(self, topic: str, message: Any) -> None:
        """
        Emit a message on a Socket.IO room / namespace.
        """

        if self._sio is None:
            logger.info(
                "SocketIOChannelBackend.publish called without server instance",
                room=topic,
            )
            logger.debug(f"Socket.IO message payload: {message!r}")
            return

        await self._sio.emit("message", message, room=topic)

    async def subscribe(self, topic: str) -> AsyncGenerator[str, None]:
        """
        Socket.IO subscriptions are handled by event handlers on the
        AsyncServer instance. This method is not implemented in the stub.
        """

        raise NotImplementedError(
            "SocketIOChannelBackend.subscribe is not implemented; "
            "use Socket.IO event handlers on the server instead."
        )

