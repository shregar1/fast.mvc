"""v1 example API controllers."""

from controllers.apis.v1.example.abstraction import IExampleAPIController
from controllers.apis.v1.example.create import ExampleCreateController

__all__ = ["IExampleAPIController", "ExampleCreateController"]
