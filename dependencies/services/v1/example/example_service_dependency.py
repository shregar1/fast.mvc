"""FastAPI dependency for :class:`services.example.example_service.ExampleService`."""

from fastapi import Depends, Request

from dependencies.repositories.example.example_repository_dependency import (
    ExampleRepositoryDependency,
)
from dependencies.services.v1.example.abstraction import IExampleServiceDependency
from repositories.example.example_repository import ExampleRepository
from services.example.example_service import ExampleService


class ExampleServiceDependency(IExampleServiceDependency):
    """Derives an :class:`ExampleService` from the current request and repository."""

    @staticmethod
    def derive(
        request: Request,
        repository: ExampleRepository = Depends(ExampleRepositoryDependency.derive),
    ) -> ExampleService:
        """Build a service instance with context from request state."""
        urn = getattr(request.state, "urn", None)
        user_urn = getattr(request.state, "user_urn", None)
        user_id = getattr(request.state, "user_id", None)
        api_name = getattr(request.state, "api_name", None) or "example_api"

        return ExampleService(
            example_repo=repository,
            urn=urn,
            user_urn=user_urn,
            user_id=user_id,
            api_name=api_name,
        )
