"""Example-domain services."""

from services.example.abstraction import IExampleService
from services.example.example_service import ExampleService

__all__ = ["IExampleService", "ExampleService"]
