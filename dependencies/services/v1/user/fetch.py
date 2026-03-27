"""FetchUser Dependencies."""
from fastapi import Request
from abstractions.dependency import IDependency
from services.user.fetch import FetchUserService
from repositories.user.fetch import FetchUserRepository

class FetchUserServiceDependency(IDependency):
    @staticmethod
    def derive(request: Request) -> FetchUserService:
        repo = FetchUserRepository(urn=getattr(request.state, "urn", None))
        return FetchUserService(repo=repo, urn=getattr(request.state, "urn", None))
