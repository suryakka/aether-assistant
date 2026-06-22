from collections.abc import AsyncIterator
from dataclasses import dataclass, field

from aether.domain.entities.chat import Message
from aether.domain.entities.message import MessageRole, SessionStatus
from aether.domain.ports.llm import LLMPort
from aether.infrastructure.logging.setup import get_logger

logger = get_logger(__name__)


@dataclass
class ChatEvent:
    type: str
    data: dict = field(default_factory=dict)


class ProcessChatUseCase:
    def __init__(self, llm: LLMPort) -> None:
        self._llm = llm
        self._history: list[Message] = []

    async def process_query(self, content: str) -> AsyncIterator[ChatEvent]:
        if not content.strip():
            yield ChatEvent(type="error", data={"message": "Empty query"})
            return

        user_message = Message(role=MessageRole.USER, content=content.strip())
        self._history.append(user_message)

        yield ChatEvent(type="status", data={"status": SessionStatus.THINKING.value})

        full_response = ""
        try:
            async for chunk in self._llm.stream_chat(self._history):
                if chunk.content:
                    full_response += chunk.content
                    yield ChatEvent(
                        type="response_chunk",
                        data={"content": chunk.content},
                    )
        except Exception as exc:
            logger.exception("chat_error", error=str(exc))
            yield ChatEvent(type="error", data={"message": str(exc)})
            yield ChatEvent(type="status", data={"status": SessionStatus.ERROR.value})
            return

        if full_response:
            self._history.append(
                Message(role=MessageRole.ASSISTANT, content=full_response)
            )

        yield ChatEvent(type="done", data={"content": full_response})
        yield ChatEvent(type="status", data={"status": SessionStatus.DONE.value})

    def clear_history(self) -> None:
        self._history.clear()
