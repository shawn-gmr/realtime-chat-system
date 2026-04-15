import uuid
from collections import defaultdict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.dependencies.conversation_access import require_websocket_participant
from api.websocket.presence_events import build_presence_updated_event
from db.repositories.chat_repository import ChatRepository
from db.session import get_session_factory
from libraries.message_delivery.replay import build_history_sync_payload
from libraries.message_delivery.service import MessageDeliveryService
from libraries.user_presence.service import UserPresenceService
from observability.chat_telemetry import get_chat_telemetry

router = APIRouter(tags=["chat-realtime"])


class ConversationHub:
    def __init__(self) -> None:
        self._connections: dict[uuid.UUID, set[WebSocket]] = defaultdict(set)

    async def join(self, conversation_id: uuid.UUID, websocket: WebSocket) -> None:
        self._connections[conversation_id].add(websocket)

    async def leave(self, conversation_id: uuid.UUID, websocket: WebSocket) -> None:
        self._connections[conversation_id].discard(websocket)

    async def broadcast_json(self, conversation_id: uuid.UUID, payload: dict[str, object]) -> None:
        for websocket in list(self._connections[conversation_id]):
            await websocket.send_json(payload)


hub = ConversationHub()


@router.websocket("/ws/conversations/{conversation_id}")
async def conversation_socket(websocket: WebSocket, conversation_id: uuid.UUID) -> None:
    await websocket.accept()
    telemetry = get_chat_telemetry()
    session_factory = get_session_factory()

    async with session_factory() as session:
        try:
            user_id = await require_websocket_participant(
                websocket=websocket,
                conversation_id=conversation_id,
                session=session,
            )
        except Exception:
            await websocket.close(code=4403)
            return

        repo = ChatRepository(session)
        await repo.create_websocket_session(conversation_id=conversation_id, user_id=user_id)
        presence_service = UserPresenceService(telemetry)
        current_presence = await presence_service.mark_online(session=session, user_id=user_id)
        await hub.join(conversation_id=conversation_id, websocket=websocket)
        await hub.broadcast_json(
            conversation_id=conversation_id,
            payload=build_presence_updated_event(conversation_id, current_presence),
        )

        try:
            connect_payload = await websocket.receive_json()
            last_seen_raw = connect_payload.get("last_seen_message_id")
            last_seen_message_id = uuid.UUID(last_seen_raw) if last_seen_raw else None
            await websocket.send_json(
                await build_history_sync_payload(
                    session=session,
                    telemetry=telemetry,
                    conversation_id=conversation_id,
                    last_seen_message_id=last_seen_message_id,
                )
            )

            message_service = MessageDeliveryService(telemetry)
            while True:
                payload = await websocket.receive_json()
                message_type = payload.get("type")
                if message_type == "send_message":
                    message_payload = await message_service.send_message(
                        session=session,
                        conversation_id=conversation_id,
                        sender_id=user_id,
                        client_message_id=uuid.UUID(payload["client_message_id"]),
                        body=payload["body"],
                    )
                    await hub.broadcast_json(
                        conversation_id=conversation_id,
                        payload={
                            "type": "message_created",
                            "conversation_id": str(conversation_id),
                            "message": message_payload,
                        },
                    )
                elif message_type == "heartbeat":
                    refreshed_presence = await presence_service.touch(session=session, user_id=user_id)
                    await websocket.send_json(
                        build_presence_updated_event(conversation_id, refreshed_presence)
                    )
                elif message_type == "request_history":
                    before_message_id = payload.get("before_message_id")
                    history_payload = await build_history_sync_payload(
                        session=session,
                        telemetry=telemetry,
                        conversation_id=conversation_id,
                        last_seen_message_id=uuid.UUID(before_message_id) if before_message_id else None,
                    )
                    await websocket.send_json(history_payload)
        except WebSocketDisconnect:
            pass
        finally:
            await hub.leave(conversation_id=conversation_id, websocket=websocket)
            offline_presence = await presence_service.mark_offline(session=session, user_id=user_id)
            await hub.broadcast_json(
                conversation_id=conversation_id,
                payload=build_presence_updated_event(conversation_id, offline_presence),
            )
