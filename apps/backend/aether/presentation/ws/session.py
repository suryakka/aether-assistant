import json
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from aether.application.use_cases.process_chat import ProcessChatUseCase
from aether.domain.entities.message import SessionStatus
from aether.infrastructure.logging.setup import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.websocket("/ws/session/{session_id}")
async def session_websocket(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    container = websocket.app.state.container
    use_case: ProcessChatUseCase = container.process_chat_use_case_factory()
    logger.info("ws_connected", session_id=session_id)

    await _send(websocket, "status", {"status": SessionStatus.IDLE.value})

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                message: dict[str, Any] = json.loads(raw)
            except json.JSONDecodeError:
                await _send(websocket, "error", {"message": "Invalid JSON"})
                continue

            msg_type = message.get("type")

            if msg_type == "query":
                content = message.get("content", "")
                async for event in use_case.process_query(content):
                    await _send(websocket, event.type, event.data)
                await _send(websocket, "status", {"status": SessionStatus.IDLE.value})

            elif msg_type == "clear":
                use_case.clear_history()
                await _send(websocket, "status", {"status": SessionStatus.IDLE.value})

            else:
                await _send(websocket, "error", {"message": f"Unknown type: {msg_type}"})

    except WebSocketDisconnect:
        logger.info("ws_disconnected", session_id=session_id)


async def _send(websocket: WebSocket, event_type: str, data: dict) -> None:
    await websocket.send_text(json.dumps({"type": event_type, "data": data}))
