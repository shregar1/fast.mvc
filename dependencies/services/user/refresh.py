"""
User Refresh Service Dependency.
"""

from collections.abc import Callable

from abstractions.dependency import IDependency
from services.user.refresh import UserRefreshService
from start_utils import logger


class UserRefreshServiceDependency(IDependency):
    """FastAPI dependency provider for UserRefreshService."""

    @staticmethod
    def derive() -> Callable:
        logger.debug("UserRefreshServiceDependency factory created")

        def factory(
            urn: str,
            user_urn: str,
            api_name: str,
            user_id: str,
            jwt_utility,
        ) -> UserRefreshService:
            return UserRefreshService(
                urn=urn,
                user_urn=user_urn,
                api_name=api_name,
                user_id=user_id,
                jwt_utility=jwt_utility,
            )

        return factory
