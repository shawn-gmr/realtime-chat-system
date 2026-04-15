# Implementation Plan: Real-Time Chat System

**Branch**: `[001-build-realtime-chat]` | **Date**: 2026-04-15 | **Spec**: `/specs/001-realtime-chat-system/spec.md`
**Input**: Feature specification from `/specs/001-realtime-chat-system/spec.md`

## Summary

Deliver a real-time chat capability with WebSocket-based live messaging, PostgreSQL-backed durable history, reconnect replay, and global user presence visible only within shared conversations. The implementation stays constitution-compliant by using FastAPI, async SQLAlchemy, PostgreSQL 16, and React 19, while rejecting Redis for presence and keeping transport handlers thin over reusable backend libraries.

## Technical Context

**Language/Version**: Python 3.13 for backend services; TypeScript 5 with React 19 for the web client  
**Primary Dependencies**: FastAPI, Starlette WebSocket support, async SQLAlchemy, Pydantic, Alembic, React 19, Material-UI  
**Storage**: PostgreSQL 16 for message history, membership, global user presence, reconnect cursors, idempotency keys, and session lifecycle records  
**Testing**: pytest for backend unit and integration tests, contract validation for OpenAPI and AsyncAPI artifacts, frontend component tests, Playwright end-to-end scenarios  
**Target Platform**: Azure-hosted web application with stateless API and WebSocket services plus modern desktop and mobile browsers  
**Project Type**: Web application with a stateless API boundary and real-time WebSocket channel  
**Performance Goals**: 95% of live messages visible to connected participants within 2 seconds; 95% of conversation opens complete within 3 seconds; reconnect restores missed messages without reopening the conversation; presence transitions to offline within 30 seconds of heartbeat loss  
**Constraints**: PostgreSQL 16 is the only permitted data store; API and WebSocket handlers remain thin; all database access is async; field names remain snake_case across contracts; structured telemetry must flow to Application Insights; HTTPS only; existing auth boundary is reused  
**Scale/Scope**: Initial release supports authenticated conversation participants, paginated histories, reconnect recovery, global presence projection, and low-thousands of concurrent active WebSocket sessions per deployment unit

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

- **Principles I and XII - Specification and testability**: PASS. The spec now contains explicit clarifications for ordering, away timeout, offline timeout, and presence scope, making the feature directly testable.
- **Principles II, III, and VI - Library-first and API boundary**: PASS. Message delivery, message history, and user presence remain reusable backend libraries. REST and WebSocket layers stay as transport adapters.
- **Principle IV - Agent/orchestrator architecture**: PASS. This feature remains inside the constitution's exemption for thin API handlers and simple CRUD-style interaction flows.
- **Principle VII - Durable technology commitments**: PASS. The design uses Python 3.13, FastAPI, React 19, Material-UI, and PostgreSQL 16 exclusively. Redis is rejected.
- **Principles VIII and X - Contract consistency and security**: PASS. Contracts use snake_case, presence visibility is limited to shared conversations, and auth continues through the established Entra-compatible boundary.
- **Principle IX - Async, concurrency, resilience**: PASS. The design includes async persistence, heartbeats, replay-on-reconnect, idempotent sends, and explicit stale-session handling.
- **Principles XI and XIII - Operations and observability**: PASS. The plan requires Application Insights telemetry for live delivery, reconnect recovery, and presence transitions, and remains deployable through Azure-oriented automation.

**Post-Design Re-check**: PASS. Research, data model, quickstart, and contracts align with the clarified spec and keep global presence as a user-level state exposed only in shared-conversation contexts.

## Project Structure

### Documentation (this feature)

```text
specs/001-realtime-chat-system/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── chat-http.openapi.yaml
│   └── chat-realtime.asyncapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
apps/
├── api/
│   ├── src/
│   │   ├── api/
│   │   │   ├── rest/
│   │   │   └── websocket/
│   │   ├── libraries/
│   │   │   ├── message_delivery/
│   │   │   ├── message_history/
│   │   │   └── user_presence/
│   │   ├── db/
│   │   │   ├── migrations/
│   │   │   ├── models/
│   │   │   └── repositories/
│   │   └── observability/
│   └── tests/
│       ├── contract/
│       ├── integration/
│       └── unit/
└── web/
    ├── src/
    │   ├── features/chat/
    │   ├── services/
    │   └── types/
    └── tests/
        ├── component/
        └── e2e/

packages/
├── contracts/
└── shared-types/

infra/
└── bicep/
```

**Structure Decision**: Use a monorepo-friendly web application layout with separate API and web applications plus shared contracts and shared types packages. This supports typed clients, reusable backend libraries, and contract-driven development without introducing any non-approved runtimes or data stores.

## Complexity Tracking

No constitutional violations are accepted. Redis-backed presence remains explicitly rejected as an alternative rather than justified as an exception.
