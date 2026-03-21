"""
Application core integration layer (FastAPI wiring, observability, security, etc.).

Shared configuration DTOs, optional-import helpers, OTLP bridge utilities, cache/queue
streams, and other framework primitives live in the ``fast_core`` package — import
from ``fast_core`` (or ``fast_core.services.*``) for those instead of duplicating them
here.

Multi-tenancy is delegated to ``fast_tenancy`` (re-exported under ``core.tenancy``).
Background jobs use ``fast_jobs`` (re-exported under ``core.tasks``).

Integration libraries are also re-exported under stable ``core.*`` paths for convenience:

- ``core.storage`` → ``fast_storage``
- ``core.secrets`` → ``fast_secrets``
- ``core.queues`` → ``fast_queues``
- ``core.search`` → ``fast_search``
- ``core.vectors`` → ``fast_vectors``
- ``core.webrtc`` → ``fast_webrtc``
- ``core.webhooks`` → ``fast_webhooks`` (outbound signing/delivery; inbound verification lives in ``core.security.webhooks``)

Relational DB access uses ``fast_db``. This ``core`` package holds app-specific glue:
``configure_otel`` / Datadog, local ``IDataStore`` adapters under ``core.datastores``,
security helpers, feature flags, and WebSocket/versioning routes tied to this repo.
"""

from core.observability import AuditLog, Metrics, StructuredLogger, Tracer
from core.resilience import CircuitBreaker, RetryPolicy, retry
from core.tasks import (
    JobsConfiguration,
    JobsConfigurationDTO,
    cancel_job,
    enqueue,
    get_job_status,
)
from core.security import APIKeyManager, FieldEncryption, WebhookVerifier
from core.features import FeatureFlags, feature_flag
from core.tenancy import Tenant, TenantContext, get_current_tenant
from core.versioning import APIVersion, versioned_router

__all__ = [
    # Observability
    "StructuredLogger",
    "Metrics",
    "Tracer",
    "AuditLog",
    # Resilience
    "CircuitBreaker",
    "RetryPolicy",
    "retry",
    # Jobs (fast_jobs)
    "enqueue",
    "cancel_job",
    "get_job_status",
    "JobsConfiguration",
    "JobsConfigurationDTO",
    # Security
    "APIKeyManager",
    "WebhookVerifier",
    "FieldEncryption",
    # Features
    "FeatureFlags",
    "feature_flag",
    # Tenancy (fast_tenancy)
    "Tenant",
    "TenantContext",
    "get_current_tenant",
    # Versioning
    "APIVersion",
    "versioned_router",
]
