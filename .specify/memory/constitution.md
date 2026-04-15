<!--
Sync Impact Report — speckit.constitution validation run
=========================================================
Version: 3.6.0 (no change — validation-only run)
Previous version: 3.6.0

Modified principles: None
Added sections: None
Removed sections: None (Docker lines removed from Principle VII in prior edit)

Dependent artifact updates:
  ✅ .specify/templates/plan-template.md — aligned (references Principle VII)
  ✅ .specify/templates/spec-template.md — no principle refs, template-safe
  ✅ .specify/templates/tasks-template.md — fixed: Principle IX → XII
  ✅ .github/copilot-code-review-instructions.md — fixed: removed Docker
  ✅ .github/copilot-instructions.md — no changes needed

Deferred items:
  - Completed specs (002–009) reference pre-v3.6.0 principle numbers;
    left unchanged (historical artifacts, self-documenting via principle names)
-->

# Sales Prospecting Platform Constitution

## Core Principles

### I. Specification Primacy, Executability, and Validation

Specifications are the primary source of truth for the platform. Code, plans, tasks, contracts, tests, diagrams, and operational changes MUST serve the specification rather than replace it.

- The authoritative development artifact for any feature is the specification and its approved supporting design documents — not the current codebase
- Specifications MUST be precise, complete, testable, and unambiguous enough to drive implementation plans, contracts, tasks, and tests
- No contributor, including AI coding assistants, may silently guess missing product or technical intent; unresolved ambiguity MUST be marked explicitly using a visible notation such as `[NEEDS CLARIFICATION: ...]`
- Specifications MUST undergo continuous validation for ambiguity, contradiction, incompleteness, requirement drift, and conflicts with the constitution
- Acceptance criteria, non-functional requirements, and constraints MUST be stated in a form that can be validated by tests, review, or operational checks
- Production incidents, operational learnings, performance findings, and security discoveries that materially affect behavior MUST result in updates to the relevant specification and/or implementation plan
- Multiple implementation approaches MAY be explored from the same approved specification when evaluating tradeoffs such as cost, maintainability, latency, or operability, but each variant MUST remain traceable back to the same source specification
- High-level planning documents MUST remain readable and decision-oriented; detailed algorithms, code-heavy notes, and verbose implementation mechanics belong in supporting artifacts, not the main plan
- Specifications MUST avoid speculative features and future-proofing not justified by active requirements

### II. Library-First Design

All core system capabilities MUST be implemented as standalone, reusable libraries before being composed into application workflows.

- Every agent, orchestrator, and domain capability MUST exist as an independently testable library
- Libraries MUST have explicit, well-defined input/output contracts
- Libraries MUST NOT depend on global state or shared mutable state
- Libraries MUST be composable and usable outside of the primary application context
- No feature may be implemented directly inside API handlers, orchestrators, or UI layers without first being expressed as a reusable library
- Orchestrators compose libraries — they do not contain business logic themselves
- Tight coupling between libraries is prohibited; dependencies MUST remain explicit and minimal

### III. Interface Mandate (CLI / Programmatic Boundary)

All core libraries and agents MUST expose a clear, testable interface boundary.

- Every library MUST expose functionality through a programmatic interface with explicit inputs and outputs
- Where appropriate, libraries SHOULD expose a CLI interface:
  - Accept input via arguments, stdin, or files
  - Produce output via stdout or structured formats (e.g., JSON)
- Interfaces MUST be deterministic, observable, and testable without requiring full system orchestration
- No critical functionality may be hidden behind internal-only calls that cannot be invoked or validated independently
- Interfaces MUST support automation, scripting, and test harness integration

### IV. Agent-First, Orchestrated Architecture

The system MUST be built as a multi-agent platform where every unit of work is either an **agent** or an **orchestrator**.

