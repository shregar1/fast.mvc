"""
Search-related service exports.
"""

from .client import (
    ISearchClient,
    MeilisearchClient,
    TypesenseClient,
    OpenSearchClient,
    AlgoliaSearchClient,
    build_search_client,
)

__all__ = [
    "ISearchClient",
    "MeilisearchClient",
    "TypesenseClient",
    "OpenSearchClient",
    "AlgoliaSearchClient",
    "build_search_client",
]

