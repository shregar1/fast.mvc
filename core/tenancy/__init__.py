"""
Multi-tenancy — re-exported from ``fast_tenancy``.

Prefer importing from the library directly in new code::

    from fast_tenancy import TenantContext, TenantMiddleware, HeaderTenantResolver
"""

from fast_tenancy import (
    ChainedTenantResolver,
    HeaderTenantResolver,
    InMemoryTenantStore,
    JWTTenantResolver,
    PathTenantResolver,
    ResolutionStrategy,
    ResolverSpec,
    SubdomainTenantResolver,
    Tenant,
    TenantConfig,
    TenantContext,
    TenantMiddleware,
    TenantResolver,
    TenantResolverRegistry,
    TenantStore,
    clear_current_tenant,
    default_registry,
    get_current_tenant,
    get_current_tenant_id,
    set_current_tenant,
    subdomain_then_header,
)

__all__ = [
    "ChainedTenantResolver",
    "HeaderTenantResolver",
    "InMemoryTenantStore",
    "JWTTenantResolver",
    "PathTenantResolver",
    "ResolutionStrategy",
    "ResolverSpec",
    "SubdomainTenantResolver",
    "Tenant",
    "TenantConfig",
    "TenantContext",
    "TenantMiddleware",
    "TenantResolver",
    "TenantResolverRegistry",
    "TenantStore",
    "clear_current_tenant",
    "default_registry",
    "get_current_tenant",
    "get_current_tenant_id",
    "set_current_tenant",
    "subdomain_then_header",
]
