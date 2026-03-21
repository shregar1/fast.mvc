## Architecture Overview

FastMVC wraps FastAPI in a structured **MVC architecture** with a rich middleware pipeline and opinionated response format. This page summarizes the architecture diagrams and explanations from the main `README.md` in a form that can be embedded into a docs site.

### High-Level Layers

From top to bottom:

- **Client**: Browsers, mobile apps, and other API consumers.
- **FastAPI application**: `app.py` entrypoint, routers, and middleware stack.
- **Controller layer** (`controllers/`):
  - HTTP routing and DTO binding.
  - Translates HTTP requests into service calls.
- **Service layer** (`services/`):
  - Business logic, workflows, orchestration of repositories and external APIs.
- **Repository layer** (`repositories/`):
  - Data access abstractions over SQLAlchemy (and optionally other datastores).
- **Data layer**:
  - PostgreSQL/MySQL/SQLite via SQLAlchemy and Alembic.
  - Optional Redis, MongoDB, Cassandra, Scylla, DynamoDB, Cosmos DB, Elasticsearch.

See `README.md` for detailed ASCII diagrams of the full stack and MVC interactions.

### Middleware Pipeline

FastMVC uses the `fast-middleware` collection (90+ middlewares) to wrap every request with:

- **Request context** – per-request URN for traceability.
- **Timing** – adds processing time headers.
- **Rate limiting** – sliding window (per-minute and per-hour).
- **Authentication** – JWT-based protection for secured routes.
- **Logging** – structured JSON logging with correlation data.
- **Security headers** – CSP, HSTS, X-Frame-Options, X-Content-Type-Options.
- **CORS** – cross-origin request handling.

These middlewares run before your controllers, so your business code sees a consistent, secure, observable environment.

### DTOs and Response Shape

FastMVC standardizes request and response structures with DTOs:

- **Request DTOs** (under `dtos/requests/`) validate incoming data via Pydantic v2.
- **Response DTOs** (under `dtos/responses/`) wrap responses in a common envelope:

```json
{
  "transactionUrn": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
  "status": "SUCCESS",
  "responseMessage": "User logged in successfully",
  "responseKey": "success_user_login",
  "data": {
    "user": { "id": 1, "email": "user@example.com" },
    "token": "..."
  }
}
```

This makes frontends and other consumers easier to build and reason about.

### Project Structure (Generated App)

A typical generated project looks like:

```text
my_api/
├── app.py              # FastAPI entry point
├── start_utils.py      # Startup configuration
├── abstractions/       # Base interfaces (IController, IService, IRepository)
├── controllers/        # HTTP route handlers
├── services/           # Business logic
├── repositories/       # Data access layer
├── models/             # SQLAlchemy models
├── dtos/               # Request/response DTOs
├── middlewares/        # Custom middlewares
├── migrations/         # Alembic migrations
├── tests/              # Test suite
└── docker-compose.yml  # Optional infrastructure
```

See [`modules.md`](modules.md) and each package `README.md` (for example `services/README.md`, `core/README.md`) for deeper details.

### Core Module Capabilities

The `core/` package extends the base MVC architecture with enterprise features (see `core/README.md`):

- Health checks (Kubernetes-ready).
- Observability: structured logging, metrics, tracing.
- Resilience: circuit breakers, retry with backoff.
- Background tasks with queues.
- API keys and webhook verification.
- Feature flags and A/B rollouts.
- Multi-tenancy support.
- API versioning.
- Testing utilities (factories, mocks, fixtures).

You can import these into generated apps as needed, or wire them into your custom templates.

