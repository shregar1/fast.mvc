# Component Rules: Tests

This file defines rules for writing tests in `tests/**`.

## Where tests belong

1. Unit tests: `tests/unit/**` for deterministic logic (DTO validation, service behavior, controller streaming helpers).
2. Integration tests: `tests/integration/**` for multi-component flows with a DB (as applicable).
3. E2E tests: `tests/e2e/**` for contract-level API behavior.

## Core principles

1. Tests should cover both success paths and failure paths.
2. For streaming endpoints (SSE), tests must validate event ordering and the `done` semantics.
3. For strict typing, keep tests typed as well:
   1. prefer `TypedDict` for fake SSE payloads
   2. annotate mocks and local variables

## Mocking rules

1. Mock external I/O:
   1. HTTP calls (mock `httpx.AsyncClient` or relevant client)
   2. file storage (mock `IFileStorage` implementations)
   3. queues/brokers (mock producers/consumers)
2. Prefer injecting fakes via constructor arguments or dependency overrides rather than patching internals.

## FastAPI controller tests

1. Use `TestClient` or `httpx.AsyncClient` with the FastAPI app.
2. For endpoints that return `StreamingResponse`, validate the streaming body by iterating the async generator.
3. Ensure tests assert:
   1. response headers (e.g. `content-type: text/event-stream`)
   2. schema shape of each SSE event
   3. that the final `done` event is emitted

## Coverage rules

1. Respect the repo coverage gate (`--cov-fail-under`).
2. When debugging an isolated failure, adjust coverage threshold locally, but restore proper thresholds for final runs.

