# Chat Operations Runbook

## Monitoring Focus

- Track message latency, reconnect replay counts, retry outcomes, and presence transitions.
- Verify the App Service deployment exposes WebSocket support and HTTPS-only access.
- Inspect structured telemetry for `message_latency`, `reconnect_replay`, `message_retry`, and `presence_transition` events.

## Failure Handling

- If live delivery fails, confirm the WebSocket endpoint is reachable and review recent `message_failed` events.
- If reconnect recovery fails, inspect replay counts and confirm the client sends `last_seen_message_id`.
- If presence becomes stale, verify heartbeat flow and active session cleanup.

## Manual Verification

1. Connect two participants to the same conversation.
2. Send messages in both directions and confirm live updates.
3. Disconnect one participant briefly and confirm replay after reconnect.
4. Leave one participant idle and confirm presence transitions.
