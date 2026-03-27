"""v1 example API service dependencies."""

from dependencies.services.v1.example.abstraction import IExampleServiceDependency
from dependencies.services.v1.example.example_service_dependency import (
    ExampleServiceDependency,
)

__all__ = ["IExampleServiceDependency", "ExampleServiceDependency"]
