"""
Configuration DTOs for file/object storage providers.

Supports AWS S3, Google Cloud Storage, Azure Blob Storage, and a
generic local/minio-style backend for development.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class S3ConfigDTO(BaseModel):
    enabled: bool = False
    bucket: str = ""
    region: str = "us-east-1"
    endpoint_url: Optional[str] = None  # for minio/compat endpoints
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    base_path: str = ""  # prefix within bucket


class GCSConfigDTO(BaseModel):
    enabled: bool = False
    bucket: str = ""
    credentials_json_path: Optional[str] = None
    base_path: str = ""


class AzureBlobConfigDTO(BaseModel):
    enabled: bool = False
    container: str = ""
    connection_string: Optional[str] = None
    account_url: Optional[str] = None
    base_path: str = ""


class LocalStorageConfigDTO(BaseModel):
    """
    Simple filesystem or minio-like dev storage.
    """

    enabled: bool = False
    base_dir: str = "storage"
    base_url: Optional[str] = None  # for serving via CDN / static


class StorageConfigurationDTO(BaseModel):
    """
    Aggregated configuration for all storage providers.
    """

    s3: S3ConfigDTO = S3ConfigDTO()
    gcs: GCSConfigDTO = GCSConfigDTO()
    azure_blob: AzureBlobConfigDTO = AzureBlobConfigDTO()
    local: LocalStorageConfigDTO = LocalStorageConfigDTO()


__all__ = [
    "S3ConfigDTO",
    "GCSConfigDTO",
    "AzureBlobConfigDTO",
    "LocalStorageConfigDTO",
    "StorageConfigurationDTO",
]

