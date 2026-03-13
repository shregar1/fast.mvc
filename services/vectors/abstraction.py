"""
Core vector store abstraction used by all providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class IVectorStore(ABC):
    """
    Minimal vector store interface.
    """

    @abstractmethod
    async def upsert(self, items: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:  # pragma: no cover - interface
        """
        Upsert a list of (id, vector, metadata) items.
        """

    @abstractmethod
    async def query(self, vector: List[float], *, top_k: int = 5) -> List[Dict[str, Any]]:  # pragma: no cover - interface
        """
        Query similar vectors and return metadata with scores.
        """


__all__ = ["IVectorStore"]