- **Orchestrators** coordinate specialized agents and are pure async Python components — they are NOT LLM agents
- Agent dependencies MUST form a **Directed Acyclic Graph (DAG)** with no cycles
- Three agent classes are supported:
  - **Tool-only agents**: no LLM, execute tools directly
  - **LLM-powered agents**: use AI models for reasoning, classification, extraction, or synthesis
  - **Algorithmic agents**: deterministic logic without LLM usage
- Orchestrators MAY coordinate fan-out execution with configurable semaphore limits
- Orchestrators are responsible for merging outputs, persisting results, and advancing workflow state
- Agents and orchestrators MUST remain composable, reusable, and independently testable libraries
- Thin API handlers, health checks, and simple CRUD operations that do not involve pipeline logic, AI, or multi-step workflows are exempt from the agent/orchestrator classification

### V. Right-Sized AI and Azure AI Foundry Default

AI usage MUST be deliberate, observable, and replaceable.

- **Microsoft Foundry / Azure AI Foundry** is the default AI workload platform for agent definitions, model deployments, tools, and evaluations
- The cheapest effective approach MUST be used for each task
- Work that can be handled algorithmically or by tool-only agents MUST NOT use an LLM
- AI provider and model selection MUST be configurable per agent at runtime
- Provider, model, credentials reference, rate limits, and cost metadata MUST be stored in configuration or the database — never hardcoded in application logic
- Real-time token, latency, and cost monitoring is mandatory for all LLM-backed agents
- Changing an agent's model or provider MUST NOT require application code changes when configuration alone can satisfy the need

### VI. API-First, Stateless Service Boundary

All backend capabilities MUST be exposed through a stateless API boundary.

- The API layer is the only supported application boundary for frontend interaction
- Frontend code MUST NOT access the database, agent pipeline, or external services directly
- Long-running work MUST use an async pattern such as trigger → queue → progress/status notification
- API operations SHOULD be single-purpose and independently testable
- Platform state transitions MUST be explicit, observable, and recoverable
- Integrations with external systems (CRM, ERP, third-party services) MUST flow through defined service boundaries, never ad hoc scripts or direct client-side calls

### VII. Durable Technology Commitments

The following technology choices are non-negotiable unless amended:

- **Backend / Agent Pipeline**: Python 3.13, FastAPI, async SQLAlchemy, Pydantic
- **Frontend**: React 19, TypeScript 5, Material-UI
- **Frontend Structure**: monorepo-friendly module boundaries with shared UI, typed API clients, and shared types isolated in dedicated libraries
- **Database**: PostgreSQL 16 exclusively
- **AI Platform**: Azure AI Foundry as the default AI platform
- **Hosting / Cloud**: Azure — Azure App Service for production compute
- **Infrastructure as Code**: Bicep
- **Edge / CDN**: Azure Front Door (when required)

No alternative language, framework, database, or runtime version may be introduced without a constitutional amendment. Version upgrades (e.g., Python 3.13 → 3.14) require an amendment to prevent silent drift by contributors or AI agents.

### VIII. Naming, Contracts, and Type Consistency

All cross-system contracts MUST remain explicit and consistent.

- All identifiers across database, backend, API contracts, and frontend types MUST use **snake_case**
- Field names MUST match exactly across the API boundary unless a documented transformation layer exists
- Frontend HTTP clients MUST be typed
- Shared contract definitions SHOULD be centralized and reused
- CSV exports MAY use presentation-friendly headers when required for business consumption, but internal canonical field names remain snake_case
- No hidden or implicit contract drift is permitted between services, agents, APIs, and UI

### IX. Async, Concurrency, and Resilience by Default

The system MUST be safe under concurrent, long-running, and failure-prone workloads.

- All database access MUST be asynchronous and non-blocking
- All queries MUST use async database sessions and pooled connections
- External API calls MUST implement explicit timeouts, retries with backoff, and concurrency limits
- Circuit breaker behavior MUST protect unstable integrations
- Long-running jobs MUST support heartbeat monitoring and stale/zombie job detection
- Recovery paths MUST exist for interrupted jobs, partial fan-out failures, and downstream unavailability
- Cost-aware caching or reference-data checks MUST be used before invoking expensive external services where practical

