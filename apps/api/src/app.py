import uuid
from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.rest.chat_history import router as chat_history_router
from api.rest.chat_presence import router as chat_presence_router
from api.websocket.chat_socket import router as chat_socket_router
from db.models.chat import Conversation, ConversationParticipant, Message, UserPresence
from db.session import Base, get_engine, get_session_factory
from settings import get_settings

DEMO_CONVERSATION_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
DEMO_USER_IDS = {
    "alice": uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
    "bob": uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
}


async def initialize_demo_data() -> None:
    engine = get_engine()
    session_factory = get_session_factory()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        conversation = await session.get(Conversation, DEMO_CONVERSATION_ID)
        if conversation is not None:
            return

        now = datetime.now(UTC)
        conversation = Conversation(
            id=DEMO_CONVERSATION_ID,
            created_at=now,
            updated_at=now,
        )
        session.add(conversation)
        session.add_all(
            [
                ConversationParticipant(
                    conversation_id=DEMO_CONVERSATION_ID,
                    user_id=DEMO_USER_IDS["alice"],
                ),
                ConversationParticipant(
                    conversation_id=DEMO_CONVERSATION_ID,
                    user_id=DEMO_USER_IDS["bob"],
                ),
            ]
        )

        seeded_messages = [
            Message(
                conversation_id=DEMO_CONVERSATION_ID,
                sender_id=DEMO_USER_IDS["alice"],
                client_message_id=uuid.UUID("10000000-0000-0000-0000-000000000001"),
                body="Hi Bob, this seeded conversation is ready for manual testing.",
                sequence_number=1,
            ),
            Message(
                conversation_id=DEMO_CONVERSATION_ID,
                sender_id=DEMO_USER_IDS["bob"],
                client_message_id=uuid.UUID("20000000-0000-0000-0000-000000000001"),
                body="Thanks Alice, I can see history and presence from here.",
                sequence_number=2,
            ),
        ]
        session.add_all(seeded_messages)
        session.add_all(
            [
                UserPresence(
                    user_id=DEMO_USER_IDS["alice"],
                    status="offline",
                    active_connection_count=0,
                    last_activity_at=now,
                    updated_at=now,
                ),
                UserPresence(
                    user_id=DEMO_USER_IDS["bob"],
                    status="offline",
                    active_connection_count=0,
                    last_activity_at=now,
                    updated_at=now,
                ),
            ]
        )

        conversation.last_message_id = seeded_messages[-1].id
        conversation.last_message_at = seeded_messages[-1].sent_at
        await session.commit()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(chat_history_router)
    app.include_router(chat_presence_router)
    app.include_router(chat_socket_router)

    @app.on_event("startup")
    async def startup() -> None:
        await initialize_demo_data()

    @app.get("/healthz")
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/demo-config")
    async def demo_config() -> dict[str, object]:
        return {
            "conversation_id": str(DEMO_CONVERSATION_ID),
            "users": {name: str(user_id) for name, user_id in DEMO_USER_IDS.items()},
        }

    return app


app = create_app()
