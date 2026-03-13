from __future__ import annotations

from typing import Any, Dict, List, Tuple

try:  # Optional dependency
    import psycopg2
except Exception:  # pragma: no cover - optional
    psycopg2 = None  # type: ignore[assignment]

from .abstraction import IVectorStore


class PGVectorStore(IVectorStore):
    def __init__(
        self,
        dsn: str,
        table: str,
        vector_column: str,
        id_column: str,
        metadata_column: str,
    ) -> None:
        if psycopg2 is None:  # pragma: no cover - optional
            raise RuntimeError("psycopg2 is not installed")
        self._dsn = dsn
        self._table = table
        self._vector_column = vector_column
        self._id_column = id_column
        self._metadata_column = metadata_column

    def _connect(self):
        return psycopg2.connect(self._dsn)

    async def upsert(self, items: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:
        import json

        with self._connect() as conn:
            with conn.cursor() as cur:
                for _id, vec, meta in items:
                    cur.execute(
                        f"""
                        INSERT INTO {self._table} ({self._id_column}, {self._vector_column}, {self._metadata_column})
                        VALUES (%s, %s, %s)
                        ON CONFLICT ({self._id_column})
                        DO UPDATE SET
                            {self._vector_column} = EXCLUDED.{self._vector_column},
                            {self._metadata_column} = EXCLUDED.{self._metadata_column}
                        """,
                        (_id, vec, json.dumps(meta)),
                    )

    async def query(self, vector: List[float], *, top_k: int = 5) -> List[Dict[str, Any]]:
        import json

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT {self._id_column}, {self._metadata_column},
                           1 - ({self._vector_column} <=> %s) AS score
                    FROM {self._table}
                    ORDER BY {self._vector_column} <=> %s
                    LIMIT %s
                    """,
                    (vector, vector, top_k),
                )
                rows = cur.fetchall()
        out: List[Dict[str, Any]] = []
        for _id, meta_json, score in rows:
            out.append(
                {
                    "id": str(_id),
                    "score": float(score),
                    "metadata": json.loads(meta_json or "{}"),
                }
            )
        return out


__all__ = ["PGVectorStore"]

