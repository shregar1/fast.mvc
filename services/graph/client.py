from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from loguru import logger

from fastmvc_core import GraphConfiguration
from core.utils.optional_imports import optional_import

_neo4j_mod, _neo4j_driver_cls = optional_import("neo4j", "GraphDatabase")


class IGraphStore(ABC):
    """
    Minimal graph database abstraction.
    """

    @abstractmethod
    async def run(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:  # pragma: no cover - interface
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class Neo4jGraphStore(IGraphStore):
    def __init__(self, uri: str, user: Optional[str], password: Optional[str], database: Optional[str]) -> None:
        if _neo4j_driver_cls is None:  # pragma: no cover - optional
            raise RuntimeError("neo4j driver is not installed")
        # The neo4j driver is synchronous; we offload blocking work to a thread.
        self._uri = uri
        self._user = user
        self._password = password
        self._database = database
        self._driver = _neo4j_driver_cls.driver(uri, auth=(user, password))  # type: ignore[call-arg]

    async def run(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        from asyncio import to_thread

        def _run_sync() -> List[Dict[str, Any]]:
            with self._driver.session(database=self._database) as session:  # type: ignore[call-arg]
                result = session.run(query, parameters or {})
                return [record.data() for record in result]

        return await to_thread(_run_sync)

    async def close(self) -> None:
        from asyncio import to_thread

        await to_thread(self._driver.close)


def build_graph_store() -> Optional[IGraphStore]:
    """
    Build a graph store from configuration.

    Currently supports Neo4j only.
    """
    cfg = GraphConfiguration.instance().get_config()
    if cfg.neo4j.enabled:
        try:
            return Neo4jGraphStore(
                uri=cfg.neo4j.uri,
                user=cfg.neo4j.user,
                password=cfg.neo4j.password,
                database=cfg.neo4j.database or None,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize Neo4j graph store: %s", exc)
    logger.info("No graph store is enabled.")
    return None


__all__ = [
    "IGraphStore",
    "Neo4jGraphStore",
    "build_graph_store",
]

