import pytest
from httpx import ASGITransport, AsyncClient

from aether.container import create_container
from aether.main import create_app


@pytest.fixture
def app():
    container = create_container()
    return create_app(container=container)


@pytest.mark.asyncio
async def test_health_endpoint(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "aether-backend"


@pytest.mark.asyncio
async def test_config_endpoint(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/config")

    assert response.status_code == 200
    data = response.json()
    assert "llm" in data
    assert data["llm"]["provider"] == "ollama"
