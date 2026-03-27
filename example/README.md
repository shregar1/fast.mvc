# Example

## What this module does

The **`example`** package is a **reference implementation** of the FastMVC stack: a small but complete vertical slice (entities, repositories, services, controllers, DTOs, tests) that shows how to wire a feature end-to-end. It is **not** required for production deployments—you can delete or replace it as your project grows.

Use it as a **template** when adding new resources: copy structure, naming, and patterns rather than inventing layout from scratch.

## What it typically contains

| Area | Role |
|------|------|
| `entities/` | Domain models (e.g. `Item`) |
| `repositories/` | Persistence for those entities |
| `services/` | Business operations |
| `controllers/` | HTTP handlers for the example API |
| `dtos/` | Request/response shapes for the example |
| `testing/` | Factories and fixtures used by tests |

## How it fits in the stack

The example module follows the same rules as the rest of the app:

```
example/controllers → example/services → example/repositories → DB
```

The main `app.py` may **include** example routers or feature flags; see project docs for how the example is mounted.

## Related documentation

- `docs/guide/project-structure.md` — overall layout  
- `docs/guide/quickstart.md` — running and exploring the app  

## Practices

1. Treat **example** as **documentation-by-code**; keep it readable.  
2. When you **copy** patterns into production code, move them into **non-example** packages (`services/`, `controllers/`, …).  
3. Keep **tests** in `tests/` aligned with example changes so CI stays green.
