"""List + total JSON payload for the Item API."""

from __future__ import annotations

from typing import Any

from models.item import Item


class ItemListResponseDTO:
    """``{ \"items\": [...], \"total\": n }`` for list/search/filter endpoints."""

    def __init__(self, items: list[dict[str, Any]], total: int) -> None:
        self._items = items
        self._total = total

    @classmethod
    def from_entities(cls, entities: list[Item]) -> ItemListResponseDTO:
        rows = [e.to_dict() for e in entities]
        return cls(rows, total=len(rows))

    def to_dict(self) -> dict[str, Any]:
        return {"items": self._items, "total": self._total}
