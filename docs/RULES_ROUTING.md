# Nested Routing Pattern Rules (FastAPI)

This rule set standardizes how routes are declared and wired using nested `APIRouter` objects inside `controllers/**`.

These rules are required for the `controllers/apis/v1/**` nested routing refactor.

## Goals

1. Make route wiring deterministic and easy to scan.
2. Ensure every route belongs to exactly one feature folder router.
3. Prevent accidental duplicate route registration.
4. Keep path matching correct by enforcing static-before-dynamic registration.

## Folder-to-path mapping

1. For v1 endpoints, the public prefix is always `/api/v1` (set by `controllers/apis/__init__.py` + `controllers/apis/v1/__init__.py`).
2. Inside `controllers/apis/v1/<feature>/__init__.py`, each feature router must declare its own `prefix` matching the public API path segment.
   - Example: `controllers/apis/v1/document/__init__.py` uses `prefix="/documents"` even if the folder name is singular.

## Feature router contract (mandatory)

Each feature folder that owns routes must:

1. Contain an `__init__.py` that exports an `APIRouter` instance named `router`.
2. Register only feature-relative paths:
   - Use `path=""` for “prefix root” endpoints.
   - Use `path="/{id}"`, `path="/subpath"`, etc. relative to the router’s `prefix`.
3. Use endpoint implementations already present in the feature’s submodules:
   - Controllers may be class-based (`ControllerClass().get/post/...`) or function-based (allowed temporarily), but the routing must still live in this feature folder router.
4. End the file with:
   - `__all__ = ["router"]`

## Top-level wiring contract (mandatory)

`controllers/apis/v1/__init__.py` must:

1. Import every feature router you want registered (explicit imports; no wildcard import).
2. Call `router.include_router(<feature>_router)` exactly once per feature router.
3. Never declare routes using `router.add_api_route(...)` for paths that are owned by a feature folder router.
   - This is the main safety rule to prevent duplicate registrations.

## Static vs dynamic path registration

FastAPI/Starlette path matching is order-sensitive when dynamic captures could shadow static routes.

Inside any feature router, register in this order:

1. Static routes first:
   - e.g. `/dashboard`, `/deliveries`, `/url`, `/download`, etc.
2. Dynamic capture routes last:
   - e.g. `/{webhook_id}`, `/{document_id}`, `/{session_id}`, etc.

If you need to guarantee ordering, do it by:
1. defining the static routes before dynamic routes in code
2. avoiding ambiguous patterns that differ only by parameter names

## SSE / Streaming typing rule

For endpoints that may return `StreamingResponse` (or other Starlette `Response` objects in union types):

1. Prefer annotating the endpoint return type as `starlette.responses.Response`.
2. Do not use complex unions like `JSONResponse | StreamingResponse` in a way that triggers FastAPI response-field validation errors.

## Testing rule (recommended)

1. Add/extend route wiring tests (or endpoint tests) to ensure:
   - each expected path is registered
   - `include_router` wiring has no missing routes
   - no duplicate routes are created
2. For SSE endpoints, validate event ordering and final `done` event semantics.

