"""
Grouped DTOs for datastore-related configuration.
"""

from pydantic import BaseModel

from dtos.configurations.cache import CacheConfigurationDTO
from dtos.configurations.cassandra import CassandraConfigurationDTO
from dtos.configurations.cosmos import CosmosConfigurationDTO
from dtos.configurations.db import DBConfigurationDTO
from dtos.configurations.dynamo import DynamoConfigurationDTO
from dtos.configurations.elasticsearch import ElasticsearchConfigurationDTO
from dtos.configurations.mongo import MongoConfigurationDTO
from dtos.configurations.scylla import ScyllaConfigurationDTO


class DatastoresConfigurationDTO(BaseModel):
    """
    Aggregate configuration for all datastore technologies used by FastMVC.

    This groups relational, document, wide-column, key-value, and search
    backends under a single object for convenience.
    """

    db: DBConfigurationDTO
    cache: CacheConfigurationDTO
    mongo: MongoConfigurationDTO
    cassandra: CassandraConfigurationDTO
    scylla: ScyllaConfigurationDTO
    dynamo: DynamoConfigurationDTO
    cosmos: CosmosConfigurationDTO
    elasticsearch: ElasticsearchConfigurationDTO


__all__ = [
    "DatastoresConfigurationDTO",
]

