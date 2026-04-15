# Tasks: Real-Time Chat System

**Input**: Design documents from `/specs/001-realtime-chat-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Contract, integration, component, and end-to-end tests are included because the specification and quickstart explicitly require test coverage for each user journey.

**Organization**: Tasks are grouped by user story so each story can be implemented and validated independently after the shared foundation is complete.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the workspace structure and package manifests required by the implementation plan.

- [x] T001 Create the backend project manifest and dependency groups in apps/api/pyproject.toml
- [x] T002 [P] Create the frontend project manifest and scripts in apps/web/package.json
- [x] T003 [P] Create the shared contracts package manifest in packages/contracts/package.json
- [x] T004 [P] Create the shared types package manifest in packages/shared-types/package.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the shared database, application, security, and observability foundation that all user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T005 Create the FastAPI application bootstrap and environment wiring in apps/api/src/app.py
- [x] T006 [P] Configure async SQLAlchemy sessions and metadata registration in apps/api/src/db/session.py
- [x] T007 [P] Configure the Alembic migration environment for chat tables in apps/api/src/db/migrations/env.py
- [x] T008 [P] Define chat ORM models for conversation, participant, message, user_presence, and websocket_session in apps/api/src/db/models/chat.py
- [x] T009 [P] Implement repositories for membership, messages, reconnect cursors, presence, and sessions in apps/api/src/db/repositories/chat_repository.py
- [x] T010 [P] Add conversation access dependencies for REST and WebSocket handlers in apps/api/src/api/dependencies/conversation_access.py
- [x] T011 [P] Add chat telemetry helpers for latency, replay, retries, and presence transitions in apps/api/src/observability/chat_telemetry.py
- [x] T012 [P] Create shared transport and domain types for chat clients in packages/shared-types/src/chat.ts
- [x] T013 Create the frontend chat workspace shell and route composition in apps/web/src/features/chat/ConversationWorkspace.tsx

**Checkpoint**: Shared persistence, routing, auth, telemetry, and frontend shell are ready; user stories can proceed independently.

---

## Phase 3: User Story 1 - Exchange Live Messages (Priority: P1) 🎯 MVP

**Goal**: Let authenticated conversation participants send and receive live messages, reconnect safely, and retry failed sends without duplicates.

**Independent Test**: Put two authenticated users in the same conversation, send messages from both sessions, force a short disconnect for one user, reconnect, and confirm live delivery, replay, and retry behavior all work without refreshing.

### Tests for User Story 1

> **NOTE**: Write these tests first, confirm they fail, then implement the story.

- [x] T014 [P] [US1] Add the AsyncAPI contract test for connect, send_message, message_created, and message_failed frames in apps/api/tests/contract/test_chat_realtime_asyncapi.py
- [x] T015 [P] [US1] Add the backend integration test for live send, reconnect replay, and idempotent retry in apps/api/tests/integration/test_live_message_delivery.py
- [x] T016 [P] [US1] Add the frontend component test for composer send states and live updates in apps/web/tests/component/chat-composer.test.tsx
- [x] T017 [P] [US1] Add the end-to-end two-user live messaging scenario in apps/web/tests/e2e/live-message-delivery.spec.ts
- [x] T047 [P] [US1] Add backend integration test rejecting non-participant WebSocket connect and send attempts in apps/api/tests/integration/test_chat_socket_authorization.py

### Implementation for User Story 1

- [x] T018 [US1] Implement authoritative sequencing and durable persistence in the message delivery service in apps/api/src/libraries/message_delivery/service.py
- [x] T019 [P] [US1] Implement reconnect replay using last_seen_message_id in apps/api/src/libraries/message_delivery/replay.py
- [x] T020 [P] [US1] Implement WebSocket command handling for connect, send_message, and heartbeat in apps/api/src/api/websocket/chat_socket.py
- [x] T048 [US1] Enforce participant authorization failures for WebSocket connect and send commands in apps/api/src/api/websocket/chat_socket.py
- [x] T021 [P] [US1] Implement the browser realtime client for chat commands and events in apps/web/src/services/chatRealtimeClient.ts
- [x] T022 [P] [US1] Implement the message composer with retry state and delivery feedback in apps/web/src/features/chat/MessageComposer.tsx
- [x] T023 [US1] Implement the live conversation stream hook that binds the realtime client to UI state in apps/web/src/features/chat/useLiveConversation.ts

**Checkpoint**: User Story 1 should now support live send, receive, reconnect replay, and retry behavior on its own.

---

## Phase 4: User Story 2 - Review Conversation History (Priority: P2)

**Goal**: Let participants open a conversation, see recent messages immediately, and page older messages without losing context.

**Independent Test**: Open a conversation that already has stored messages, verify the newest messages load first in stable order, then request older messages and confirm they append correctly while preserving the current view.

### Tests for User Story 2

> **NOTE**: Write these tests first, confirm they fail, then implement the story.

- [x] T024 [P] [US2] Add the OpenAPI contract test for paginated message history in apps/api/tests/contract/test_chat_history_openapi.py
- [x] T025 [P] [US2] Add the backend integration test for opening a conversation and loading older messages in apps/api/tests/integration/test_message_history_api.py
- [x] T049 [P] [US2] Add backend integration test rejecting non-participant history reads in apps/api/tests/integration/test_chat_history_authorization.py
- [x] T026 [P] [US2] Add the frontend component test for empty history and older-message pagination in apps/web/tests/component/chat-history-panel.test.tsx
- [x] T027 [P] [US2] Add the end-to-end history hydration scenario in apps/web/tests/e2e/message-history.spec.ts

### Implementation for User Story 2

- [x] T028 [US2] Implement the paginated history query service with stable ordering in apps/api/src/libraries/message_history/service.py
- [x] T029 [P] [US2] Implement the conversation history REST endpoint in apps/api/src/api/rest/chat_history.py
- [x] T050 [US2] Enforce participant authorization failures for the conversation history endpoint in apps/api/src/api/rest/chat_history.py
- [x] T030 [P] [US2] Implement the history HTTP client with cursor pagination in apps/web/src/services/chatHistoryClient.ts
- [x] T031 [P] [US2] Implement the message timeline and empty state UI in apps/web/src/features/chat/MessageHistoryPanel.tsx
- [x] T032 [US2] Implement the history hydration hook for recent and older messages in apps/web/src/features/chat/useMessageHistory.ts

**Checkpoint**: User Story 2 should now load recent history, show an empty state, and paginate older messages independently.

---

## Phase 5: User Story 3 - See Participant Presence (Priority: P3)

**Goal**: Show global participant presence for shared conversations and keep status transitions accurate across online, away, and offline states.

**Independent Test**: Connect two users who share a conversation, verify one appears online, let that user go idle for 5 minutes to become away, then disconnect or stop heartbeats for 30 seconds and confirm the observer sees offline.

### Tests for User Story 3

> **NOTE**: Write these tests first, confirm they fail, then implement the story.

- [x] T033 [P] [US3] Add the OpenAPI contract test for the conversation presence roster in apps/api/tests/contract/test_chat_presence_openapi.py
- [x] T034 [P] [US3] Add the backend integration test for online, away, and offline transitions in apps/api/tests/integration/test_user_presence.py
- [x] T052 [P] [US3] Add backend integration test verifying reconnect restores current presence state before live updates resume in apps/api/tests/integration/test_reconnect_presence_state.py
- [x] T056 [P] [US3] Add backend integration test rejecting non-participant presence roster reads in apps/api/tests/integration/test_chat_presence_authorization.py
- [x] T035 [P] [US3] Add the frontend component test for shared-conversation presence indicators in apps/web/tests/component/participant-presence-strip.test.tsx
- [x] T036 [P] [US3] Add the end-to-end presence visibility and timeout scenario in apps/web/tests/e2e/participant-presence.spec.ts

### Implementation for User Story 3

- [x] T037 [US3] Implement global user presence projection and timeout reconciliation in apps/api/src/libraries/user_presence/service.py
- [x] T038 [P] [US3] Implement the presence roster REST endpoint for shared conversations in apps/api/src/api/rest/chat_presence.py
- [x] T051 [US3] Enforce participant authorization failures for the presence roster endpoint in apps/api/src/api/rest/chat_presence.py
- [x] T039 [P] [US3] Implement presence update broadcasting for shared participants in apps/api/src/api/websocket/presence_events.py
- [x] T040 [P] [US3] Implement the presence bootstrap client in apps/web/src/services/chatPresenceClient.ts
- [x] T041 [P] [US3] Implement the participant presence strip UI in apps/web/src/features/chat/ParticipantPresenceStrip.tsx
- [x] T042 [US3] Implement the global presence state hook and timeout rendering in apps/web/src/features/chat/useParticipantPresence.ts
- [x] T053 [US3] Rehydrate current presence state on reconnect before resuming live presence updates in apps/web/src/features/chat/useParticipantPresence.ts

**Checkpoint**: User Story 3 should now show global participant presence, restore current presence state on reconnect, and apply accurate timeout-driven state changes without depending on unfinished lower-priority work.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finish deployment, observability, performance validation, and operational documentation that spans multiple user stories.

- [x] T043 [P] Add telemetry integration coverage for latency, replay, retries, and presence transitions in apps/api/tests/integration/test_chat_observability.py
- [x] T054 [P] Add latency validation scenarios for message delivery and conversation open thresholds in apps/api/tests/integration/test_chat_latency.py
- [x] T055 [P] Add quickstart steps for recording SC-001 and SC-002 latency measurements in specs/001-realtime-chat-system/quickstart.md
- [x] T044 [P] Add deployment configuration for WebSocket scaling and heartbeat settings in infra/bicep/app-service.bicep
- [x] T045 Update the manual validation and local setup guide in specs/001-realtime-chat-system/quickstart.md
- [x] T046 [P] Add the chat operations runbook for monitoring and failure handling in docs/chat-operations.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational completion.
- **User Story 2 (Phase 4)**: Depends on Foundational completion.
- **User Story 3 (Phase 5)**: Depends on Foundational completion.
- **Polish (Phase 6)**: Depends on the user stories you intend to ship.

### User Story Dependencies

- **US1**: No dependency on other user stories after Phase 2; this is the MVP slice.
- **US2**: No dependency on US1 after Phase 2; it uses the shared message persistence foundation but can be delivered independently.
- **US3**: No dependency on US1 or US2 after Phase 2; it uses the shared session and presence foundation but remains independently testable.

### Within Each User Story

- Tests must be written and confirmed failing before implementation.
- Backend services must be implemented before transport adapters that expose them.
- Client services must be implemented before the hooks and UI components that consume them.
- Each story must satisfy its independent test before moving on.

### Parallel Opportunities

- Setup tasks `T002` through `T004` can run in parallel after `T001` starts.
- Foundational tasks `T006` through `T012` can run in parallel once the application bootstrap approach in `T005` is set.
- After Phase 2, US1, US2, and US3 can be staffed in parallel.
- In each story, all contract, integration, component, and end-to-end tests marked `[P]` can run in parallel.
- In each story, API implementation and web-client implementation tasks marked `[P]` can run in parallel once the story service task begins.

---

## Parallel Example: User Story 1

```bash
# Run User Story 1 tests in parallel:
T014 apps/api/tests/contract/test_chat_realtime_asyncapi.py
T015 apps/api/tests/integration/test_live_message_delivery.py
T016 apps/web/tests/component/chat-composer.test.tsx
T017 apps/web/tests/e2e/live-message-delivery.spec.ts
T047 apps/api/tests/integration/test_chat_socket_authorization.py

