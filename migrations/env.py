"""
Alembic environment.

Loads ``DATABASE_URL`` from ``.env`` or ``.env.example`` (project root), then runs
migrations against :attr:`models.Base.metadata` for autogenerate support.
"""

from __future__ import annotations

import os
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import create_engine, pool

from alembic import context

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[misc, assignment]

_ROOT = Path(__file__).resolve().parent.parent

if load_dotenv is not None:
    load_dotenv(_ROOT / ".env")
    load_dotenv(_ROOT / ".env.example", override=False)

from models import Base  # noqa: E402

target_metadata = Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_url() -> str:
    url = os.environ.get("DATABASE_URL", "").strip()
    if url:
        return url
    return f"sqlite:///{_ROOT / 'app.db'}"


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = get_url()
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
