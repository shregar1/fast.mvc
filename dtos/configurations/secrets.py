"""
Configuration DTOs for secrets backends.

Includes AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager,
and Azure Key Vault, aggregated into a single configuration object.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class AwsSecretsManagerConfigDTO(BaseModel):
    enabled: bool = False
    region: str = "us-east-1"
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    prefix: str = ""  # optional key prefix


class VaultConfigDTO(BaseModel):
    enabled: bool = False
    url: str = "http://localhost:8200"
    token: Optional[str] = None
    mount_point: str = "secret"


class GcpSecretsManagerConfigDTO(BaseModel):
    enabled: bool = False
    project_id: Optional[str] = None
    credentials_json_path: Optional[str] = None


class AzureKeyVaultConfigDTO(BaseModel):
    enabled: bool = False
    vault_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None


class SecretsConfigurationDTO(BaseModel):
    """
    Aggregated configuration for all secrets backends.
    """

    aws: AwsSecretsManagerConfigDTO = AwsSecretsManagerConfigDTO()
    vault: VaultConfigDTO = VaultConfigDTO()
    gcp: GcpSecretsManagerConfigDTO = GcpSecretsManagerConfigDTO()
    azure: AzureKeyVaultConfigDTO = AzureKeyVaultConfigDTO()


__all__ = [
    "AwsSecretsManagerConfigDTO",
    "VaultConfigDTO",
    "GcpSecretsManagerConfigDTO",
    "AzureKeyVaultConfigDTO",
    "SecretsConfigurationDTO",
]

