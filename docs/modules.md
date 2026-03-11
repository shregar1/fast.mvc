## Modules Overview

FastMVC ships with rich, package-level documentation in the repository itself. This page is a high-level index that you can use as a sidebar entry in a docs site, while linking to the existing `README.md` files in each package.

### Core Packages

- **Abstractions** (`abstractions/README.md`):  
  Base interfaces and contracts such as `IController`, `IService`, and `IRepository`. These define how controllers, services, and repositories interact in the MVC pattern.

- **Configurations** (`configurations/README.md`):  
  Configuration loaders and helpers for database, cache, security, and optional services. Uses Pydantic DTOs and supports environment-variable overrides.

- **Constants** (`constants/README.md`):  
  Application-wide constants and default values (e.g., default pagination, status codes, environment names).

- **Controllers** (`controllers/README.md`):  
  HTTP route handlers that receive validated DTOs, call services, and return standardized responses.

- **Dependencies** (`dependencies/README.md`):  
  Dependency injection factories for repositories, services, and external clients. Used with FastAPI’s `Depends`.

- **DTOs** (`dtos/README.md`):  
  Request and response DTOs for input validation and output shaping, including configuration DTOs under `dtos/configurations/`.

- **Errors** (`errors/README.md`):  
  Custom exception hierarchy (e.g. `BadInputError`, `NotFoundError`) used across services and controllers.

- **Middlewares** (`middlewares/README.md`):  
  Extra application-level middlewares on top of `fastmvc-middleware` (authentication hooks, additional logging, etc.).

- **Migrations** (`migrations/README.md`):  
  Alembic configuration and migration scripts, wired to the `fastmvc migrate` CLI commands.

- **Models** (`models/README.md`):  
  SQLAlchemy models that back the repository layer.

- **Repositories** (`repositories/README.md`):  
  Data access layer built on top of SQLAlchemy (and other datastores if enabled), exposing rich filtering and CRUD helpers.

- **Services** (`services/README.md`):  
  Business logic layer, including user services, domain services, and API-specific services. Implements error handling patterns and response DTOs.

- **Utilities** (`utilities/README.md`):  
  Helper functions, cross-cutting utilities, and shared support code.

- **Core module** (`core/README.md`):  
  Enterprise features such as health checks, observability (logging/metrics/tracing), resilience (circuit breaker, retry), tasks, security (API keys, webhooks, encryption), feature flags, tenancy, versioning, and testing helpers.

### CLI Package

- **CLI** (`fastmvc_cli/README.md`):  
  Documentation for the `fastmvc` command-line interface, including:
  - `generate` and `init` for project creation.
  - `add entity` and `add service` for scaffolding into existing projects.
  - `migrate` for Alembic migrations.
  - `info` and `version` commands.

This page is intended as a single index entry in your docs site; for deep dives, use links to the per-package `README.md` files or the more focused docs pages like [`cli.md`](cli.md), [`architecture.md`](architecture.md), and [`configuration.md`](configuration.md).

