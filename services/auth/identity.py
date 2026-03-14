"""
Identity provider abstractions and builders. Re-exports from fastmvc_identity.
"""

from fastmvc_identity import (
    IdentityUserProfile,
    IIdentityProvider,
    build_identity_providers,
)

__all__ = [
    "IdentityUserProfile",
    "IIdentityProvider",
    "build_identity_providers",
]
