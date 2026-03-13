from __future__ import annotations

from fastapi import APIRouter

from core.health.dashboard import router as HealthDashboardRouter
from core.api_dashboard import ApiDashboardRouter
from core.queues_dashboard import QueuesDashboardRouter
from core.tenants_dashboard import TenantsDashboardRouter
from core.secrets_dashboard import SecretsDashboardRouter
from core.workflows_dashboard import WorkflowsDashboardRouter


router = APIRouter()

# Nest all dashboard-related routers under a single composite router.
# Each imported router already defines its own prefix (e.g. /dashboard/queues),
# so we simply include them without adding an extra prefix here.
router.include_router(HealthDashboardRouter)
router.include_router(ApiDashboardRouter)
router.include_router(QueuesDashboardRouter)
router.include_router(TenantsDashboardRouter)
router.include_router(SecretsDashboardRouter)
router.include_router(WorkflowsDashboardRouter)


__all__ = ["router"]

