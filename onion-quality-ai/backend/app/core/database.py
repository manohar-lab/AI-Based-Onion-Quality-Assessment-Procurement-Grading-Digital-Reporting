"""
SQLAlchemy async engine and session factory.

The health endpoint must remain available even when the database is
temporarily unreachable, so we do NOT fail at import time if the
connection string is invalid.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


def _resolve_db_url(url: str) -> str:
    """Normalize async database URL to available driver (asyncpg or psycopg)."""
    if "postgresql+asyncpg://" in url:
        try:
            import asyncpg  # noqa: F401
        except ImportError:
            try:
                import psycopg  # noqa: F401
                return url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
            except ImportError:
                pass
    return url


def get_engine():
    """Create or return existing async engine."""
    global engine
    if engine is None:
        url = _resolve_db_url(settings.database_url)
        engine = create_async_engine(
            url,
            echo=settings.debug,
            pool_pre_ping=True,
        )
    return engine


def get_session_factory():
    """Create or return async sessionmaker."""
    global async_session_factory
    if async_session_factory is None:
        async_session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return async_session_factory


engine = None
async_session_factory = None


async def get_db() -> AsyncSession:
    """FastAPI dependency that yields an async session and closes it after use."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
