## FastMVC CLI Reference

The `fastmvc` CLI is the main entry point for generating and managing FastMVC projects. It is implemented in `fast_cli/cli.py` and documented here in a docs-friendly format.

### Overview

Top-level command:

```bash
fastmvc [COMMAND] [OPTIONS]
```

Available commands:

- **`generate`**: Create a new FastMVC project from the template.
- **`init`**: Interactive wizard to generate a project (TUI-style).
- **`add`**: Add components (entities, infrastructure services) to an existing project.
- **`migrate`**: Database migrations via Alembic.
- **`info`**: Show FastMVC feature overview and links.
- **`version`**: Print current FastMVC version.

---

### `fastmvc generate`

**Purpose**: Non-interactive project generator suitable for scripts and CI.

```bash
fastmvc generate PROJECT_NAME [OPTIONS]
```

Key options (see `LANDING.md` for the feature matrix):

- **Core**
  - `--output-dir, -o PATH` – where to create the project (default: current directory).
  - `--git / --no-git` – initialize a git repository (default: `--git`).
  - `--venv / --no-venv` – create a virtual environment (default: `--no-venv`).
  - `--install / --no-install` – install dependencies after generation (default: `--no-install`).

- **Datastores**
  - `--with-redis / --no-redis` (default: with Redis)
  - `--with-mongo / --no-mongo`
  - `--with-cassandra / --no-cassandra`
  - `--with-scylla / --no-scylla`
  - `--with-dynamo / --no-dynamo`
  - `--with-cosmos / --no-cosmos`
  - `--with-elasticsearch / --no-elasticsearch`

- **Communications**
  - `--with-email / --no-email`
  - `--with-slack / --no-slack`

- **Observability & telemetry**
  - `--with-datadog / --no-datadog`
  - `--with-telemetry / --no-telemetry`

- **Payments & identity**
  - `--with-payments / --no-payments`
  - `--with-identity / --no-identity`

Example:

```bash
fastmvc generate my_api \
  --output-dir ./projects \
  --with-redis \
  --with-mongo \
  --with-elasticsearch \
  --with-email \
  --with-slack \
  --with-datadog \
  --with-telemetry \
  --with-payments \
  --with-identity
```

The generator wires flags into `ProjectGenerator` and prunes unused configs so the generated project only contains the services you selected.

---

### `fastmvc init`

**Purpose**: Interactive, multi-step project initializer with a TUI-like experience.

```bash
fastmvc init
```

The wizard guides you through:

- **Project details**: name, output directory.
- **Stack & features**:
  - API preset (`auth_only`, `crud`, `admin`).
  - Database backend (`postgres`, `mysql`, `sqlite`).
  - Optional datastores, communications, observability, payments, identity.
  - Feature toggles: auth module, user management, example Product CRUD.
  - Layout: `monolith`, `backend-only`, `backend+worker`.
- **Tooling**:
  - Git, virtualenv, dependency installation.
  - Quality tools: ruff, black, isort, mypy.
  - Pre-commit config, GitHub Actions CI.
  - Optional git remote and initial push.
- **Ports & secrets**:
  - Application port (with conflict detection).
  - DB host/port/name (for non-SQLite).
  - Auto-generated JWT secret and bcrypt salt.
  - CORS origins.

At the end it calls the same `ProjectGenerator` used by `generate` and can also create:

- `LICENSE`
- `CONTRIBUTING.md`
- `CODEOWNERS`
- `pyproject.toml`
- `.pre-commit-config.yaml`
- `.github/workflows/ci.yml`

---

### `fastmvc add`

Group command to enhance an existing FastMVC project (must be run from the project root where `app.py` exists).

```bash
fastmvc add [SUBCOMMAND] ...
```

Subcommands:

- **`fastmvc add entity`** – generate full CRUD for an entity.
- **`fastmvc add service`** – copy infrastructure service configs and DTOs into an existing project.

#### `fastmvc add entity`

```bash
fastmvc add entity ENTITY_NAME [--tests / --no-tests]
```

- `ENTITY_NAME` should be PascalCase (e.g. `Product`, `OrderItem`).
- `--tests / --no-tests` controls whether test files are generated (default: `--tests`).

Generated structure includes:

- `models/<entity>.py`
- `repositories/<entity>.py`
- `services/<entity>/`
- `controllers/<entity>/`
- `dtos/requests/<entity>/`
- `dependencies/repositories/<entity>.py`
- `tests/unit/.../test_<entity>.py`

After generation you typically:

- Import and register the router in `app.py`.
- Generate and apply a migration.

#### `fastmvc add service`

```bash
fastmvc add service [mongo|cassandra|scylla|dynamo|cosmos|elasticsearch|email|slack|datadog|telemetry|payments|identity]
```

This copies config and DTOs from the FastMVC template into your existing project _without_ overwriting existing files:

- For most services: adds `config/<service>/`, `configurations/<service>.py`, `dtos/configurations/<service>.py`.
- For `identity`: also adds `dtos/configurations/identity/` and `services/auth/`.
- For `email`: also adds `services/communications/`.

You then customize the corresponding `config/*/config.json` and restart your app.

---

### `fastmvc migrate`

Group command for Alembic-based database migrations.

```bash
fastmvc migrate [generate|upgrade|downgrade|status|history] [...]
```

Requires `alembic.ini` in your project root.

- **`fastmvc migrate generate "message"`**
  - Creates a new migration.
  - Options:
    - `--autogenerate / --no-autogenerate` (default: `--autogenerate`).

- **`fastmvc migrate upgrade [revision]`**
  - Apply migrations (default: `head`).

- **`fastmvc migrate downgrade [revision]`**
  - Roll back migrations (default: `-1` for previous).

- **`fastmvc migrate status`**
  - Show current migration revision.

- **`fastmvc migrate history [--verbose]`**
  - Show migration history.

The CLI wraps Alembic commands so you can manage migrations without remembering raw `alembic` invocations.

---

### `fastmvc info`

```bash
fastmvc info
```

Prints:

- FastMVC version and Python version.
- High-level feature list (MVC, middleware stack, testing).
- Project layout overview.
- CLI command summary.
- Links to PyPI and documentation.

Useful as a one-glance overview for new team members.

---

### `fastmvc version`

```bash
fastmvc version
```

Outputs:

```text
FastMVC vX.Y.Z
```

Handy for debugging, bug reports, and ensuring your environment matches the docs.

