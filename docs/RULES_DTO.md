# Component Rules: DTOs

This file defines rules for writing Data Transfer Objects (DTOs) in `dtos/**`.

## Where DTOs belong

1. Request DTOs live in `dtos/requests/**`.
2. Response DTOs live in `dtos/responses/**`.
3. Shared abstractions live in `dtos/**/abstraction.py` and `dtos/base.py`.

## Core principles

1. DTOs must be used for input validation and output shaping at layer boundaries.
2. Controllers should accept request DTOs and return response DTOs (directly or via `BaseResponseDTO.model_dump()`).
3. DTOs must not perform I/O (no HTTP calls, no DB sessions, no file access).
4. DTOs must be “security-first”: inherit from `EnhancedBaseModel` for user-facing inputs.

## Request DTO requirements

1. Inherit from `dtos.base.EnhancedBaseModel` for all user-provided inputs.
2. Ensure `extra = "forbid"` so unknown fields are rejected.
3. Prefer explicit field types (`str | int | bool | datetime | UUID`, etc).
4. Use `Field(..., description="...")` for any field that appears in OpenAPI.
5. For optional inputs use `Optional[T]` or `T | None` and ensure the route logic handles `None`.
6. Do not use `Any` in DTOs. If a field is genuinely unstructured, use a typed structure (`TypedDict`, nested `BaseModel`, or constrained `dict` types).

## Reference numbers and request tracking

1. Request DTOs that participate in request tracking should implement `IRequestDTO` (see `dtos/requests/abstraction.py`).
2. `reference_number` (or equivalent) must be a validated UUID-like string per `IRequestDTO`.

## Response DTO requirements

1. All responses should ultimately be shaped as `BaseResponseDTO` (see `dtos/responses/base.py`).
2. Error payloads should use the same response wrapper with `status=APIStatus.FAILED` and `responseKey` matching an error key.
3. Ensure `data` is always JSON-serializable.
4. Response DTOs must not leak internal ORM models directly. Convert using `.to_dict()` or explicit mapping.

## Strict typing rules

1. Use `from __future__ import annotations` where appropriate.
2. Prefer `TypedDict` when you need lightweight typed payloads for JSON/SSE structures.
3. Prefer `Final[str]` for constant keys used by DTOs.
4. Avoid implicit `dict` shapes; specify `dict[str, str]`, `dict[str, object]`, or a dedicated `TypedDict`.

## Serialization rules

1. Use `model_dump()` to serialize DTOs.
2. When controllers need camelCase output, they should pass the DTO dump through `DictionaryUtility.convert_dict_keys_to_camel_case`.
3. Always ensure `datetime` fields can be encoded. `EnhancedBaseModel` already includes datetime encoders; otherwise encode explicitly to ISO 8601.

## Testing rules

1. DTO validation should be covered by unit tests for sanitization and validation edge cases.
2. Tests must assert both “accept” and “reject” scenarios.

