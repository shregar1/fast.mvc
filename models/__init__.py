"""
SQLAlchemy models package.

Import concrete model modules here so Alembic autogenerate sees all tables::

    from models import Base
    from models.user import User  # noqa: F401

:class:`Base` is the declarative base for application ORM models.

Extending models
----------------
Compose :mod:`models.mixins` (soft delete, audit, timestamps) before ``Base``, add
entity-specific :class:`~sqlalchemy.orm.Mapped` columns and ``__table_args__``, then
``alembic revision --autogenerate``. Triggers: ``op.execute(...)`` in migrations.
"""

from sqlalchemy.orm import DeclarativeBase

from models.mixins import AuditActorMixin, SoftDeleteMixin, TimestampMixin

__all__ = [
    "Base",
    "AuditActorMixin",
    "SoftDeleteMixin",
    "TimestampMixin",
]


class Base(DeclarativeBase):
    """Declarative base for FastMVC application models."""
