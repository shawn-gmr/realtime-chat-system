# Quickstart: Real-Time Chat System

## Goal

Validate live messaging, history loading, reconnect recovery, and global user presence for the real-time chat feature using the contract-first design in this spec.

## Prerequisites

1. Provision PostgreSQL 16 for local or shared development use.
2. Expose the existing authentication and conversation-membership boundary in development mode.
3. Configure Application Insights or an equivalent local telemetry sink so message and presence events are observable during testing.
4. Prepare two test users who belong to the same conversation.

## Implementation Order

1. Implement the contract artifacts first: HTTP history/presence endpoints and WebSocket frame schemas.
2. Build backend libraries in this order: message_history, user_presence, then message_delivery.
3. Add thin HTTP and WebSocket adapters on top of those libraries.
4. Add the frontend chat view, live message handling, reconnect flow, and presence indicators.
5. Add telemetry for message latency, reconnect replay, failed sends, and presence transitions before feature completion.

## Validation Flow

1. Start the API service and web client with PostgreSQL connected.
2. Sign in as two conversation participants in separate browser sessions.
3. Open the same conversation in both sessions and confirm recent history is visible.
4. Send a message from one user and verify the second user sees it without refresh.
5. Send near-simultaneous messages from both users and verify the conversation renders a stable, deterministic order.
6. Disconnect one browser session, send additional messages from the other session, reconnect the first session, and verify missed messages are replayed automatically.
7. Leave one user idle for 5 minutes to transition to `away`, then disconnect entirely or stop heartbeats for 30 seconds and verify the user becomes `offline` for the other participant.
8. Force a failed send, retry it with the same client message identifier, and verify only one delivered message appears.

## Required Test Coverage Before Tasks Are Complete

1. Contract tests for the HTTP and WebSocket schemas.
2. Backend integration tests for send, replay, global presence timeout, and authorization.
3. Frontend interaction tests for empty state, live updates, and retry handling.
4. End-to-end tests for two-user messaging, reconnect recovery, and presence transitions.

## Local Setup

1. Install backend dependencies with `cd apps/api && python -m pip install -e .[dev]`.
2. Install frontend dependencies with `cd apps/web && npm install`.
3. Start the API with `cd apps/api && uvicorn src.app:app --reload`.
4. Serve the web client with your preferred React dev server wiring for `apps/web`.

## Latency Recording

1. Capture message send-to-visible latency for at least 20 sends and confirm 95% stay under 2 seconds.
2. Capture conversation open-to-history-visible latency for at least 20 opens and confirm 95% stay under 3 seconds.
3. Record the resulting measurements alongside telemetry output before closing the feature.

## Telemetry Checks

1. Confirm message delivery latency metrics are emitted for every successful send.
2. Confirm reconnect events record replay counts and completion status.
3. Confirm presence transitions emit structured events with conversation_id and user_id.
4. Confirm failed sends and successful retries are separately visible in telemetry.
