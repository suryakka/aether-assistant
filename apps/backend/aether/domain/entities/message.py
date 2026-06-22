from enum import StrEnum


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class SessionStatus(StrEnum):
    IDLE = "idle"
    LISTENING = "listening"
    WATCHING = "watching"
    THINKING = "thinking"
    RESEARCHING = "researching"
    EXECUTING = "executing"
    DONE = "done"
    ERROR = "error"
