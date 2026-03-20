# Component Rules: Models (SQLAlchemy ORM)

This file defines rules for writing ORM models in `models/**`.

## Core principles

1. Models define DB schema: columns, relationships, indexes, and constraints.
2. Business rules belong in services; models should remain “data-only”.
3. Use soft deletes consistently:
   1. models should include `is_deleted` (or equivalent)
   2. repositories/services should filter appropriately

## Required fields and conventions

1. Include audit fields where the repo expects them:
   1. `created_at`, `created_by`
   2. `updated_at`, `updated_by`
2. Use URN fields as external identifiers where the repo expects URNs:
   1. field naming: `urn`
   2. format: `urn:<entity>:<ulid>`
3. Use snake_case column names.
4. Table names should follow existing repo convention (lowercase, typically singular).

## Typing and mappings

1. Ensure column types match actual DB schema and migrations.
2. Document columns with docstrings/comments when intent is not obvious.

## Migrations

1. Any model change that alters schema must be accompanied by a migration under `migrations/versions/**`.
2. Migrations must be deterministic and safe to run in order.

## Testing rules

1. Prefer repository/service tests to validate model behavior end-to-end.
2. Add targeted tests for critical relationships and computed fields.

