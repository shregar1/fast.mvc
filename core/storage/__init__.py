"""Object storage — re-exported from ``fast_storage``. Prefer ``from fast_storage import …`` in new code."""

from fast_storage import (
    IStorageBackend,
    LocalStorageBackend,
    StorageObjectHead,
    StorageConfiguration,
    StorageConfigurationDTO,
    build_storage_backend,
    multipart_upload_large_file,
)

__all__ = [
    "IStorageBackend",
    "LocalStorageBackend",
    "StorageObjectHead",
    "StorageConfiguration",
    "StorageConfigurationDTO",
    "build_storage_backend",
    "multipart_upload_large_file",
]
