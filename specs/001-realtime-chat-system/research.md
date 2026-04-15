# Research: Real-Time Chat System

## Decision: Use WebSocket as the real-time transport for live conversation sessions

**Rationale**: WebSocket provides low-latency bidirectional delivery for live messages, reconnect handshakes, heartbeats, and presence updates without requiring repeated polling. It satisfies the live messaging requirement while preserving a thin API boundary.

**Alternatives considered**:

- **Short polling**: Rejected because it adds avoidable latency and unnecessary request overhead for active conversations.
- **Server-Sent Events**: Rejected because client-to-server messaging and heartbeats would still require separate HTTP calls.

## Decision: Store durable conversation data in PostgreSQL 16 only

**Rationale**: PostgreSQL 16 is constitutionally required and can serve as the canonical store for conversation history, membership, reconnect cursors, idempotency keys, and user presence. A single data store reduces operational sprawl and keeps schema governance straightforward.

**Alternatives considered**:

- **Redis for presence**: Rejected because it introduces a second database technology and violates the PostgreSQL-only rule.
- **Document storage for chat history**: Rejected because it is unnecessary for the known access patterns and violates the constitution.

## Decision: Model presence as a global user-level state, exposed only within shared conversations

**Rationale**: The spec now clarifies that presence is global per user rather than conversation-scoped. The backend will maintain one authoritative user presence projection in PostgreSQL and expose that state only to users who share a conversation with the target user.

**Alternatives considered**:

- **Conversation-scoped presence**: Rejected because it conflicts with the clarified product decision and would make the same user appear differently across shared chats.
- **Pure in-memory global presence**: Rejected because it is unreliable across instances and provides weak recoverability and auditability.

## Decision: Use server-assigned per-conversation sequence numbers for message ordering

**Rationale**: The spec clarifies that ordering must be authoritative and system-assigned. A server-generated conversation sequence creates deterministic rendering and reliable reconnect replay when multiple participants send at nearly the same time.

**Alternatives considered**:

- **Client timestamps**: Rejected because clock skew can reorder messages incorrectly.
- **Server receive timestamp only**: Rejected because equal timestamps still require tie-breaking and are less explicit than a sequence.

## Decision: Replay missed messages on reconnect using the last acknowledged message cursor

**Rationale**: On reconnect, the client supplies its last seen message identifier. The server loads all later messages from PostgreSQL and emits them before live streaming resumes, satisfying reconnect recovery without requiring a full reload.

**Alternatives considered**:

- **Full conversation reload on every reconnect**: Rejected because it adds unnecessary latency and payload size.
- **Live-only reconnect with no replay**: Rejected because it fails FR-011 and SC-003.

## Decision: Use idempotent client_message_id values for retry safety

**Rationale**: Failed message sends must be retryable without creating duplicates. A sender-scoped idempotency key lets the backend safely accept retries and maintain a single delivered message.

**Alternatives considered**:

- **No deduplication**: Rejected because retries can duplicate user-visible messages.
- **Body-and-time comparison**: Rejected because it is error-prone under concurrency.

## Decision: Separate HTTP and WebSocket contracts by interaction style

**Rationale**: HTTP is a better fit for paginated history and reading the currently visible presence roster for a conversation, while WebSocket is the right fit for live message and presence change events.

**Alternatives considered**:

- **WebSocket-only surface**: Rejected because history and initial reads become harder to validate and cache.
- **HTTP-only surface**: Rejected because it does not satisfy the low-latency live delivery requirement cleanly.

## Decision: Instrument message delivery, reconnect recovery, and user presence transitions

**Rationale**: Application Insights must receive structured telemetry for operational transparency. The highest-value signals for this feature are message latency, reconnect replay success, failed sends, and transitions between online, away, and offline.

**Alternatives considered**:

- **Minimal request logging**: Rejected because it leaves WebSocket behavior and business events opaque.
- **Ad hoc debugging output**: Rejected because it violates the observability principle.
