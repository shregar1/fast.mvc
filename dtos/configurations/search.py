"""
Configuration DTOs for search providers beyond Elasticsearch.

Includes Meilisearch, Typesense, OpenSearch, and Algolia.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class MeilisearchConfigDTO(BaseModel):
    enabled: bool = False
    url: str = "http://localhost:7700"
    api_key: Optional[str] = None


class TypesenseConfigDTO(BaseModel):
    enabled: bool = False
    host: str = "localhost"
    port: int = 8108
    protocol: str = "http"
    api_key: Optional[str] = None


class OpenSearchConfigDTO(BaseModel):
    enabled: bool = False
    hosts: list[str] = ["http://localhost:9200"]
    username: Optional[str] = None
    password: Optional[str] = None


class AlgoliaConfigDTO(BaseModel):
    enabled: bool = False
    app_id: Optional[str] = None
    api_key: Optional[str] = None
    default_index: Optional[str] = None


class SearchConfigurationDTO(BaseModel):
    """
    Aggregated configuration for additional search providers.
    """

    meilisearch: MeilisearchConfigDTO = MeilisearchConfigDTO()
    typesense: TypesenseConfigDTO = TypesenseConfigDTO()
    opensearch: OpenSearchConfigDTO = OpenSearchConfigDTO()
    algolia: AlgoliaConfigDTO = AlgoliaConfigDTO()


__all__ = [
    "MeilisearchConfigDTO",
    "TypesenseConfigDTO",
    "OpenSearchConfigDTO",
    "AlgoliaConfigDTO",
    "SearchConfigurationDTO",
]

