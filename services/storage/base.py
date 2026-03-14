"""
File/object storage abstraction layer.

Provides a minimal interface ``IFileStorage`` and concrete backends
for AWS S3, Google Cloud Storage, Azure Blob Storage, and local
filesystem-based storage suitable for development/minio.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Optional

from loguru import logger

from fastmvc_core import StorageConfiguration

try:  # Optional providers
    import boto3
except Exception:  # pragma: no cover - optional
    boto3 = None  # type: ignore

try:
    from google.cloud import storage as gcs_storage
except Exception:  # pragma: no cover - optional
    gcs_storage = None  # type: ignore

try:
    from azure.storage.blob import BlobServiceClient
except Exception:  # pragma: no cover - optional
    BlobServiceClient = None  # type: ignore


@dataclass
class StoredFile:
    """
    Metadata about a stored file.
    """

    url: str
    path: str


class IFileStorage(ABC):
    """
    Minimal file storage interface.
    """

    name: str

    @abstractmethod
    async def upload(self, path: str, data: bytes) -> StoredFile:  # pragma: no cover - interface
        raise NotImplementedError

    @abstractmethod
    async def delete(self, path: str) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class LocalFileStorage(IFileStorage):
    def __init__(self, base_dir: str, base_url: Optional[str]) -> None:
        self.name = "local"
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(parents=True, exist_ok=True)
        self._base_url = base_url.rstrip("/") if base_url else None

    async def upload(self, path: str, data: bytes) -> StoredFile:
        full_path = self._base_dir / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(data)
        if self._base_url:
            url = f"{self._base_url}/{path}"
        else:
            url = str(full_path.resolve())
        return StoredFile(url=url, path=path)

    async def delete(self, path: str) -> None:
        full_path = self._base_dir / path
        try:
            full_path.unlink()
        except FileNotFoundError:
            return


class S3FileStorage(IFileStorage):
    def __init__(
        self,
        bucket: str,
        region: str,
        endpoint_url: Optional[str],
        access_key_id: Optional[str],
        secret_access_key: Optional[str],
        base_path: str,
    ) -> None:
        self.name = "s3"
        self._bucket = bucket
        self._base_path = base_path.strip("/")
        if boto3 is None:  # pragma: no cover - optional
            self._client = None
            logger.warning("boto3 not installed; S3 storage is disabled.")
        else:
            session_kwargs = {}
            if access_key_id and secret_access_key:
                session_kwargs.update(
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                )
            self._client = boto3.client(
                "s3",
                region_name=region,
                endpoint_url=endpoint_url or None,
                **session_kwargs,
            )

    async def upload(self, path: str, data: bytes) -> StoredFile:
        if not self._client:
            raise RuntimeError("S3 client is not configured")

        key = f"{self._base_path}/{path}" if self._base_path else path
        self._client.put_object(Bucket=self._bucket, Key=key, Body=data)
        url = f"s3://{self._bucket}/{key}"
        return StoredFile(url=url, path=key)

    async def delete(self, path: str) -> None:
        if not self._client:
            return
        key = f"{self._base_path}/{path}" if self._base_path else path
        self._client.delete_object(Bucket=self._bucket, Key=key)


class GCSFileStorage(IFileStorage):
    def __init__(
        self,
        bucket: str,
        credentials_json_path: Optional[str],
        base_path: str,
    ) -> None:
        self.name = "gcs"
        self._bucket_name = bucket
        self._base_path = base_path.strip("/")
        if gcs_storage is None:  # pragma: no cover - optional
            self._client = None
            self._bucket = None
            logger.warning("google-cloud-storage not installed; GCS storage is disabled.")
        else:
            if credentials_json_path:
                self._client = gcs_storage.Client.from_service_account_json(credentials_json_path)
            else:
                self._client = gcs_storage.Client()
            self._bucket = self._client.bucket(self._bucket_name)

    async def upload(self, path: str, data: bytes) -> StoredFile:
        if not self._bucket:
            raise RuntimeError("GCS client is not configured")
        key = f"{self._base_path}/{path}" if self._base_path else path
        blob = self._bucket.blob(key)
        blob.upload_from_string(data)
        url = blob.public_url
        return StoredFile(url=url, path=key)

    async def delete(self, path: str) -> None:
        if not self._bucket:
            return
        key = f"{self._base_path}/{path}" if self._base_path else path
        blob = self._bucket.blob(key)
        try:
            blob.delete()
        except Exception:
            return


class AzureBlobFileStorage(IFileStorage):
    def __init__(
        self,
        container: str,
        connection_string: Optional[str],
        account_url: Optional[str],
        base_path: str,
    ) -> None:
        self.name = "azure_blob"
        self._container_name = container
        self._base_path = base_path.strip("/")
        if BlobServiceClient is None:  # pragma: no cover - optional
            self._container_client = None
            logger.warning("azure-storage-blob not installed; Azure Blob storage is disabled.")
        else:
            if connection_string:
                service_client = BlobServiceClient.from_connection_string(connection_string)
            elif account_url:
                service_client = BlobServiceClient(account_url=account_url)
            else:
                self._container_client = None
                logger.warning(
                    "Azure Blob storage enabled but neither connection_string nor "
                    "account_url is configured.",
                )
                return
            self._container_client = service_client.get_container_client(container)

    async def upload(self, path: str, data: bytes) -> StoredFile:
        if not self._container_client:
            raise RuntimeError("Azure Blob client is not configured")
        key = f"{self._base_path}/{path}" if self._base_path else path
        blob_client = self._container_client.get_blob_client(key)
        blob_client.upload_blob(data, overwrite=True)
        url = blob_client.url
        return StoredFile(url=url, path=key)

    async def delete(self, path: str) -> None:
        if not self._container_client:
            return
        key = f"{self._base_path}/{path}" if self._base_path else path
        blob_client = self._container_client.get_blob_client(key)
        try:
            blob_client.delete_blob()
        except Exception:
            return


def build_storage_backend() -> IFileStorage:
    """
    Build an appropriate storage backend from configuration.

    Priority:
      - S3 if enabled
      - GCS if enabled
      - Azure Blob if enabled
      - Local as a safe default (enabled by default in JSON)
    """

    cfg = StorageConfiguration.instance().get_config()

    if cfg.s3.enabled and cfg.s3.bucket:
        return S3FileStorage(
            bucket=cfg.s3.bucket,
            region=cfg.s3.region,
            endpoint_url=cfg.s3.endpoint_url or None,
            access_key_id=cfg.s3.access_key_id,
            secret_access_key=cfg.s3.secret_access_key,
            base_path=cfg.s3.base_path,
        )

    if cfg.gcs.enabled and cfg.gcs.bucket:
        return GCSFileStorage(
            bucket=cfg.gcs.bucket,
            credentials_json_path=cfg.gcs.credentials_json_path,
            base_path=cfg.gcs.base_path,
        )

    if cfg.azure_blob.enabled and cfg.azure_blob.container:
        return AzureBlobFileStorage(
            container=cfg.azure_blob.container,
            connection_string=cfg.azure_blob.connection_string,
            account_url=cfg.azure_blob.account_url,
            base_path=cfg.azure_blob.base_path,
        )

    # Fallback: local storage
    if not cfg.local.enabled:
        logger.info("All cloud storage providers disabled; enabling local storage.")
    return LocalFileStorage(
        base_dir=cfg.local.base_dir,
        base_url=cfg.local.base_url,
    )


__all__ = [
    "StoredFile",
    "IFileStorage",
    "LocalFileStorage",
    "S3FileStorage",
    "GCSFileStorage",
    "AzureBlobFileStorage",
    "build_storage_backend",
]

