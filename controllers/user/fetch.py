"""FetchUser Core Controller."""
from abstractions.controller import IController
from services.user.fetch import FetchUserService
from dtos.requests.apis.v1.user.fetch import FetchUserRequestDTO
from dtos.responses.base import BaseResponseDTO
from constants.api_status import APIStatus

class FetchUserController(IController):
    async def handle(self, urn, payload, api_name) -> BaseResponseDTO:
        await self.validate_request(urn=urn, request_payload=payload, api_name=api_name)
        return BaseResponseDTO(status=APIStatus.SUCCESS, responseMessage="Flow check")
