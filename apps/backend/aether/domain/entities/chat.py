from dataclasses import dataclass, field
from datetime import UTC, datetime

from aether.domain.entities.message import MessageRole


@dataclass(frozen=True)
class Message:
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_ollama(self) -> dict[str, str]:
        return {"role": self.role.value, "content": self.content}
