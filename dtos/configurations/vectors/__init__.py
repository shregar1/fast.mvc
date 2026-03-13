"""
DTO package for vector store configuration.

Split per provider to keep each config focused, while exposing a
single aggregated ``VectorsConfigurationDTO`` for consumers.
"""

from __future__ import annotations

from pydantic import BaseModel

from .pinecone import PineconeConfigDTO
from .qdrant import QdrantConfigDTO
from .weaviate import WeaviateConfigDTO
from .pgvector import PGVectorConfigDTO
from .faiss import FaissConfigDTO
from .chroma import ChromaConfigDTO


class VectorsConfigurationDTO(BaseModel):
    """
    Aggregated configuration for all vector stores.
    """

    pinecone: PineconeConfigDTO = PineconeConfigDTO()
    qdrant: QdrantConfigDTO = QdrantConfigDTO()
    weaviate: WeaviateConfigDTO = WeaviateConfigDTO()
    pgvector: PGVectorConfigDTO = PGVectorConfigDTO()
    faiss: FaissConfigDTO = FaissConfigDTO()
    chroma: ChromaConfigDTO = ChromaConfigDTO()


__all__ = [
    "PineconeConfigDTO",
    "QdrantConfigDTO",
    "WeaviateConfigDTO",
    "PGVectorConfigDTO",
    "FaissConfigDTO",
    "ChromaConfigDTO",
    "VectorsConfigurationDTO",
]

