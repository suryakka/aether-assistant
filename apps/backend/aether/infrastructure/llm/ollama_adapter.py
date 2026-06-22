import json
from collections.abc import AsyncIterator

import httpx

from aether.config.settings import Settings
from aether.domain.entities.chat import Message
from aether.domain.entities.message import MessageRole
from aether.domain.ports.llm import LLMChunk
from aether.infrastructure.logging.setup import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = (
    "You are Aether, a local-first AI desktop assistant. "
    "Be concise, helpful, and privacy-aware. "
    "Respond in the same language the user writes in."
)


class OllamaLLMAdapter:
    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self._settings = settings
        self._client = client or httpx.AsyncClient(
            base_url=settings.llm_base_url,
            timeout=settings.llm_timeout_seconds,
        )
        self._owns_client = client is None

    async def stream_chat(self, messages: list[Message]) -> AsyncIterator[LLMChunk]:
        ollama_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        ollama_messages.extend(msg.to_ollama() for msg in messages)

        payload = {
            "model": self._settings.llm_model,
            "messages": ollama_messages,
            "stream": True,
        }

        logger.info("ollama_stream_start", model=self._settings.llm_model)

        async with self._client.stream("POST", "/api/chat", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                data = json.loads(line)
                message = data.get("message", {})
                content = message.get("content", "")
                done = data.get("done", False)
                if content:
                    yield LLMChunk(content=content, done=done)
                elif done:
                    yield LLMChunk(content="", done=True)

    async def health_check(self) -> bool:
        try:
            response = await self._client.get("/api/tags")
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    @staticmethod
    def build_user_message(content: str) -> Message:
        return Message(role=MessageRole.USER, content=content)
