from collections.abc import AsyncIterator

import pytest

from aether.application.use_cases.process_chat import ProcessChatUseCase
from aether.domain.entities.chat import Message
from aether.domain.entities.message import MessageRole, SessionStatus
from aether.domain.ports.llm import LLMChunk


class MockLLM:
    def __init__(self, chunks: list[str] | None = None, raise_error: bool = False) -> None:
        self._chunks = chunks or ["Hello", " world"]
        self._raise_error = raise_error
        self.received_messages: list[Message] = []

    async def stream_chat(self, messages: list[Message]) -> AsyncIterator[LLMChunk]:
        self.received_messages = list(messages)
        if self._raise_error:
            raise RuntimeError("LLM unavailable")
        for i, text in enumerate(self._chunks):
            is_last = i == len(self._chunks) - 1
            yield LLMChunk(content=text, done=is_last)

    async def health_check(self) -> bool:
        return True


@pytest.mark.asyncio
async def test_process_query_streams_chunks():
    llm = MockLLM(chunks=["Hi", " there"])
    use_case = ProcessChatUseCase(llm=llm)

    events = [e async for e in use_case.process_query("Test question")]

    types = [e.type for e in events]
    assert "status" in types
    assert "response_chunk" in types
    assert "done" in types

    chunks = [e.data["content"] for e in events if e.type == "response_chunk"]
    assert chunks == ["Hi", " there"]

    done_event = next(e for e in events if e.type == "done")
    assert done_event.data["content"] == "Hi there"


@pytest.mark.asyncio
async def test_process_query_empty():
    use_case = ProcessChatUseCase(llm=MockLLM())
    events = [e async for e in use_case.process_query("   ")]

    assert len(events) == 1
    assert events[0].type == "error"


@pytest.mark.asyncio
async def test_process_query_error():
    use_case = ProcessChatUseCase(llm=MockLLM(raise_error=True))
    events = [e async for e in use_case.process_query("Hello")]

    error_events = [e for e in events if e.type == "error"]
    assert len(error_events) == 1
    assert "LLM unavailable" in error_events[0].data["message"]


@pytest.mark.asyncio
async def test_process_query_builds_history():
    llm = MockLLM(chunks=["Answer"])
    use_case = ProcessChatUseCase(llm=llm)

    _ = [e async for e in use_case.process_query("Question")]

    assert len(llm.received_messages) == 1
    assert llm.received_messages[0].role == MessageRole.USER
    assert llm.received_messages[0].content == "Question"


@pytest.mark.asyncio
async def test_clear_history():
    llm = MockLLM(chunks=["Answer"])
    use_case = ProcessChatUseCase(llm=llm)

    await anext(use_case.process_query("Question"))
    use_case.clear_history()

    assert len(use_case._history) == 0


@pytest.mark.asyncio
async def test_thinking_status_emitted():
    use_case = ProcessChatUseCase(llm=MockLLM())
    events = [e async for e in use_case.process_query("Hi")]

    status_events = [e for e in events if e.type == "status"]
    statuses = [e.data["status"] for e in status_events]
    assert SessionStatus.THINKING.value in statuses
    assert SessionStatus.DONE.value in statuses
