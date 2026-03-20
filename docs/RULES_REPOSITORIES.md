# Component Rules: Repositories

This file defines rules for data access in `repositories/**`.

## Where repositories belong

1. Repository modules implement DB queries and mapping from ORM models to `to_dict()` payloads.
2. Repository files typically import SQLAlchemy models from `models/**`.
3. Repositories should be wired via dependency factories (`dependencies/repositiories/**`).

## Core principles

1. Repositories encapsulate data access and query composition.
2. Repositories must not contain business policy decisions (those belong in services/controllers).
3. Repositories must always scope queries to request context for logging:
   1. `urn`
   2. `user_urn`
   3. `api_name`
   4. `user_id`
4. Respect soft-delete:
   1. ensure `is_deleted` filtering is applied where the repository expects it.

## Type and API rules

1. Prefer strongly typed method parameters (ids as `int`, URNs as `str`, statuses as `str | None`, etc).
2. Prefer typed return values or explicit conversion:
   1. Return ORM models only when the service expects that.
   2. Otherwise return `to_dict()` results or typed DTOs.
3. Avoid `Any` and untyped dicts.

## Caching and performance

1. If the repository provides caching, ensure cache invalidation happens on writes.
2. Log slow queries consistently with repo timing helpers.

## Testing rules

1. Repository tests should use a test DB or a mocked session.
2. Assert that soft-delete filtering and ordering/limit logic is correct.

