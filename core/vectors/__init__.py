"""Vector stores — re-exported from ``fast_vectors``. Prefer ``from fast_vectors import …`` in new code."""

from fast_vectors import (
    IVectorStore,
    PineconeConfigDTO,
    QdrantConfigDTO,
    VectorsConfiguration,
    VectorsConfigurationDTO,
    WeaviateConfigDTO,
    build_vector_store,
    prefixed_collection_name,
    sanitize_collection_segment,
)

__all__ = [
    "IVectorStore",
    "PineconeConfigDTO",
    "QdrantConfigDTO",
    "VectorsConfiguration",
    "VectorsConfigurationDTO",
    "WeaviateConfigDTO",
    "build_vector_store",
    "prefixed_collection_name",
    "sanitize_collection_segment",
]
