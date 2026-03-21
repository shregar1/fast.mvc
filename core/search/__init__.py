"""Search backends — re-exported from ``fast_search``. Prefer ``from fast_search import …`` in new code."""

from fast_search import (
    BulkIndexError,
    BulkIndexResult,
    FacetBucket,
    FacetedSearchResult,
    ISearchBackend,
    SearchConfiguration,
    SearchConfigurationDTO,
    SearchHit,
    build_search_backend,
    bulk_index_documents,
    suggest_autocomplete,
    swap_index_alias,
)

__all__ = [
    "BulkIndexError",
    "BulkIndexResult",
    "FacetBucket",
    "FacetedSearchResult",
    "ISearchBackend",
    "SearchConfiguration",
    "SearchConfigurationDTO",
    "SearchHit",
    "build_search_backend",
    "bulk_index_documents",
    "suggest_autocomplete",
    "swap_index_alias",
]
