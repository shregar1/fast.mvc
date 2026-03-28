"""Root DTO layer — re-exports and inheritance map for :mod:`dtos`.

Hierarchy (each arrow is “inherits”):

- :class:`abstractions.dto.IDTO` — all DTOs
- **Configuration:** :class:`dtos.configuration.abstraction.IConfigurationDTO`
- **Requests:** :class:`dtos.requests.abstraction.IRequestDTO` →
  :class:`dtos.requests.apis.abstraction.IRequestAPIDTO` →
  :class:`dtos.requests.apis.v1.abstraction.IRequestAPIV1DTO` → …;
  parallel segments: :class:`dtos.requests.item.abstraction.IRequestItemDTO`,
  :class:`dtos.requests.example.abstraction.IRequestExampleDTO`, …
- **Responses:** :class:`dtos.responses.abstraction.IResponseDTO` →
  :class:`dtos.responses.apis.abstraction.IResponseAPIDTO` →
  :class:`dtos.responses.apis.v1.abstraction.IResponseAPIV1DTO` → …;
  parallel segments: :class:`dtos.responses.item.abstraction.IResponseItemDTO`,
  :class:`dtos.responses.example.abstraction.IResponseExampleDTO`, …
"""

from __future__ import annotations

from abstractions.dto import IDTO

from dtos.configuration.abstraction import IConfigurationDTO
from dtos.requests.abstraction import IRequestDTO
from dtos.responses.abstraction import IResponseDTO

__all__ = [
    "IDTO",
    "IConfigurationDTO",
    "IRequestDTO",
    "IResponseDTO",
]
