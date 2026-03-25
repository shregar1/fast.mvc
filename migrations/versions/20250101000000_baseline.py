"""Baseline (empty schema).

Revision ID: 20250101000000
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""

from typing import Sequence, Union

revision: str = "20250101000000"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No tables in metadata at baseline; add models then autogenerate."""
    pass


def downgrade() -> None:
    pass
