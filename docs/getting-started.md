## Getting Started with FastMVC

This guide walks you from installation to a running FastMVC-powered API.

### 1. Install FastMVC

You need Python 3.10+.

**Using `uv` (recommended):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install pyfastmvc
```

**Using `pip`:**

```bash
pip install pyfastmvc
```

Verify the CLI:

```bash
fastmvc --version
```

### 2. Generate a New Project

Use the non-interactive `generate` command:

```bash
fastmvc generate my_api
```

This creates a full FastAPI project with:

- MVC structure (`controllers/`, `services/`, `repositories/`, `models/`, `dtos/`)
- Middleware stack (security headers, logging, rate limiting, etc.)
- Configurations and `.env.example`
- Testing and migrations wiring

You can also provide options:

```bash
fastmvc generate my_api \
  --output-dir ./projects \
  --git \
  --venv \
  --install
```

See the **CLI reference** in [`cli.md`](cli.md) for all flags.

### 3. Set Up Dependencies

Change into the generated project:

```bash
cd my_api
```

**With `uv`:**

```bash
uv sync
uv run fastmvc migrate upgrade
```

**With `pip`:**

```bash
pip install -r requirements.txt
cp .env.example .env
```

Customize `.env` with your database, Redis, and security settings as needed (see [`configuration.md`](configuration.md)).

### 4. Start Infrastructure (Optional)

If you use Postgres and Redis, you can bring them up via Docker:

```bash
docker-compose up -d
```

### 5. Run the API

```bash
python -m uvicorn app:app --reload
```

Default endpoints:

- API root: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Dashboards (if enabled in your template):  
  - Health: `http://localhost:8000/dashboard/health`  
  - API activity: `http://localhost:8000/dashboard/api`

### 6. Next Steps

- **Generate entities**: use `fastmvc add entity <Name>` to scaffold full CRUD – see [`cli.md`](cli.md).
- **Explore architecture**: see how controllers, services, and repositories fit together in [`architecture.md`](architecture.md).
- **Configure datastores and integrations**: see [`configuration.md`](configuration.md) and the landing overview in `LANDING.md`.

