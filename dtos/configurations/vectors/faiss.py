from __future__ import annotations

from pydantic import BaseModel


class FaissConfigDTO(BaseModel):
    enabled: bool = False
    use_gpu: bool = False


__all__ = ["FaissConfigDTO"]

