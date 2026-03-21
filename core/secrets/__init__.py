"""Secrets backends — re-exported from ``fast_secrets``. Prefer ``from fast_secrets import …`` in new code."""

from fast_secrets import (
    CachedSecretsBackend,
    ISecretsBackend,
    LeasedSecretsBackend,
    RotationCallback,
    SecretsConfiguration,
    SecretsConfigurationDTO,
    build_secrets_backend,
    redact_json_for_log,
    redact_mapping,
    redact_text,
)

__all__ = [
    "CachedSecretsBackend",
    "ISecretsBackend",
    "LeasedSecretsBackend",
    "RotationCallback",
    "SecretsConfiguration",
    "SecretsConfigurationDTO",
    "build_secrets_backend",
    "redact_json_for_log",
    "redact_mapping",
    "redact_text",
]
