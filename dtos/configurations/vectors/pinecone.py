from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class PineconeConfigDTO(BaseModel):
    enabled: bool = False
    api_key: Optional[str] = None
    environment: Optional[str] = None
    index_name: str = "fastmvc-index"


__all__ = ["PineconeConfigDTO"]

