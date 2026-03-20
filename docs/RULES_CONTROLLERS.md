# Component Rules: Controllers

This file defines rules for writing HTTP controllers in `controllers/**`.

## Where controllers belong

1. Versioned business endpoints live in `controllers/apis/v1/**`.
2. User-facing auth/session endpoints live in `controllers/user/**`.
3. Routing entry points:
   1. `controllers/apis/v1/__init__.py` wires nested routers under `/api/v1`.
   2. Feature folders should expose an `APIRouter` from their own `__init__.py` when using nested routing.
   3. User router is `controllers/user/__init__.py`.

## Core principles

1. Controllers are orchestration: validate inputs (via DTOs), call services, return standardized responses.
2. Controllers must not contain business rules or DB query logic. Push those to services/repositories.
3. Controllers must return FastAPI responses that match endpoint expectations (`JSONResponse`, `RedirectResponse`, `StreamingResponse`, or `Response` for streaming unions).

## Class-based controllers (required by repo convention)

1. API controllers should inherit from `controllers/apis/abstraction.py` / `controllers/apis/v1/abstraction.py` or implement the correct interface for the layer.
2. User controllers should inherit from `controllers/user/abstraction.IUserController`.
3. Each controller class should expose methods named after the HTTP operation (`get`, `post`, `patch`, `delete`, `put`) and referenced via `ControllerClass().get` etc.
4. If a module currently has function endpoints, wrap them in a class controller before wiring routes (until fully refactored).

## Error handling rules

1. Catch known domain/HTTP errors and map them into `BaseResponseDTO` plus the error HTTP code.
2. Always include `transactionUrn` (use `request.state.urn` or `self.urn`).
3. For unknown exceptions:
   1. log the exception with request context
   2. return `error_internal_server_error`

## Strict typing rules

1. Prefer concrete return types.
2. For streaming endpoints where return types vary, annotate with `starlette.responses.Response` to avoid FastAPI response-field validation issues.
3. Avoid `dict` without type parameters; prefer `dict[str, object]` / `TypedDict`.
4. Use `TypedDict` for SSE payload schemas and keep them synchronized with documentation.

## Nested routing rules (new structure)

1. Each feature folder should define its own `APIRouter` in `controllers/apis/v1/<feature>/__init__.py` and register only relative paths.
2. The top-level `controllers/apis/v1/__init__.py` should `include_router()` those routers instead of repeating route registrations.
3. Ensure static paths are registered before any dynamic capture paths (FastAPI route ordering).

## Testing rules

1. Add unit tests for controller behavior (especially streaming event ordering).
2. Controller tests should mock services/repositories when possible.

