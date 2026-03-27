"""Repository dependency abstraction."""

from abstractions.dependency import IDependency


class IRepositoryDependency(IDependency):
    """Root injectable dependency for repository factories under ``dependencies/repositories``."""
