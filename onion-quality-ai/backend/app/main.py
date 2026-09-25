"""
FastAPI application entry point.

Usage:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    """Application factory — builds and configures the FastAPI instance."""
    settings = get_settings()
    setup_logging()

    application = FastAPI(
        title="Onion Quality Assessment API",
        description=(
            "AI-based quality assessment, government-specification-aware grading, "
            "and digital reporting for Indian onion procurement."
        ),
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.include_router(api_router)

    return application


app = create_app()
