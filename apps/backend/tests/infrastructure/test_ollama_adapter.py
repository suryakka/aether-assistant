import json

import httpx
import pytest
import respx

from aether.config.settings import Settings
from aether.infrastructure.llm.ollama_adapter import OllamaLLMAdapter


@pytest.fixture
def settings() -> Settings:
    return Settings(
        llm_base_url="http://127.0.0.1:11434",
        llm_model="qwen3:8b",
        llm_timeout_seconds=30,
    )


@pytest.mark.asyncio
@respx.mock
async def test_ollama_stream_chat(settings: Settings):
    lines = [
        json.dumps({"message": {"content": "Hello"}, "done": False}),
        json.dumps({"message": {"content": " world"}, "done": True}),
    ]
    stream_content = "\n".join(lines)

    respx.post("http://127.0.0.1:11434/api/chat").mock(
        return_value=httpx.Response(200, text=stream_content)
    )

    adapter = OllamaLLMAdapter(settings=settings)
    chunks = [c async for c in adapter.stream_chat([])]

    assert len(chunks) == 2
    assert chunks[0].content == "Hello"
    assert chunks[1].content == " world"
    await adapter.close()


@pytest.mark.asyncio
@respx.mock
async def test_ollama_health_check_ok(settings: Settings):
    respx.get("http://127.0.0.1:11434/api/tags").mock(
        return_value=httpx.Response(200, json={"models": []})
    )

    adapter = OllamaLLMAdapter(settings=settings)
    assert await adapter.health_check() is True
    await adapter.close()


@pytest.mark.asyncio
@respx.mock
async def test_ollama_health_check_fail(settings: Settings):
    respx.get("http://127.0.0.1:11434/api/tags").mock(
        return_value=httpx.Response(503)
    )

    adapter = OllamaLLMAdapter(settings=settings)
    assert await adapter.health_check() is False
    await adapter.close()


@pytest.mark.asyncio
@respx.mock
async def test_ollama_health_check_connection_error(settings: Settings):
    respx.get("http://127.0.0.1:11434/api/tags").mock(
        side_effect=httpx.ConnectError("Connection refused")
    )

    adapter = OllamaLLMAdapter(settings=settings)
    assert await adapter.health_check() is False
    await adapter.close()


def test_build_user_message():
    from aether.domain.entities.message import MessageRole

    msg = OllamaLLMAdapter.build_user_message("Hello")
    assert msg.role == MessageRole.USER
    assert msg.content == "Hello"
