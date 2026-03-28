"""String constants for ``/health`` payloads and dependency probe results.

Keep probe outcomes stable for load balancers, monitors, and API consumers.
"""

from __future__ import annotations

from typing import Final

# --- Rollup status (``data.status`` on GET /health) ---
HEALTH_STATUS_HEALTHY: Final[str] = "healthy"
HEALTH_STATUS_UNHEALTHY: Final[str] = "unhealthy"

# --- Per-dependency values (database, redis, …) ---
DEPENDENCY_NOT_CONFIGURED: Final[str] = "not_configured"
DEPENDENCY_CONNECTED: Final[str] = "connected"
DEPENDENCY_DISCONNECTED: Final[str] = "disconnected"

# --- Readiness / liveness payload values ---
READINESS_READY: Final[str] = "ready"
READINESS_NOT_READY: Final[str] = "not_ready"
LIVENESS_ALIVE: Final[str] = "alive"

# --- DB probe ---
HEALTH_CHECK_SQL_PING: Final[str] = "SELECT 1"


def dependency_disconnected_message(exc: BaseException) -> str:
    """Format a dependency failure string: ``disconnected: <error>``."""
    return f"{DEPENDENCY_DISCONNECTED}: {str(exc)}"
