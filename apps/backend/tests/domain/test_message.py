from datetime import UTC, datetime

from aether.domain.entities.chat import Message
from aether.domain.entities.message import MessageRole


def test_message_to_ollama():
    msg = Message(role=MessageRole.USER, content="Hello")
    assert msg.to_ollama() == {"role": "user", "content": "Hello"}


def test_message_roles():
    assert MessageRole.USER.value == "user"
    assert MessageRole.ASSISTANT.value == "assistant"
    assert MessageRole.SYSTEM.value == "system"


def test_message_has_timestamp():
    msg = Message(role=MessageRole.USER, content="Hi")
    assert isinstance(msg.timestamp, datetime)
    assert msg.timestamp.tzinfo == UTC
