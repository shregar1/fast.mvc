"""
Factory for building the appropriate vector store implementation.
"""

from __future__ import annotations

from typing import Optional

from loguru import logger

from fastmvc_core import VectorsConfiguration
from .abstraction import IVectorStore
from .pinecone_store import PineconeVectorStore
from .qdrant_store import QdrantVectorStore
from .weaviate_store import WeaviateVectorStore
from .pgvector_store import PGVectorStore
from .faiss_store import FaissVectorStore
from .chroma_store import ChromaVectorStore


def build_vector_store() -> Optional[IVectorStore]:
    """
    Build a vector store instance from configuration.

    Priority:
      - Pinecone
      - Qdrant
      - Weaviate
      - PGVector
      - FAISS
      - ChromaDB
    """

    cfg = VectorsConfiguration.instance().get_config()

    if cfg.pinecone.enabled and cfg.pinecone.api_key:
        try:
            return PineconeVectorStore(
                api_key=cfg.pinecone.api_key,
                environment=cfg.pinecone.environment,
                index_name=cfg.pinecone.index_name,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize Pinecone vector store: %s", exc)

    if cfg.qdrant.enabled:
        try:
            return QdrantVectorStore(
                url=cfg.qdrant.url,
                api_key=cfg.qdrant.api_key,
                collection_name=cfg.qdrant.collection_name,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize Qdrant vector store: %s", exc)

    if cfg.weaviate.enabled:
        try:
            return WeaviateVectorStore(
                url=cfg.weaviate.url,
                api_key=cfg.weaviate.api_key,
                class_name=cfg.weaviate.class_name,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize Weaviate vector store: %s", exc)

    if cfg.pgvector.enabled:
        try:
            return PGVectorStore(
                dsn=cfg.pgvector.dsn,
                table=cfg.pgvector.table,
                vector_column=cfg.pgvector.vector_column,
                id_column=cfg.pgvector.id_column,
                metadata_column=cfg.pgvector.metadata_column,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize PGVector store: %s", exc)

    if cfg.faiss.enabled:
        try:
            return FaissVectorStore()
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize FAISS vector store: %s", exc)

    if cfg.chroma.enabled:
        try:
            return ChromaVectorStore(persist_directory=cfg.chroma.persist_directory)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize ChromaDB vector store: %s", exc)

    logger.info("No vector store is enabled.")
    return None


__all__ = [
    "IVectorStore",
    "PineconeVectorStore",
    "QdrantVectorStore",
    "WeaviateVectorStore",
    "PGVectorStore",
    "FaissVectorStore",
    "ChromaVectorStore",
    "build_vector_store",
]

