"""Example-scoped v1 factories (CRUD-style helpers for tests and tooling)."""

from factories.apis.v1.example.create import ExampleCreateRequestFactory
from factories.apis.v1.example.delete import ExampleDeleteRequestFactory
from factories.apis.v1.example.fetch import ExampleFetchRequestFactory
from factories.apis.v1.example.patch import ExamplePatchRequestFactory
from factories.apis.v1.example.put import ExamplePutRequestFactory
from factories.apis.v1.example.update import ExampleUpdateRequestFactory

__all__ = [
    "ExampleCreateRequestFactory",
    "ExampleDeleteRequestFactory",
    "ExampleFetchRequestFactory",
    "ExamplePatchRequestFactory",
    "ExamplePutRequestFactory",
    "ExampleUpdateRequestFactory",
]
