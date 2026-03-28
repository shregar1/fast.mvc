"""Request DTO abstraction for the item segment."""

from dtos.requests.abstraction import IRequestDTO


class IRequestItemDTO(IRequestDTO):
    """Interface for item-scoped request DTOs (create, update, …)."""
