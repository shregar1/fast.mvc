# Static

## What this module does

The **`static`** directory holds **static assets** served by the application (or by a reverse proxy in production): HTML fragments, custom Swagger UI, logos, or other files that are not Python modules and **not** generated at runtime.

Typical uses include:

- **Custom Swagger UI** (`swagger.html`) when you override the default OpenAPI UI  
- **Branding** assets referenced from templates or docs  
- **Small client bundles** that you choose to serve from FastAPI’s `StaticFiles` mount  

## What does *not* belong here

- **Large** front-end builds (prefer a separate CDN or SPA host)  
- **Secrets** or environment-specific config (use `.env` and `config/`)  
- **User uploads** (use object storage or a dedicated upload volume)  

## How it fits in the stack

`app.py` (or `start_utils`) may mount:

```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

Exact path and mount name depend on your template.

## Practices

1. **Version** assets when caching aggressively (cache-busting query strings or filenames).  
2. **Minify** CSS/JS in production pipelines if you add many assets.  
3. **Document** any new mount in `docs/guide/` or `README.md` at repo root.
