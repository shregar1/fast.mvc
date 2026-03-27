# The `_maint` folder (critical — do not change casually)

!!! danger "Do not modify without platform / infra review"
    The **`_maint`** directory is **not** application feature code. It holds **infrastructure and tooling** that the runtime, Docker, database bootstrap, reverse proxy, and automation depend on.

    **Do not rename, relocate, or delete** this folder or its contents unless you fully understand every reference (see below). Treat changes here like changes to production deployment config.

## What lives here

| Path | Role |
|------|------|
| `_maint/nginx/` | Nginx config and TLS material expected by `docker-compose` (reverse proxy profile). |
| `_maint/init-scripts/` | SQL executed on PostgreSQL first init (mounted into `docker-entrypoint-initdb.d`). |
| `_maint/scripts/` | Operational scripts (e.g. DB seed, git metadata hooks). Paths are wired in Docker entrypoints and **pre-commit**. |

Breaking paths here breaks **local Docker**, **CI hooks**, and **documented commands** without touching your Python app code.

## Who should change it

- **Platform / DevOps** or maintainers who own deployment and Docker.
- **Never** as part of a normal feature PR unless the task explicitly updates infra (and reviewers know to check `docker-compose.yml`, `docker-entrypoint.sh`, `.pre-commit-config.yaml`, and this doc).

## If you must change something

1. Search the repo for `_maint`, `init-scripts`, `nginx`, and the script filenames you move.
2. Update **all** references (compose volumes, entrypoints, docs, pre-commit).
3. Run Docker and pre-commit locally to verify.

## Related documentation

- [Project structure](project-structure.md) — where `_maint` appears in the tree.
- [Docker](docker.md) — nginx volumes and seed commands use paths under `_maint`.
