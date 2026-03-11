"""
Main FastAPI application entry point. Sets up middleware, routers,
and configuration for the FastMVC API.
"""
import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from http import HTTPStatus
from loguru import logger

from constants.api_status import APIStatus
from constants.default import Default
from controllers.user import router as UserRouter
from dtos.responses.base import BaseResponseDTO
from errors.unexpected_response_error import UnexpectedResponseError

from middlewares.authetication import AuthenticationMiddleware
from middlewares.rate_limit import (
    RateLimitMiddleware, RateLimitConfig
)
from middlewares.security_headers import (
    SecurityHeadersMiddleware,
    SecurityHeadersConfig
)
from middlewares.request_context import RequestContextMiddleware


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        logger.warning(
            f"Invalid integer value for environment variable {name!r}: "
            f"{value!r}. Falling back to default {default!r}."
        )
        return default


app = FastAPI()

load_dotenv()
HOST = os.getenv("HOST", "0.0.0.0")
PORT: int = _get_int_env("PORT", 8000)
RATE_LIMIT_REQUESTS_PER_MINUTE: int = _get_int_env(
    "RATE_LIMIT_REQUESTS_PER_MINUTE",
    Default.RATE_LIMIT_REQUESTS_PER_MINUTE,
)
RATE_LIMIT_REQUESTS_PER_HOUR: int = _get_int_env(
    "RATE_LIMIT_REQUESTS_PER_HOUR",
    Default.RATE_LIMIT_REQUESTS_PER_HOUR,
)
RATE_LIMIT_WINDOW_SECONDS: int = _get_int_env(
    "RATE_LIMIT_WINDOW_SECONDS",
    Default.RATE_LIMIT_WINDOW_SECONDS,
)
RATE_LIMIT_BURST_LIMIT: int = _get_int_env(
    "RATE_LIMIT_BURST_LIMIT",
    Default.RATE_LIMIT_BURST_LIMIT,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors and return a structured JSON response.
    """
    logger.error(f"error: {exc.errors()}")
    for error in exc.errors():
        if "ctx" in error:
            error.pop("ctx")
    response_payload: dict = {
        "transactionUrn": getattr(request.state, "urn", None),
        "responseMessage": "Bad or missing input.",
        "responseKey": "error_bad_input",
        "errors": exc.errors(),
    }
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content=response_payload,
    )


@app.exception_handler(UnexpectedResponseError)
async def unexpected_response_error_handler(
    request: Request, exc: UnexpectedResponseError
):
    """
    Handle application-specific unexpected response errors with a structured payload.
    """
    urn = getattr(request.state, "urn", None) or ""
    logger.error(
        f"UnexpectedResponseError occurred: {exc.responseMessage} "
        f"(key={exc.responseKey}, status={exc.httpStatusCode})",
        urn=urn,
    )
    response_dto = BaseResponseDTO(
        transactionUrn=urn,
        status=APIStatus.FAILED,
        responseMessage=exc.responseMessage,
        responseKey=exc.responseKey,
        data={},
        errors=None,
    )
    return JSONResponse(
        status_code=exc.httpStatusCode,
        content=response_dto.model_dump(),
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unhandled exceptions to avoid leaking internals.
    """
    urn = getattr(request.state, "urn", None) or ""
    logger.exception(
        "Unhandled exception occurred while processing request.", urn=urn
    )
    response_dto = BaseResponseDTO(
        transactionUrn=urn,
        status=APIStatus.FAILED,
        responseMessage="Internal server error.",
        responseKey="error_internal_server_error",
        data={},
        errors=None,
    )
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=response_dto.model_dump(),
    )


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    logger.info("Health check endpoint called")
    return {"status": "ok"}


app.add_middleware(middleware_class=TrustedHostMiddleware, allowed_hosts=["*"])
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

logger.info("Initialising middleware stack")
security_config = SecurityHeadersConfig(
    enable_hsts=True,
    enable_csp=True,
    hsts_max_age=31536000,
    hsts_include_subdomains=True
)
app.add_middleware(SecurityHeadersMiddleware, **security_config.__dict__)
rate_limit_config = RateLimitConfig(
    requests_per_minute=RATE_LIMIT_REQUESTS_PER_MINUTE,
    requests_per_hour=RATE_LIMIT_REQUESTS_PER_HOUR,
    burst_limit=RATE_LIMIT_BURST_LIMIT,
    enable_sliding_window=True,
    enable_token_bucket=False
)
app.add_middleware(RateLimitMiddleware, config=rate_limit_config)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(RequestContextMiddleware)
logger.info("Initialised middleware stack")

logger.info("Initialising routers")
# USER ROUTER
app.include_router(UserRouter)
logger.info("Initialised routers")


@app.on_event("startup")
async def on_startup():
    """
    Application startup event handler.
    """
    logger.info("Application startup event triggered")


@app.on_event("shutdown")
async def on_shutdown():
    """
    Application shutdown event handler.
    """
    logger.info("Application shutdown event triggered")

if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
