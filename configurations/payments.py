"""
Payments configuration. Re-exports from fastmvc_payments for backward compatibility.
"""

from fastmvc_payments import (
    PaymentsConfiguration,
    PaymentsConfigurationDTO,
)

__all__ = ["PaymentsConfiguration", "PaymentsConfigurationDTO"]
