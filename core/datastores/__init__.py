"""
Concrete ``IDataStore`` / search adapters for Redis, Mongo, Cassandra, Dynamo, etc.

**Also use the dedicated packages (do not duplicate their concerns here):**

- **SQLAlchemy / relational:** ``fast_db`` (engines, sessions, FastAPI dependencies).
- **Object storage (S3, GCS, Azure Blob):** ``fast_storage`` (``build_storage_backend``, …).

This package only holds thin driver wrappers that implement ``abstractions.datastore``.
"""

from .redis_kv import RedisKeyValueStore  # noqa: F401
from .mongo import MongoDocumentStore  # noqa: F401
from .cassandra import CassandraWideColumnStore  # noqa: F401
from .scylla import ScyllaWideColumnStore  # noqa: F401
from .dynamo import DynamoKeyValueStore  # noqa: F401
from .cosmos import CosmosDocumentStore  # noqa: F401
from .elasticsearch import ElasticsearchSearchStore  # noqa: F401

__all__ = [
    "RedisKeyValueStore",
    "MongoDocumentStore",
    "CassandraWideColumnStore",
    "ScyllaWideColumnStore",
    "DynamoKeyValueStore",
    "CosmosDocumentStore",
    "ElasticsearchSearchStore",
]

