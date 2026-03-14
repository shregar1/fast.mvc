"""
Database table name constants.

Re-exports Table from fastmvc_db for backward compatibility.

Usage:
    >>> from constants.db.table import Table
    >>> class User(Base):
    ...     __tablename__ = Table.USER
"""

from fastmvc_db import Table

__all__ = ["Table"]
