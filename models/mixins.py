"""
Reusable SQLAlchemy 2.0 mixins for composed models.

Compose mixins **before** :class:`~models.Base` so columns merge correctly::

    class Order(SoftDeleteMixin, AuditActorMixin, TimestampMixin, Base):
        __tablename__ = "orders"
        id: Mapped[int] = mapped_column(primary_key=True, ...)
        # entity-specific columns only

Add project-specific mixins here (e.g. ``TenantMixin``) and inherit them alongside these.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

__all__ = [
    "AuditActorMixin",
    "SoftDeleteMixin",
    "TimestampMixin",
]


class SoftDeleteMixin:
    """``is_active`` / ``is_deleted`` flags for soft delete and listing."""

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class AuditActorMixin:
    """Who created / last updated the row."""

    created_by: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class TimestampMixin:
    """Creation and last-mutation timestamps."""

    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_on: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.now
    )
