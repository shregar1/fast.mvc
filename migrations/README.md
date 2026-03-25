# Alembic migrations

- **URL**: Set `DATABASE_URL` in `.env` (see `.env.example`). `migrations/env.py` loads `.env` then `.env.example`.
- **Metadata**: Import ORM modules in `models/__init__.py` so autogenerate sees every table.
- **New revision (autogenerate)** after model changes:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

- **Apply**: `alembic upgrade head`
- **Triggers / raw DDL**: The ORM does not create triggers. In a new revision, use `op.execute(sa.text("CREATE TRIGGER ..."))` and the matching `DROP` in `downgrade()`.
