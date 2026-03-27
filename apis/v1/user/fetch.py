"""V1 API FetchUser Controller."""
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from apis.v1.abstraction import IV1APIController  # Reuse v1 abstraction if base is similar
from dependencies.services.v1.user.fetch import FetchUserServiceDependency
from services.user.fetch import FetchUserService
from dtos.requests.apis.v1.user.fetch import FetchUserRequestDTO
from dtos.responses.base import BaseResponseDTO
from constants.api_status import APIStatus

class FetchUserAPIController(IV1APIController):
    async def execute(self, request: Request, payload: FetchUserRequestDTO, service: FetchUserService = Depends(FetchUserServiceDependency.derive)) -> JSONResponse:
        async def _run():
            result = service.run(payload)
            return self._to_json_response(BaseResponseDTO(transactionUrn=request.state.urn, status=APIStatus.SUCCESS, data=result["item"]))
        return await self.invoke_with_exception_handling(request, _run)
