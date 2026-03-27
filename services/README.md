# Services

## What this module does

The **`services`** package holds **application and domain logic**: use cases, orchestration, validation that spans multiple steps, and coordination between **repositories**, caches, and external APIs. A service’s public API is typically a **`run(request_dto)`** (or similar) method that returns a **`dict`** or structured result consumed by the controller.

This layer sits between **controllers** (HTTP) and **repositories** (persistence). It is where you enforce rules like “email must be unique”, “order cannot ship if unpaid”, or “aggregate multiple reads/writes in one transaction” when your framework supports it.

## Responsibilities

| Concern | Handled here |
|--------|----------------|
| Business rules | Validation, workflows, cross-entity invariants |
| Orchestration | Multiple repositories, external calls, compensating actions |
| Logging / metrics | Operation-level context (`urn`, `api_name`, `user_id` via `IService`) |
| DTO mapping | Transform request DTOs into domain operations and results back to dicts |

## Layout (conceptual)

```
services/
├── abstraction.py          # App-level service base (extends IService)
├── example/                # Example use case (abstraction.py, example_service.py)
└── user/                   # Feature-specific services (e.g. user/fetch)
```

## How it fits in the stack

```
Controller → Service → Repository → Database
```

Services receive **dependencies** injected via **`dependencies/services/`** (factories) and use **DTOs** from **`dtos`** as inputs.

## Related documentation

- `abstractions/README.md` — `IService` and `run()`  
- `repositories/README.md` — data access  
- `dependencies/README.md` — service factories  

## Practices

1. **Idempotent** behavior where possible for the same logical operation.  
2. **Raise** domain-appropriate errors (mapped to HTTP by controllers or platform).  
3. **Avoid** importing FastAPI `Request` inside services; pass context via kwargs or DTOs.  
4. **Unit test** services with mocked repositories.
