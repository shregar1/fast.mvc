"""Statistics JSON payload for ``GET /items/statistics``."""

from __future__ import annotations

from typing import Any


class ItemStatsResponseDTO:
    """Wraps the stats dict from :meth:`services.item.item_service.ItemService.get_statistics`."""

    def __init__(self, stats: dict[str, Any]) -> None:
        self._stats = stats

    @classmethod
    def from_stats(cls, stats: dict[str, Any]) -> ItemStatsResponseDTO:
        return cls(stats)

    def to_dict(self) -> dict[str, Any]:
        return dict(self._stats)
