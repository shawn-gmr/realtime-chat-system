import uuid
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.models.chat import Conversation, ConversationParticipant, Message
from db.session import Base


@pytest.fixture
async def session(tmp_path: Path) -> AsyncIterator[AsyncSession]:
    database_path = tmp_path / "chat-system-test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def seeded_conversation(session: AsyncSession) -> dict[str, uuid.UUID]:
    conversation_id = uuid.uuid4()
    sender_id = uuid.uuid4()
    receiver_id = uuid.uuid4()

    session.add(Conversation(id=conversation_id))
    session.add_all(
        [
            ConversationParticipant(conversation_id=conversation_id, user_id=sender_id),
            ConversationParticipant(conversation_id=conversation_id, user_id=receiver_id),
        ]
    )
    await session.commit()
    return {
        "conversation_id": conversation_id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
    }


@pytest.fixture
async def seeded_messages(
    session: AsyncSession, seeded_conversation: dict[str, uuid.UUID]
) -> dict[str, uuid.UUID]:
    for index in range(3):
        session.add(
            Message(
                conversation_id=seeded_conversation["conversation_id"],
                sender_id=seeded_conversation["sender_id"],
                client_message_id=uuid.uuid4(),
                body=f"message-{index}",
                sequence_number=index + 1,
            )
        )
    await session.commit()
    return seeded_conversation
