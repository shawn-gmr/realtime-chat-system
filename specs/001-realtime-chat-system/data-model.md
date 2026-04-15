# Data Model: Real-Time Chat System

## Overview

The feature extends an existing authenticated user and conversation-membership domain. It adds durable chat history, reconnect cursors, authoritative global user presence, and session lifecycle tracking while keeping canonical state in PostgreSQL 16.

## Entities

### Conversation

Represents a chat thread that participants can open and exchange messages in.

| Field           | Type                 | Notes                         |
| --------------- | -------------------- | ----------------------------- |
| id              | uuid                 | Primary key                   |
| created_at      | timestamptz          | Creation time                 |
| updated_at      | timestamptz          | Last metadata change          |
| last_message_id | uuid nullable        | Most recent persisted message |
| last_message_at | timestamptz nullable | Last message timestamp        |

**Relationships**:

- One conversation has many conversation_participant rows.
- One conversation has many message rows.
- One conversation is used to scope which users may see each other's global presence.

### Conversation Participant

Represents a user's membership in a conversation and stores per-user cursors.

| Field                | Type                 | Notes                                 |
| -------------------- | -------------------- | ------------------------------------- |
| conversation_id      | uuid                 | Foreign key to conversation           |
| user_id              | uuid                 | Foreign key to existing user identity |
| joined_at            | timestamptz          | Membership creation time              |
| last_read_message_id | uuid nullable        | Most recently acknowledged message    |
| last_read_at         | timestamptz nullable | Last read confirmation time           |

**Validation rules**:

- `(conversation_id, user_id)` must be unique.
- Only participants may open history, connect to the WebSocket channel, or send messages.

### Message

Represents one text message in a conversation.

| Field             | Type        | Notes                                                      |
| ----------------- | ----------- | ---------------------------------------------------------- |
| id                | uuid        | Primary key                                                |
| conversation_id   | uuid        | Foreign key to conversation                                |
| sender_id         | uuid        | Foreign key to existing user identity                      |
| client_message_id | uuid        | Sender-supplied idempotency key                            |
| body              | text        | Message text                                               |
| sent_at           | timestamptz | Server-assigned send time                                  |
| sequence_number   | bigint      | Conversation-scoped authoritative ordering value           |
| delivery_status   | text        | Server response semantics, such as `delivered` or `failed` |

**Validation rules**:

- `body` must be non-empty after trimming.
- `sender_id` must belong to the conversation at send time.
- `(conversation_id, sender_id, client_message_id)` must be unique.
- `sequence_number` must be strictly increasing within a conversation.

### User Presence

Represents the authoritative global presence state of a user across the chat system.

| Field                   | Type                 | Notes                                                               |
| ----------------------- | -------------------- | ------------------------------------------------------------------- |
| user_id                 | uuid                 | Primary key and foreign key to existing user identity               |
| status                  | text                 | `online`, `away`, or `offline`                                      |
| active_connection_count | integer              | Number of active WebSocket sessions across all joined conversations |
| last_activity_at        | timestamptz          | Last heartbeat or message activity                                  |
| last_connected_at       | timestamptz nullable | Last successful connect time                                        |
| last_disconnected_at    | timestamptz nullable | Last disconnect or timeout time                                     |
| updated_at              | timestamptz          | Last projection update                                              |

**Validation rules**:

- One row per `user_id`.
- `status` must be one of `online`, `away`, or `offline`.
- `active_connection_count` cannot be negative.

### WebSocket Session

Represents an active or recently closed socket session for one user in one conversation.

| Field             | Type                 | Notes                                     |
| ----------------- | -------------------- | ----------------------------------------- |
| id                | uuid                 | Primary key                               |
| conversation_id   | uuid                 | Foreign key to conversation               |
| user_id           | uuid                 | Foreign key to existing user identity     |
| connected_at      | timestamptz          | Socket accepted time                      |
| last_heartbeat_at | timestamptz          | Most recent heartbeat                     |
| disconnected_at   | timestamptz nullable | Disconnect time                           |
| disconnect_reason | text nullable        | Client close, timeout, or server shutdown |

**Validation rules**:

- Active sessions are counted into the owning user's global presence projection.
- A session must belong to a valid conversation participant.

## Derived Views

- **Conversation timeline**: Ordered by `sequence_number` for display and replay.
- **Conversation presence roster**: For a given conversation, join `conversation_participant` to `user_presence` to show global user presence only for shared participants.
- **Reconnect replay window**: Messages where `sequence_number` is greater than the participant's last acknowledged cursor.

## State Transitions

### Message lifecycle

1. `received` -> `validated` when membership, body, and idempotency checks pass.
2. `validated` -> `persisted` when the message row and ordering metadata commit successfully.
3. `persisted` -> `broadcast` when the message is emitted to active WebSocket sessions for that conversation.
4. `received` -> `failed` when validation or persistence fails; the client may retry with the same `client_message_id`.

### User presence lifecycle

1. `offline` -> `online` when the user establishes at least one active WebSocket session.
2. `online` -> `away` when the user has no activity for 5 minutes but still has an active session.
3. `online` or `away` -> `offline` when the user has no active connection or no heartbeat for 30 seconds.
4. `offline` -> `online` on reconnect when a new active session is established.

### Participant cursor lifecycle

1. `null` -> `message_id` when the participant first acknowledges delivered history.
2. `message_id(n)` -> `message_id(n+1)` when the client confirms a newer message has been rendered.
3. The stored cursor is reused during reconnect to compute replay messages.

## Indexing Considerations

- Index `message(conversation_id, sequence_number desc)` for newest-first history queries.
- Unique index on `message(conversation_id, sender_id, client_message_id)` for retry deduplication.
- Index `conversation_participant(user_id, conversation_id)` for shared-conversation presence lookups.
- Index `websocket_session(user_id, disconnected_at)` for stale-session cleanup and global presence reconciliation.
