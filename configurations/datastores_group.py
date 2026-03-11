"""
Datastores Configuration Aggregator.

Provides a single access point (`DatastoresConfiguration`) that aggregates
all datastore-related configuration DTOs into a `DatastoresConfigurationDTO`.
"""

from typing import Optional

from configurations.cache import CacheConfiguration
from configurations.cassandra import CassandraConfiguration
from configurations.cosmos import CosmosConfiguration
from configurations.db import DBConfiguration
from configurations.dynamo import DynamoConfiguration
from configurations.elasticsearch import ElasticsearchConfiguration
from configurations.mongo import MongoConfiguration
from configurations.scylla import ScyllaConfiguration
from dtos.configurations.datastores import DatastoresConfigurationDTO


class DatastoresConfiguration:
    """
    Aggregated configuration for all datastore technologies.

    Example:
        cfg = DatastoresConfiguration().get_config()
        db_cfg = cfg.db
        redis_cfg = cfg.cache
        mongo_cfg = cfg.mongo
    """

    _instance: Optional["DatastoresConfiguration"] = None

    def __new__(cls) -> "DatastoresConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_config(self) -> DatastoresConfigurationDTO:
        """
        Load all datastore configurations and return a grouped DTO.
        """
        return DatastoresConfigurationDTO(
            db=DBConfiguration().get_config(),
            cache=CacheConfiguration().get_config(),
            mongo=MongoConfiguration().get_config(),
            cassandra=CassandraConfiguration().get_config(),
            scylla=ScyllaConfiguration().get_config(),
            dynamo=DynamoConfiguration().get_config(),
            cosmos=CosmosConfiguration().get_config(),
            elasticsearch=ElasticsearchConfiguration().get_config(),
        )

