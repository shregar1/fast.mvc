"""v1 example service dependency abstraction."""

from dependencies.services.v1.abstraction import IV1ServiceDependency


class IExampleServiceDependency(IV1ServiceDependency):
    """Interface for v1 example-scoped service dependencies."""
