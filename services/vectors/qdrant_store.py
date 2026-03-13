from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

try:  # Optional dependency
    from qdrant_client import QdrantClient, models as qdrant_models
except Exception:  # pragma: no cover - optional
    QdrantClient = None  # type: ignore[assignment]
    qdrant_models = None  # type: ignore[assignment]

from .abstraction import IVectorStore


class QdrantVectorStore(IVectorStore):
    def __init__(self, url: str, api_key: Optional[str], collection_name: str) -> None:
        if QdrantClient is None or qdrant_models is None:  # pragma: no cover - optional
            raise RuntimeError("qdrant-client is not installed")
        self._client = QdrantClient(url=url, api_key=api_key or None)
        self._collection = collection_name

    async def upsert(self, items: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:
        points = [
            qdrant_models.PointStruct(
                id=_id,
                vector=vec,
                payload=meta,
            )
            for _id, vec, meta in items
        ]
        self._client.upsert(collection_name=self._collection, points=points)

    async def query(self, vector: List[float], *, top_k: int = 5) -> List[Dict[str, Any]]:
        res = self._client.search(
            collection_name=self._collection,
            query_vector=vector,
            limit=top_k,
        )
        out: List[Dict[str, Any]] = []
        for pt in res or []:
            out.append(
                {
                    "id": str(pt.id),
                    "score": pt.score,
                    "metadata": pt.payload or {},
                }
            )
        return out


__all__ = ["QdrantVectorStore"]

