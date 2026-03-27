# 🚀 Core Features

FastMVC is a high-performance, developer-centric framework built on top of FastAPI. It enforces clean, vertical architecture while automating the most repetitive parts of API development through a powerful CLI.

---

## 🏗️ Architectural Excellence

FastMVC projects follow a "Vertical Slice" architecture by default. Instead of grouping all logic by technical layer (e.g., all controllers in one folder), it groups by **business context and operation**.

- **Endpoints:** Completely isolated in `apis/{version}/{folder}/{operation}.py`.
- **Services:** Operation-specific business logic in `services/{folder}/{operation}.py`.
- **Repositories:** Decoupled data access in `repositories/{folder}/{operation}.py`.
- **Contracts:** Strictly-typed Request/Response DTOs isolated by version.

### Benefits
1. **Developer Velocity:** Modify an operation without touching unrelated files.
2. **Reduced Conflicts:** Parallel development on the same resource (e.g., `create` and `fetch`) is seamless.
3. **Implicit Versioning:** Clear isolation between API versions (`v1`, `v2`, etc.).

---

## 🔐 Zero-to-Hero Authentication

Scaffold a complete, production-ready authentication layer with a single command: `fastmvc add auth`.

- **JWT Integration:** Includes secure token generation and validation.
- **Hashing:** Industry-standard Bcrypt hashing for password storage.
- **Auto-Injection:** Middleware extracts tokens and injects `user_id` into the request session.
- **Protection:** Includes a `get_current_user_id` dependency for easy route guarding.

---

## 🛡️ Secure Configurations (`.env`)

FastMVC automates the setup of local environment variables:
- **Automatic Secret Generation:** Secure 64-character hex keys for `SECRET_KEY` and `JWT_SECRET_KEY`.
- **Templating:** Projects generate a functional `.env` from an `.env.example` boilerplate during creation.
- **Environment Management:** Use `fastmvc add env` at any time to refresh or generate local configurations.

---

## 🛰️ API Documentation

Documentation is a first-class citizen in FastMVC.
- **OpenAPI:** Native FastAPI interactive Swagger and ReDoc.
- **Auto-Discovery Reference:** Run `fastmvc docs generate` to crawl your code and build a dedicated MkDocs API Reference using `mkdocstrings`.
- **Dto Descriptions:** Descriptions from your Pydantic DTOs are automatically pulled into the generated documentation.

---

## ⏳ Background Tasks

FastMVC handles background processing with a clear, decoupled pattern:
- **Task Definitions:** Isolated in the `tasks/` directory.
- **FastAPI Integration:** Wired for `BackgroundTasks` out of the box.
- **Celery Ready:** Scaffolds are easy to decorate with `@celery.task` for distributed worker setups.

---

## 🧪 Built-in Testing

FastMVC makes testing a habit, not a chore.
- **Async Pytest:** Pre-configured for asynchronous operations and `httpx`.
- **Mocking Support:** Scaffolds include examples for mocking complex service and repository dependencies.
- **Versioned Tests:** Test suites mirror the API architecture for easy navigation.
