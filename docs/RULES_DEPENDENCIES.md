# Component Rules: Dependencies (FastAPI DI)

This file defines rules for writing dependencies under `dependencies/**`.

## Where dependencies belong

1. Shared dependencies go in the appropriate module:
   1. `dependencies/db.py` for DB session.
   2. `dependencies/utilities/**` for shared utilities.
   3. `dependencies/repositiories/**` for repository factories.
   4. `dependencies/services/**` for service factories.
2. Each dependency module should export `*Dependency` classes (and optionally `__all__`).

## Core principles

1. Dependencies must be pure in the sense that they only *create/return* objects; they must not execute domain logic.
2. Dependencies must support FastAPI request scoping via parameters when needed.
3. Avoid global mutable state. If shared state is required, encapsulate it in configuration/singletons.

## Required interface

1. Use `class <Thing>Dependency:` naming (example: `UserRepositoryDependency`).
2. Implement `@staticmethod def derive(...):` as the factory/producer FastAPI uses.
3. Ensure `derive()` returns either:
   1. A shared instance (for DB/cache sessions), or
   2. A callable factory that accepts request context and returns a repository/service instance.

## Typing rules (strict)

1. Avoid `Any`. Return concrete types or typed factories: `Callable[..., SomeRepo]`.
2. Fully type the factory signature when returning a factory:
   1. Use `Callable[[...], SomeType]`.
   2. Use explicit `dict[str, X]` types instead of raw dicts.
3. Use `-> Session` / `-> Redis` / `-> <Service>` return annotations.

## Naming and imports

1. Keep dependency naming consistent with its target:
   1. `UserRepositoryDependency` must create/return `repositories.user.UserRepository`.
   2. `UserLoginServiceDependency` must create/return `services.user.login.UserLoginService`.
2. Export only what routes/controllers need.

## Testing rules

1. Unit test dependencies by asserting they return the correct type.
2. In controller tests, mock dependencies rather than patching repository/service internals.

