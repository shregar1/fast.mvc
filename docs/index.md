## FastMVC Documentation

FastMVC is a **project generator and MVC framework for FastAPI** that lets you spin up a production-ready backend in minutes.

- **What this docs set is for**
  - Understand what FastMVC gives you out of the box.
  - Learn how to generate and run a new project.
  - Explore the CLI, architecture, configuration system, and core modules.
  - Reuse these pages as the content source for a docs website (MkDocs, Docusaurus, etc.).

### Key Sections

- **Getting started**: Installation, `fastmvc generate`, running your first service – see [`getting-started.md`](getting-started.md).
- **CLI reference**: All `fastmvc` commands (`generate`, `init`, `add`, `migrate`, `info`, `version`) – see [`cli.md`](cli.md).
- **Architecture**: MVC layering, middleware pipeline, request lifecycle – see [`architecture.md`](architecture.md).
- **Configuration**: `.env`, JSON configs under `config/**/config.json`, configuration DTOs – see [`configuration.md`](configuration.md).
- **Modules overview**: High-level docs per package (controllers, services, repositories, etc.) – see [`modules.md`](modules.md).

For deeper, code-level documentation, each package also has its own `README.md` in the repo (for example `services/README.md`, `configurations/README.md`, `core/README.md`).

