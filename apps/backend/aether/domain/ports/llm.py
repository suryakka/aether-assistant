from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Protocol

from aether.domain.entities.chat import Message


@dataclass
class LLMChunk:
    content: str
    done: bool = False


class LLMPort(Protocol):
    async def stream_chat(self, messages: list[Message]) -> AsyncIterator[LLMChunk]: ...

    async def health_check(self) -> bool: ...
