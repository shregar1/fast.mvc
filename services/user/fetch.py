"""FetchUser Service."""
from abstractions.service import IService
from dtos.requests.apis.v1.user.fetch import FetchUserRequestDTO
from repositories.user.fetch import FetchUserRepository

class FetchUserService(IService):
    def __init__(self, repo: FetchUserRepository, **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def run(self, request_dto: FetchUserRequestDTO) -> dict:
        self.logger.info("Executing fetch service")
        return { "item": { "id": "1" }, "message": "Success" }
