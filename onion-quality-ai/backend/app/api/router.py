"""
Central API router.

Aggregates all route modules under the /api/v1 prefix.
"""

from fastapi import APIRouter

from app.api.routes import health, inspections, images, grading, reports

api_router = APIRouter(prefix="/api/v1")

# Health check has no additional prefix
api_router.include_router(health.router)

# Domain routes (currently stubs)
api_router.include_router(inspections.router)
api_router.include_router(images.router)
api_router.include_router(grading.router)
api_router.include_router(reports.router)
