"""Test and tooling factories for API payloads and domain objects.

Layout mirrors ``controllers/apis/...`` and ``dtos/requests/apis/...``, e.g.
``factories/apis/v1/example/fetch`` for GET-style payloads and ``create`` / ``patch`` / … for writes.
"""

from factories.apis.v1.example import (
    ExampleCreateRequestFactory,
    ExampleDeleteRequestFactory,
    ExampleFetchRequestFactory,
    ExamplePatchRequestFactory,
    ExamplePutRequestFactory,
    ExampleUpdateRequestFactory,
)

__all__ = [
    "ExampleCreateRequestFactory",
    "ExampleDeleteRequestFactory",
    "ExampleFetchRequestFactory",
    "ExamplePatchRequestFactory",
    "ExamplePutRequestFactory",
    "ExampleUpdateRequestFactory",
]
