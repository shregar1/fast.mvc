"""
Repository Abstraction Module.

.. deprecated::
    This module is deprecated. Import from ``fast_database`` instead:
    
    >>> from fast_database.persistence.repositories.abstraction import IRepository
    >>> from fast_database.persistence.repositories.lookup_base import LookupRepositoryBase

This module now provides re-exports for backward compatibility.
All functionality has been consolidated into ``fast_database`` to
eliminate code duplication (DRY principle).

The IRepository class now extends ContextMixin from fast_platform
to eliminate duplication of context fields across the framework.
"""

from __future__ import annotations

# Re-export from fast_database to eliminate duplication
# This maintains backward compatibility while ensuring both
# modules use the same implementation
from fast_database.persistence.repositories.abstraction import IRepository

# Also re-export FilterOperator for convenience
from constants.filter_operator import FilterOperator

__all__ = ["IRepository", "FilterOperator"]