### X. Security, Secrets, and Network Isolation

Security controls are mandatory and built into the platform.

- All secrets, credentials, tokens, and connection strings MUST be stored in **Azure Key Vault** or an approved secure secret store
- No secrets may be committed to source control or embedded in application code
- Applications MUST retrieve secrets at runtime
- Data access MUST follow least-privilege principles across agents, APIs, storage, and operational tooling
- Authentication and authorization MUST use **Azure Entra ID (RBAC)** — no custom auth schemes
- Local development MAY use a simplified auth bypass or mock identity provider; the auth boundary interface MUST remain identical so switching to Entra ID requires zero application code changes
- All database queries MUST use parameterized statements — no raw SQL string concatenation
- All API inputs MUST be validated at the boundary (Pydantic models for backend, typed schemas for frontend)
- Frontend MUST enforce XSS prevention practices; Content Security Policy (CSP) headers MUST be configured
- All traffic MUST use HTTPS with TLS 1.2+ — HTTP is prohibited in all environments
- OWASP Top 10 compliance MUST be verified as part of code review
- Dependency vulnerability scanning MUST run in CI pipelines; known critical/high vulnerabilities block merge

**Network Security (Deferred):**

- Private endpoints and public access restrictions are planned but NOT enforced in the initial deployment
- When activated, Azure resources MUST use private networking — all services (database, Key Vault, storage, AI services) accessible only via private endpoints within the virtual network
- When activated, public access MUST be disabled for internal-only resources unless explicitly approved as part of the application edge
- Activation of private endpoints will be tracked as a separate spec and constitutional amendment

### XI. Infrastructure, Deployment, and Operational Discipline

Infrastructure and deployment MUST be automated, reproducible, and reviewable.

- All Azure infrastructure MUST be defined using **Bicep** and versioned in the same repository as the application code
- Deployments MUST flow through approved automated pipelines; manual production deployments and portal-only infrastructure changes are prohibited
- Infrastructure changes MUST be reviewed like code
- Environments MUST be reproducible from shared infrastructure definitions, with environment-specific differences expressed through parameter or configuration artifacts rather than duplicated templates or ad hoc code paths
- Detailed repository layout, pipeline naming, validation commands, and rollout procedures belong in infrastructure specs, contracts, quickstarts, or operational runbooks

### XII. Testing and Specification Discipline

Test-first delivery is mandatory for application behavior that changes the platform.

- **Test-Driven Development (TDD)** is the default engineering workflow
- Tests MUST be written before implementation for new behavior whenever reasonably possible
- The Red → Green → Refactor cycle is the expected delivery model
- For feature delivery under the SDD workflow, the preferred artifact order is: contracts/interfaces → contract tests → integration tests → end-to-end scenarios → unit tests → implementation
- Integration tests are required for API endpoints and critical workflow boundaries
- Agent, orchestrator, and qualification logic MUST be independently testable
- Specs, architecture docs, and implementation MUST remain aligned
- No change is complete if behavior, tests, and documented intent materially diverge
- Every `tasks.md` MUST include a **Traceability Matrix** mapping each functional requirement (FR) from the spec to the task(s) that implement it
- All FRs MUST be covered by at least one task; uncovered FRs indicate an incomplete task breakdown
- The traceability matrix is the single source for FR-to-task mapping — individual task lines do not carry FR references

### XIII. Observability, Auditability, and Transparency

Operational transparency is a first-class requirement.

- All application telemetry MUST flow through **Azure Application Insights** or an approved centralized observability platform
- Logging MUST be structured
- Business-critical events MUST be instrumented, including prospect ingestion, validation, qualification, assignment, campaign actions, AI usage, and seller handoff
- Assignment and reassignment decisions MUST be explainable and auditable
- System health, performance, error rates, and job progress MUST be visible to operators
- Print-style debugging and opaque workflow transitions are prohibited in production code
- Material operational findings that expose requirement, workflow, or architectural gaps MUST feed back into specifications, plans, and test scenarios

