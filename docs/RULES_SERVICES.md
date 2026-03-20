# Component Rules: Services

This file defines rules for writing business logic in `services/**`.

## Where services belong

1. Feature-specific services live in `services/<domain>/**` (example: `services/user/login.py`).
2. Service modules should export service classes (and optionally factories if used elsewhere).

## Core principles

1. Services own business logic and workflows.
2. Services must not depend on FastAPI `Request` or `Depends()` directly.
3. Services must not create SQLAlchemy sessions globally; accept repositories or use repository instances injected via constructor/factories.
4. Services must raise custom errors for exceptional conditions; controllers translate those into HTTP responses.

## Service API shape

1. Services generally implement:
   1. `__init__(urn, user_urn, api_name, user_id, ...)` for request context.
   2. `async def run(...):` or `async def get_current(...):` depending on the endpoint.
2. Return `BaseResponseDTO` (or payload objects that controllers embed into `BaseResponseDTO`), matching repo conventions.

## Strict typing rules

1. Do not return raw JSON objects from services unless controllers expect that exact structure.
2. Avoid `Any` and untyped dicts.
3. Use explicit DTO types for inputs and explicit response DTO types for outputs where possible.

## Error handling rules

1. Raise typed domain errors (from `errors/**`) instead of returning error responses.
2. Ensure each raised error includes:
   1. `responseMessage`
   2. `responseKey`
   3. `httpStatusCode`

## Testing rules

1. Unit test services by exercising business flows and expecting raised errors.
2. Mock repositories and external integrations.

