"""
Payment provider DTOs. Re-exports from fastmvc_payments for backward compatibility.
"""

from fastmvc_payments import (
    LinkConfigDTO,
    PayUConfigDTO,
    PaypalConfigDTO,
    PaymentsConfigurationDTO,
    RazorpayConfigDTO,
    StripeConfigDTO,
)

__all__ = [
    "StripeConfigDTO",
    "RazorpayConfigDTO",
    "PaypalConfigDTO",
    "PayUConfigDTO",
    "LinkConfigDTO",
    "PaymentsConfigurationDTO",
]
