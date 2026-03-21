"""
Payment provider DTOs. Re-exports from fast_payments for backward compatibility.
"""

from fast_payments import (
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