# Build User Story 1 implementation pieces in parallel after T018 starts:
T019 apps/api/src/libraries/message_delivery/replay.py
T020 apps/api/src/api/websocket/chat_socket.py
T048 apps/api/src/api/websocket/chat_socket.py
T021 apps/web/src/services/chatRealtimeClient.ts
T022 apps/web/src/features/chat/MessageComposer.tsx
```

## Parallel Example: User Story 2

```bash
# Run User Story 2 tests in parallel:
T024 apps/api/tests/contract/test_chat_history_openapi.py
T025 apps/api/tests/integration/test_message_history_api.py
T026 apps/web/tests/component/chat-history-panel.test.tsx
T027 apps/web/tests/e2e/message-history.spec.ts

# Build User Story 2 implementation pieces in parallel after T028 starts:
T029 apps/api/src/api/rest/chat_history.py
T030 apps/web/src/services/chatHistoryClient.ts
T031 apps/web/src/features/chat/MessageHistoryPanel.tsx
```

## Parallel Example: User Story 3

```bash
# Run User Story 3 tests in parallel:
T033 apps/api/tests/contract/test_chat_presence_openapi.py
T034 apps/api/tests/integration/test_user_presence.py
T052 apps/api/tests/integration/test_reconnect_presence_state.py
T056 apps/api/tests/integration/test_chat_presence_authorization.py
T035 apps/web/tests/component/participant-presence-strip.test.tsx
T036 apps/web/tests/e2e/participant-presence.spec.ts

