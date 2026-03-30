# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository context

This is the monorepo for **MFG Copilot**, a multi-agent management platform for NVIDIA manufacturing operations. It is currently in scaffold/foundation stage (Phase 0). No executable service code exists yet — the repo contains architecture docs, schemas, requirement stories, and project conventions.

## Key commands

```bash
# Validate requirement files (runs on every PR via GitHub Actions)
bash scripts/check-requirements.sh

# Validate progressive-disclosure doc navigation (runs on every PR via GitHub Actions)
bash scripts/check-progressive-disclosure.sh
```

No build, lint, or test commands exist yet. As services are added under `services/` and `apps/`, the following tooling has been chosen:
- **Backend tests**: `pytest` + FastAPI `TestClient` / `httpx.AsyncClient`
- **Integration tests**: `pytest` + `testcontainers-python`
- **API contract/fuzz**: Schemathesis (against FastAPI OpenAPI)
- **Browser E2E**: Playwright
- **Load tests**: k6 (scenarios go in `tests/load/`)
- **Agent evals**: DeepEval (scenarios go in `harness/evals/`)

## Architecture

The system routes manufacturing users through a layered stack:

```
Portal (React) → API Gateway (FastAPI) → Agent Router → Orchestrator (LangGraph)
                                                              ↓
                                          Doc Copilot / Deploy Agent / Ops Agent
                                                              ↓
                                    RAG Service (Milvus + ES) | Toolhub (MES/SFC/CMDB)
```

**Key service boundaries** (defined in `docs/architecture/solution-design.md`):
- `services/orchestrator/` owns all LangGraph execution, checkpoints, retries, HITL pauses, and approval gating. Agent services are stateless with respect to long-running workflow control.
- `services/rag-service/` is the **only** retrieval interface. Agents never call Milvus or Elasticsearch directly.
- `services/toolhub/` is the **only** enterprise integration surface. Agent code should not know whether data came from MySQL, a PostgreSQL mirror, or a search index.
- `services/api-gateway/` owns the approval API. Approval schema is defined in `packages/py/shared-schemas/approval-envelope.schema.yaml`.

See `docs/adr/0001-orchestrator-agent-boundary.md` for the orchestrator/agent split rationale.

## Database strategy

PostgreSQL is the platform system-of-record (users, sessions, approvals, audit, task ledger, LangGraph checkpoints). Enterprise MySQL systems are upstream read-only sources accessed only through `services/toolhub/`, optionally mirrored one-way into PostgreSQL via CDC. See `docs/adr/0002-platform-database-and-enterprise-sync.md`.

- `data/migrations/postgresql/` — real platform migrations (Alembic)
- `data/migrations/mysql/` — snapshots and reference docs only, **no platform migrations**
- `data/sync/` — CDC and mirroring assets

## Model routing

All task-class-to-model-profile routing is declared in `config/model-routing/task-routing.schema.yaml`. Services must not hardcode model vendor decisions. PII-restricted and export-controlled tasks must route to local SGLang profiles.

## Requirement management

Feature stories live in `tasks/features/REQ-xxx.md`. Phase contracts live in `tasks/phases/PHASE-NNN.md`. The script `scripts/check-requirements.sh` enforces:
- required frontmatter fields (`req_id`, `title`, `status`, `priority`, `phase`, `epic`, `owner`, `depends_on`, `scope`, `acceptance_summary`)
- enum values for `status`, `priority`, `scope`, `owner`
- required markdown sections (User Story, Goal, Deliverables, In Scope, Out of Scope, Acceptance Criteria, Validation Notes, Dependency Notes)
- bidirectional consistency between `tasks/features/` and `tasks/phases/` (feature_refs must match feature.phase)

Story template is in `harness/requirement-standard.md`. New stories start with `status: draft`. Architecture rationale belongs in `docs/adr/`, not in story files.

The repo follows progressive disclosure:
- start at `README.md`, `docs/README.md`, or `tasks/README.md`
- use index docs before opening deep design or individual `REQ-xxx` files
- avoid adding root-level doc lists that point directly to every deep architecture artifact

## Tests vs Harness

- `tests/` — service and application correctness (unit, integration, contract, E2E, load)
- `harness/` — agent behavior quality (DeepEval evals, golden dataset replay, scenario regression, harness/LangSmith run correlation)

If a test asserts software behavior of a service, it belongs in `tests/`. If it judges quality or regression of agent behavior over scenarios or datasets, it belongs in `harness/`.

## Trace correlation

Every critical workflow must carry: `task_id`, `workflow_id`, `agent_id`, `plan_id`, `approval_id`, `langsmith_run_id`. Harness runs must also carry `harness_run_id`. These are defined in `packages/py/shared-schemas/` and propagated from the orchestrator layer. Do not invent ad hoc trace fields in individual services.

## Agent patterns

Three patterns are defined in `docs/architecture/patterns/` and implemented in `packages/py/agent-patterns/`:
- **ReAct** — default for tool-using operational workflows (ops-agent, deploy-agent)
- **Markdown Planning** — for approval-facing workflows and auditable step-by-step state
- **Ralph Loop** — for higher-risk tasks needing generate/critique/revise cycles (RCA drafts, doc refinement)
