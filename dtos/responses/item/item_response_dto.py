"""Single-item JSON payload for the Item API."""

from __future__ import annotations

from typing import Any

from models.item import Item


class ItemResponseDTO:
    """Maps an :class:`~models.item.Item` to the JSON body returned by item routes."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    @classmethod
    def from_entity(
        cls, entity: Item, *, reference_urn: str | None = None
    ) -> ItemResponseDTO:
        _ = reference_urn  # reserved for future envelope / header correlation
        return cls(entity.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return dict(self._payload)
