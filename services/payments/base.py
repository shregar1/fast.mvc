"""
Base abstractions for payment gateways. Re-exports from fastmvc_payments.
"""

from fastmvc_payments import CheckoutSession, IPaymentGateway

__all__ = ["CheckoutSession", "IPaymentGateway"]
