"""Response DTO abstraction for the item segment."""

from dtos.responses.abstraction import IResponseDTO


class IResponseItemDTO(IResponseDTO):
    """Interface for item resource response envelopes (single, list, stats)."""
