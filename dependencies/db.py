"""
Database Dependency Module.

Re-exports DBDependency from fast_db for backward compatibility.

Usage:
    >>> from fastapi import Depends
    >>> from dependencies.db import DBDependency
    >>>
    >>> async def my_endpoint(session: Session = Depends(DBDependency.derive)):
    ...     users = session.query(User).all()
"""

from fast_db import DBDependency

__all__ = ["DBDependency"]
