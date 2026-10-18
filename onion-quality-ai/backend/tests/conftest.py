"""Pytest test fixtures and configuration."""

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.core.database import Base, get_db
from app.main import app as fastapi_app
import app.models
from app.services import image_service


@pytest.fixture(autouse=True)
def isolate_test_image_storage(tmp_path, monkeypatch):
    """Isolate image upload storage to pytest's tmp_path to prevent git pollution."""
    test_image_dir = tmp_path / "data" / "raw"
    test_image_dir.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    monkeypatch.setattr(settings, "image_directory", str(test_image_dir))
    monkeypatch.setattr(image_service, "settings", settings)
    yield test_image_dir


# In-memory SQLite async engine for lightning fast and isolated testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_db_session():
    """Create a fresh in-memory database schema for each test."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def async_client(test_db_session):
    """Provide an HTTPX AsyncClient with get_db overridden to use test_db_session."""
    async def override_get_db():
        yield test_db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    fastapi_app.dependency_overrides.clear()
