"""Response DTO abstraction for v1 user API envelopes."""

from dtos.responses.apis.v1.abstraction import IResponseAPIV1DTO


class IResponseUserV1DTO(IResponseAPIV1DTO):
    """Interface for v1 user-scoped response envelope DTOs."""
