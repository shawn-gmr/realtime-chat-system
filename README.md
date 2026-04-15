# chat-system

Monorepo for a real-time chat system built around a FastAPI backend, a React 19 web client, shared TypeScript contracts, and infrastructure assets for Azure deployment.

The current feature set focuses on:

- real-time message delivery over WebSocket
- durable message history with pagination
- global user presence projected into shared conversations
- reconnect replay for missed messages
- contract-first API design with OpenAPI and AsyncAPI artifacts

## Architecture

The repository is split into four main areas:

```text
apps/
  api/        FastAPI backend and backend tests
  web/        React web client, component tests, and Playwright e2e tests
packages/
  shared-types/  Shared TypeScript chat contracts
  contracts/     Contract packaging metadata
infra/
  bicep/      Azure infrastructure definitions
specs/
  001-realtime-chat-system/  Feature spec, plan, tasks, research, and contracts
```

### Backend

- Python 3.13
- FastAPI
- async SQLAlchemy
- Pydantic
- Alembic
- structured logging via `python-json-logger`

### Frontend

- TypeScript 5
- React 19
- Material UI
- Vitest for component tests
- Playwright for end-to-end tests

### Deployment Target

- Azure App Service
- Azure Application Insights
- PostgreSQL 16 as the intended production data store

For local development, the backend currently defaults to `sqlite+aiosqlite:///./chat-system.db` when `CHAT_DATABASE_URL` is not set.

## Implemented Interfaces

### HTTP

- `GET /api/conversations/{conversation_id}/messages`
  Returns paginated message history.
- `GET /api/conversations/{conversation_id}/presence`
  Returns the current presence roster for participants in a conversation.

### WebSocket

- `WS /ws/conversations/{conversation_id}`
  Supports connect, send message, heartbeat, history replay, and presence updates.

Client/server payload types are shared in `packages/shared-types/src/chat.ts`.

## Repository Documents

- Feature specification: `specs/001-realtime-chat-system/spec.md`
- Implementation plan: `specs/001-realtime-chat-system/plan.md`
- Quickstart and validation flow: `specs/001-realtime-chat-system/quickstart.md`
- HTTP contract: `specs/001-realtime-chat-system/contracts/chat-http.openapi.yaml`
- Realtime contract: `specs/001-realtime-chat-system/contracts/chat-realtime.asyncapi.yaml`
- Operations runbook: `docs/chat-operations.md`

## Prerequisites

- Python 3.13
- Node.js 22
- npm

Optional for production-aligned local work:

- PostgreSQL 16
- Application Insights connection string

## Local Setup

### Backend

Install backend dependencies from the repository root:

```bash
python -m pip install -e './apps/api[dev]'
```

Run the backend test suite from the repository root:

```bash
PYTHONPATH=apps/api/src python -m pytest apps/api/tests
```

Start the API locally from the repository root:

```bash
PYTHONPATH=apps/api/src uvicorn app:app --app-dir apps/api/src --reload
```

Health endpoint:

```text
GET /healthz
```

### Frontend

Install frontend dependencies:

```bash
cd apps/web
npm ci
```

Run component tests:

```bash
npm test
```

Run Playwright end-to-end tests:

```bash
npm run test:e2e
```

## Testing

The repository keeps unit/component and browser-level tests separate.

### Backend

```bash
PYTHONPATH=apps/api/src python -m pytest apps/api/tests
```

### Web Component Tests

```bash
cd apps/web
npm test
```

### Web End-to-End Tests

```bash
cd apps/web
npm run test:e2e
```

## CI

GitHub Actions runs three separate jobs on pull requests targeting `dev` and `main`:

- backend tests
- web unit tests
- web end-to-end tests

Workflow file:

```text
.github/workflows/ci.yml
```

## Current State

The repo contains the backend API, frontend chat components, shared contracts, tests, specs, and Azure deployment assets for the real-time chat feature.

One notable gap is frontend project wiring for a TypeScript build: `apps/web/package.json` includes a `build` script, but there is no `tsconfig.json` in `apps/web` yet, so `npm run build` is not currently a working verification step.

## Observability

The backend emits structured telemetry for:

- message delivery latency
- reconnect replay counts
- retry outcomes
- presence transitions

Operational notes live in `docs/chat-operations.md`.
