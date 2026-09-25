"""Tests for the health-check endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_returns_200():
    """GET /api/v1/health should return 200 with status ok."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_response_body():
    """Health response must include status, service name, and version."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "onion-quality-backend"
    assert "version" in data