# Build User Story 3 implementation pieces in parallel after T037 starts:
T038 apps/api/src/api/rest/chat_presence.py
T051 apps/api/src/api/rest/chat_presence.py
T039 apps/api/src/api/websocket/presence_events.py
T040 apps/web/src/services/chatPresenceClient.ts
T041 apps/web/src/features/chat/ParticipantPresenceStrip.tsx
T053 apps/web/src/features/chat/useParticipantPresence.ts
```

---

## Implementation Strategy

### MVP First

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. Validate the live messaging, reconnect replay, and retry scenarios.
5. Ship or demo the MVP before taking on lower-priority stories.

### Incremental Delivery

1. Deliver Setup and Foundational work once.
2. Add US1 and validate it independently.
3. Add US2 and validate history behavior independently.
4. Add US3 and validate presence behavior independently.
5. Finish with cross-cutting telemetry, performance validation, deployment, and operations tasks.

### Parallel Team Strategy

1. One developer completes the shared foundation in Phases 1 and 2.
2. After Phase 2, separate developers can own US1, US2, and US3 in parallel.
3. Reserve one final pass for shared observability, deployment, and runbook work.

---

## Traceability Matrix

| Functional Requirement | Summary                                                                                  | Task IDs                                 |
| ---------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------- |
| FR-001                 | Allow authenticated participants to open and participate in conversations they belong to | T010, T013, T020, T029, T038             |
| FR-002                 | Allow participants to send text messages                                                 | T018, T020, T021, T022                   |
| FR-003                 | Show newly sent messages to connected participants without refresh                       | T014, T015, T017, T020, T021, T023       |
| FR-004                 | Persist sent messages with sender identity and sent time                                 | T008, T009, T018                         |
| FR-005                 | Display recent conversation history on open                                              | T024, T025, T028, T029, T031, T032       |
| FR-006                 | Retrieve older conversation history                                                      | T024, T025, T028, T029, T030, T032       |
| FR-007                 | Maintain stable authoritative conversation order                                         | T018, T028                               |
| FR-008                 | Prevent non-participants from viewing or sending messages                                | T010, T047, T048, T049, T050, T051, T056 |
| FR-009                 | Display global participant presence in shared conversations                              | T033, T037, T038, T040, T041, T042       |
| FR-010                 | Update presence on connect, inactivity, reconnect, disconnect, and heartbeat loss        | T034, T037, T039, T042                   |
| FR-011                 | Restore missed messages and current presence state after reconnect                       | T015, T019, T020, T052, T053             |
| FR-012                 | Show failed-send state and allow retry                                                   | T014, T015, T016, T017, T022, T023       |
| FR-013                 | Provide a clear empty state for conversations with no prior messages                     | T026, T027, T031, T032                   |

## Success Criteria Validation

| Success Criterion | Validation Tasks       |
| ----------------- | ---------------------- |
| SC-001            | T043, T054, T055       |
| SC-002            | T043, T054, T055       |
| SC-003            | T015, T017, T019, T052 |
| SC-004            | T034, T036, T042       |
| SC-005            | T015, T016, T017, T022 |

---

## Notes

- `[P]` means the task can proceed in parallel because it targets a separate file and does not require an unfinished sibling task.
- `[US1]`, `[US2]`, and `[US3]` map tasks directly to the user stories in spec.md.
- All task descriptions include concrete file paths so an implementation agent can execute them without additional planning.
- The recommended MVP scope is Phase 3 only after Setup and Foundational work are complete.
