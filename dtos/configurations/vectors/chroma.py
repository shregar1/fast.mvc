from __future__ import annotations

from pydantic import BaseModel


class ChromaConfigDTO(BaseModel):
    enabled: bool = False
    persist_directory: str = "chroma-data"


__all__ = ["ChromaConfigDTO"]

