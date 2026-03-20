# Component Rules: Configurations

This file defines rules for configuration classes in `configurations/**` and JSON config files in `config/**`.

## Core principles

1. Configuration loading must happen at startup (or first access) and be validated early.
2. Configuration classes should be singletons to avoid repeated parsing/loading.
3. Configuration must never contain secrets committed to git. Treat credentials as environment-specific and exclude them from commits.

## Required patterns

1. Configuration classes should expose:
   1. `get_config()` returning a Pydantic DTO
   2. `instance()` (singleton accessor) where the repo convention requires it
2. Use DTOs for validation and typing:
   1. e.g. `DBConfigurationDTO`, `CacheConfigurationDTO`

## Environment overrides

1. Support environment variable overrides for sensitive or environment-specific values.
2. Overrides must not crash startup if the env var is missing or invalid; use safe defaults and log warnings.

## Strict typing rules

1. Configuration DTO fields must be typed (no `Any`).
2. Parsing functions must validate types and range constraints.

## Error handling rules

1. Handle missing config files gracefully (log and fall back to defaults).
2. Handle invalid JSON gracefully (log and fall back).

## Testing rules

1. Unit test configuration defaults and override behavior where feasible.
2. Ensure shim/default config modules match expected DTO shapes.

