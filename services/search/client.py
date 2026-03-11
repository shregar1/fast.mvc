"""
Search client abstraction for additional providers (beyond Elasticsearch).

Supports Meilisearch, Typesense, OpenSearch, and Algolia via a common
``ISearchClient`` interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from loguru import logger

from configurations.search import SearchConfiguration

try:  # Optional dependencies
    import meilisearch
except Exception:  # pragma: no cover - optional
    meilisearch = None  # type: ignore

try:
    import typesense
except Exception:  # pragma: no cover - optional
    typesense = None  # type: ignore

try:
    from opensearchpy import OpenSearch
except Exception:  # pragma: no cover - optional
    OpenSearch = None  # type: ignore

try:
    from algoliasearch.search_client import SearchClient as AlgoliaClient
except Exception:  # pragma: no cover - optional
    AlgoliaClient = None  # type: ignore


class ISearchClient(ABC):
    """
    Minimal search interface.
    """

    @abstractmethod
    async def index_document(self, index: str, doc_id: str, body: Dict[str, Any]) -> None:  # pragma: no cover - interface
        raise NotImplementedError

    @abstractmethod
    async def delete_document(self, index: str, doc_id: str) -> None:  # pragma: no cover - interface
        raise NotImplementedError

    @abstractmethod
    async def search(self, index: str, query: str, *, limit: int = 10) -> List[Dict[str, Any]]:  # pragma: no cover - interface
        raise NotImplementedError


class MeilisearchClient(ISearchClient):
    def __init__(self, url: str, api_key: Optional[str]) -> None:
        if meilisearch is None:  # pragma: no cover - optional
            raise RuntimeError("meilisearch client library is not installed")
        self._client = meilisearch.Client(url, api_key or None)

    async def index_document(self, index: str, doc_id: str, body: Dict[str, Any]) -> None:
        index_client = self._client.index(index)
        payload = {**body, "id": doc_id}
        index_client.add_documents([payload])

    async def delete_document(self, index: str, doc_id: str) -> None:
        index_client = self._client.index(index)
        index_client.delete_document(doc_id)

    async def search(self, index: str, query: str, *, limit: int = 10) -> List[Dict[str, Any]]:
        index_client = self._client.index(index)
        res = index_client.search(query, {"limit": limit})
        return list(res.get("hits", []))


class TypesenseClient(ISearchClient):
    def __init__(self, host: str, port: int, protocol: str, api_key: Optional[str]) -> None:
        if typesense is None:  # pragma: no cover - optional
            raise RuntimeError("typesense client library is not installed")
        self._client = typesense.Client(
            {
                "nodes": [{"host": host, "port": port, "protocol": protocol}],
                "api_key": api_key or "",
                "connection_timeout_seconds": 2,
            }
        )

    async def index_document(self, index: str, doc_id: str, body: Dict[str, Any]) -> None:
        collection = self._client.collections[index]
        payload = {**body, "id": doc_id}
        collection.documents.create(payload)

    async def delete_document(self, index: str, doc_id: str) -> None:
        collection = self._client.collections[index]
        collection.documents[doc_id].delete()

    async def search(self, index: str, query: str, *, limit: int = 10) -> List[Dict[str, Any]]:
        collection = self._client.collections[index]
        res = collection.documents.search({"q": query, "query_by": "text", "per_page": limit})
        return list(res.get("hits", []))


class OpenSearchClient(ISearchClient):
    def __init__(self, hosts: List[str], username: Optional[str], password: Optional[str]) -> None:
        if OpenSearch is None:  # pragma: no cover - optional
            raise RuntimeError("opensearch-py client library is not installed")
        http_auth = (username, password) if username and password else None
        self._client = OpenSearch(hosts=hosts, http_auth=http_auth)

    async def index_document(self, index: str, doc_id: str, body: Dict[str, Any]) -> None:
        self._client.index(index=index, id=doc_id, body=body, refresh=True)

    async def delete_document(self, index: str, doc_id: str) -> None:
        self._client.delete(index=index, id=doc_id, ignore=[404])

    async def search(self, index: str, query: str, *, limit: int = 10) -> List[Dict[str, Any]]:
        res = self._client.search(
            index=index,
            body={"query": {"multi_match": {"query": query, "fields": ["*"]}}},
            size=limit,
        )
        return [hit["_source"] for hit in res.get("hits", {}).get("hits", [])]


class AlgoliaSearchClient(ISearchClient):
    def __init__(self, app_id: str, api_key: str, default_index: Optional[str]) -> None:
        if AlgoliaClient is None:  # pragma: no cover - optional
            raise RuntimeError("algoliasearch client library is not installed")
        self._client = AlgoliaClient.create(app_id, api_key)
        self._default_index = default_index

    def _get_index(self, index: Optional[str]) -> Any:
        name = index or self._default_index
        if not name:
            raise ValueError("Algolia index name must be provided")
        return self._client.init_index(name)

    async def index_document(self, index: str, doc_id: str, body: Dict[str, Any]) -> None:
        idx = self._get_index(index)
        payload = {**body, "objectID": doc_id}
        idx.save_object(payload)

    async def delete_document(self, index: str, doc_id: str) -> None:
        idx = self._get_index(index)
        idx.delete_object(doc_id)

    async def search(self, index: str, query: str, *, limit: int = 10) -> List[Dict[str, Any]]:
        idx = self._get_index(index)
        res = idx.search(query, {"hitsPerPage": limit})
        return list(res.get("hits", []))


def build_search_client() -> Optional[ISearchClient]:
    """
    Build a search client from configuration.

    Priority:
      - Meilisearch
      - Typesense
      - OpenSearch
      - Algolia
    """

    cfg = SearchConfiguration.instance().get_config()

    if cfg.meilisearch.enabled:
        try:
            return MeilisearchClient(url=cfg.meilisearch.url, api_key=cfg.meilisearch.api_key)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize Meilisearch client: %s", exc)

    if cfg.typesense.enabled:
        try:
            return TypesenseClient(
                host=cfg.typesense.host,
                port=cfg.typesense.port,
                protocol=cfg.typesense.protocol,
                api_key=cfg.typesense.api_key,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize Typesense client: %s", exc)

    if cfg.opensearch.enabled:
        try:
            return OpenSearchClient(
                hosts=cfg.opensearch.hosts,
                username=cfg.opensearch.username,
                password=cfg.opensearch.password,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize OpenSearch client: %s", exc)

    if cfg.algolia.enabled and cfg.algolia.app_id and cfg.algolia.api_key:
        try:
            return AlgoliaSearchClient(
                app_id=cfg.algolia.app_id,
                api_key=cfg.algolia.api_key,
                default_index=cfg.algolia.default_index,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize Algolia client: %s", exc)

    logger.info("No additional search provider is enabled.")
    return None


__all__ = [
    "ISearchClient",
    "MeilisearchClient",
    "TypesenseClient",
    "OpenSearchClient",
    "AlgoliaSearchClient",
    "build_search_client",
]

