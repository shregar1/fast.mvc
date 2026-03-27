"""Example API router."""

from http import HTTPStatus
from fastapi import APIRouter, Request
from controllers.apis.v1.example.create import ExampleCreateController
from dtos.responses.I import IResponseDTO

router = APIRouter(prefix="/example", tags=["Example"])
controller = ExampleCreateController()


@router.post("", response_model=IResponseDTO, status_code=HTTPStatus.CREATED)
async def create_example(request: Request, payload: dict) -> IResponseDTO:
    """Create an example via class-Id controller."""
    # Context injected from RequestContextMiddleware by starlette request state
    request.state.api_name = "create_example"
    urn = getattr(request.state, "urn", "urn:req:default")
    user_urn = getattr(request.state, "user_urn", "")
    user_id = getattr(request.state, "user_id", "")

    return await controller.handle_create_example(
        request=request,
        urn=urn,
        user_urn=user_urn,
        payload=payload,
        headers=dict(request.headers),
        api_name="create_example",
        user_id=str(user_id),
    )
