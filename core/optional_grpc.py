"""Optional gRPC transport wiring (removable template).

This module isolates gRPC startup/shutdown from `app.py` so gRPC can be
removed cleanly by deleting a couple of lines in the lifespan handler.
"""

from __future__ import annotations

from typing import Any, Optional

from loguru import logger

from constants.default import Default
from constants.environment import EnvironmentVar
from utilities.env import EnvironmentParserUtility


async def maybe_start_grpc(app: Any) -> None:
    """Start optional gRPC transport when enabled."""
    grpc_enabled = EnvironmentParserUtility.get_bool_with_logging(
        EnvironmentVar.GRPC_ENABLED,
        Default.GRPC_ENABLED,
    )
    if not grpc_enabled:
        return

    try:
        from core.grpc_server import start_grpc_health_server, stop_grpc_server  # pyright: ignore[reportMissingImports]

        server = await start_grpc_health_server()
        app.state._fastmvc_grpc = {
            "server": server,
            "stop": stop_grpc_server,
        }
        logger.info("Optional gRPC transport enabled")
    except Exception:
        logger.exception("Failed to start optional gRPC server")


async def maybe_stop_grpc(app: Any) -> None:
    """Best-effort stop of the optional gRPC transport."""
    cfg: Optional[dict[str, Any]] = getattr(app.state, "_fastmvc_grpc", None)
    if not cfg:
        return

    try:
        stop_fn = cfg.get("stop")
        server = cfg.get("server")
        if stop_fn is not None:
            await stop_fn(server)
    except Exception:
        logger.exception("Failed to stop optional gRPC server cleanly")

