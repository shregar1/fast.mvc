"""
Outbound webhook signing & delivery — re-exported from ``fast_webhooks``.

For **inbound** HTTP signature verification on your own routes, see ``core.security.webhooks``.
Prefer ``from fast_webhooks import …`` in new code.
"""

from fast_webhooks import (
    RetryPolicy,
    compute_signature,
    deliver_webhook,
    deliver_webhook_sync,
    require_webhook_signature,
    signature_header_value,
    verify_signature,
    __version__,
)

__all__ = [
    "RetryPolicy",
    "__version__",
    "compute_signature",
    "deliver_webhook",
    "deliver_webhook_sync",
    "require_webhook_signature",
    "signature_header_value",
    "verify_signature",
]
