# Component Rules: Errors

This file defines rules for writing and using custom errors in `errors/**`.

## Core principles

1. Errors should be typed domain/HTTP exceptions, not plain `Exception`.
2. Controllers catch known errors and convert them into `BaseResponseDTO` responses.
3. Services should raise errors instead of returning error responses.

## Required error attributes

Every custom error must expose:

1. `responseMessage` (human readable)
2. `responseKey` (machine-readable key for client translation)
3. `httpStatusCode` (integer HTTP status)

## Error categorization

1. Use `BadInputError` for validation and malformed input.
2. Use `NotFoundError` for missing resources.
3. Use `UnauthorizedError` / `ForbiddenError` for authz/authn failures.
4. Use `UnexpectedResponseError` for external integration failures and inconsistent states.
5. Use `RateLimitError` when throttling applies.

## Controllers must

1. Catch known errors and map directly:
   1. `responseMessage`, `responseKey`, and `httpStatusCode`
2. Catch unknown exceptions and return:
   1. `responseKey = "error_internal_server_error"`
   2. `responseMessage` generic user message
3. Always include `transactionUrn`.

## Strict typing rules

1. Errors should be deterministic and should not mutate their own attributes after initialization.
2. Avoid dynamic error payload dicts unless strongly typed.

