"""
Configuration DTOs for graph databases.

Initial support focuses on Neo4j, with room for additional providers.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Neo4jConfigDTO(BaseModel):
    enabled: bool = False
    uri: str = "bolt://localhost:7687"
    user: Optional[str] = "neo4j"
    password: Optional[str] = "password"
    database: Optional[str] = None


class GraphConfigurationDTO(BaseModel):
    neo4j: Neo4jConfigDTO = Neo4jConfigDTO()


__all__ = ["Neo4jConfigDTO", "GraphConfigurationDTO"]