### XIV. Simplicity and Change Discipline

The platform MUST be built for current business value, not speculative architecture.

- Build only what is needed for active requirements
- Do not introduce abstractions before repeated use cases justify them
- Favor correctness, readability, and maintainability over cleverness
- Prefer minimal safe changes over broad refactors without direct value
- Measure before optimizing
- Configuration should exist only where there is a genuine operational need
- Constitutional principles outrank convenience, expedience, and undocumented team habits

### XV. Schema Governance & Visual Documentation

Schema and architecture documentation MUST remain versioned, reviewable, and aligned with implementation.

- All database schema changes MUST go through versioned Alembic migration scripts
- No direct SQL execution against managed environments or ad hoc migration scripts outside the migrations directory
- Material entity, schema, architecture, and data-flow changes MUST be reflected in maintained visual documentation
- Diagram formats, file locations, and completion checklists belong in feature specs, data models, tasks, or workflow documentation rather than the constitution

### XVI. Environment Strategy & Resource Naming

Environment configuration, resource naming, and tagging MUST be consistent, documented, and reproducible.

- Shared infrastructure definitions MUST be reused across environments; environment-specific differences belong in parameter or configuration artifacts
- Azure resource names and tags MUST follow a single documented convention across the platform
- Concrete naming patterns, tag values, approved regions, and environment inventories belong in infrastructure specs, contracts, parameter files, or operational setup documentation

## Development Workflow

**Required SDD Artifact Chain:**

- Every feature change that materially affects behavior MUST maintain, at minimum, the following artifact chain unless explicitly exempted as trivial operational work:
  - `spec.md` — feature requirements, user stories, acceptance criteria, and open clarifications
  - `plan.md` — implementation plan and technical decision record
  - `tasks.md` — executable task breakdown with traceability matrix
- The following supporting artifacts SHOULD be created when relevant to the feature: `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, diagrams, and operational rollout notes
- The implementation plan MUST reference the constitution and identify any approved exceptions
- Main plan documents MUST stay high-level and readable; detailed mechanics belong in supporting artifacts
- Ambiguities MUST be resolved or explicitly marked before implementation of affected behavior proceeds

**Change Governance:**

- Material changes MUST remain traceable from approved specifications through plans, tasks, tests, code, and review
- Alternative implementation approaches MAY be explored in subordinate branches or documented variants, provided the shared parent specification remains authoritative and traceability is preserved
- Branch naming, commit granularity, and review automation rules belong in workflow and repository policy documents rather than the constitution

**Review Expectations:**

- All code changes MUST go through pull requests with review
- Pull requests MUST pass automated tests before merge
- Architecture, specs, migrations, infrastructure changes, and pipeline updates MUST be reviewed as rigorously as code
- No implementation is complete until code, tests, documentation, and operations guidance are aligned

## Governance

- This constitution defines the non-negotiable engineering and architectural boundaries for the Sales Prospecting Platform
- All contributors, including AI coding assistants, MUST comply with it
- Amendments require documented rationale, impact assessment, and review
- Implementation details such as specific model names, prompt text, concurrency values, source inventories, repository layout, pipeline commands, naming patterns, tag values, and branch conventions belong in specs and architecture documents unless they represent durable constitutional commitments
- Specs MUST NOT duplicate constitutional constraints — they reference the constitution and document only feature-specific decisions
- Constitutional compliance MUST be reviewed as part of every significant change
- Versioning follows semantic versioning:
  - **MAJOR**: a principle is removed or fundamentally redefined
  - **MINOR**: a new principle is added or an existing principle is materially expanded
  - **PATCH**: wording clarifications or non-semantic refinements

**Version**: 3.6.0  
**Ratified**: 2026-03-19  
**Last Amended**: 2026-04-13
