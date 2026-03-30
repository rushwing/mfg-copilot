# Project Layout

This repository is laid out as a product monorepo with clear service boundaries. It is optimized for a multi-agent management platform using React, FastAPI, LangGraph, LangSmith, Milvus, Elasticsearch, PostgreSQL, MySQL, Docker, Kubernetes, and Prometheus.

## Guiding choices

- Start as a modular monorepo, not a premature microservice mesh.
- Keep north-south traffic on FastAPI.
- Introduce gRPC only for east-west service contracts that need independent scaling or language-neutral interfaces.
- Treat PostgreSQL as the primary platform system-of-record.
- Use MySQL for manufacturing or enterprise data synchronization when upstream systems already standardize on MySQL.
- Keep vector, search, traces, logs, and metrics in dedicated systems instead of overloading the primary relational store.
- Make Harness Engineering a first-class top-level concern so agent behavior can be replayed, evaluated, and regression-tested.

## Recommended tree

```text
mfg-copilot/
├── apps/
│   └── portal-web/                  # React.js + Tailwind CSS operator and user portal
├── services/
│   ├── api-gateway/                 # FastAPI north-south API, auth, session, approval inbox
│   ├── agent-router/                # intent routing, policy routing, tenant and role resolution
│   ├── orchestrator/                # LangGraph runtime host, state machine, HITL, task execution
│   ├── rag-service/                 # retrieval, reranking, citation building, vector and search access
│   ├── toolhub/                     # MES/SFC/CMDB/ticketing/Git adapters
│   └── agents/
│       ├── doc-copilot/             # document generation and checkpoint preparation
│       ├── deploy-agent/            # deployment planning, approvals, execution
│       └── ops-agent/               # triage, diagnostics, RCA, FA assist
├── packages/
│   ├── py/
│   │   ├── agent-core/              # shared agent runtime primitives
│   │   ├── agent-patterns/          # ReAct, Markdown Planning, Ralph Loop implementations
│   │   ├── rag-core/                # retrieval abstractions and index clients
│   │   ├── toolkits/                # shared tool wrappers and integration clients
│   │   └── shared-schemas/          # Pydantic models, DTOs, policy schemas
│   └── ts/
│       ├── api-client/              # typed frontend API client
│       ├── shared-config/           # Tailwind, lint, env, shared frontend config
│       └── ui/                      # reusable React UI primitives
├── proto/                           # gRPC contracts for optional internal service boundaries
├── docs/
│   ├── architecture/
│   ├── adr/
│   └── runbooks/
├── harness/
│   ├── scenarios/                   # end-to-end harness definitions
│   ├── evals/                       # agent eval suites and golden expectations
│   ├── datasets/                    # replayable prompt / tool / workflow fixtures
│   ├── fixtures/                    # synthetic service responses and stub data
│   ├── runners/                     # harness executors
│   └── reports/                     # eval outputs and benchmark snapshots
├── observability/
│   ├── prometheus/                  # metrics scrape and alert rules
│   ├── langsmith/                   # tracing, run metadata, prompt lineage
│   └── elasticsearch/               # operational search and log indexing
├── infra/
│   ├── docker/                      # local container builds
│   └── k8s/
│       ├── base/
│       └── overlays/
│           ├── dev/
│           ├── staging/
│           └── prod/
├── config/
│   ├── env/                         # env templates
│   ├── model-routing/               # SGLang vs remote model routing rules
│   └── policies/                    # safety, approval, export, and execution policies
├── data/
│   ├── migrations/
│   │   ├── postgresql/              # platform and orchestration state schema
│   │   └── mysql/                   # mirrored manufacturing / ERP schema adapters
│   └── seeds/
├── scripts/                         # bootstrap, dev, lint, test, release helpers
└── tests/
    ├── unit/
    ├── integration/
    ├── contract/
    ├── e2e/
    └── load/
```

## How the stack maps into the layout

### Frontend

- `apps/portal-web/` is the single React.js + Tailwind CSS entry point for operators, approvers, and end users.
- `packages/ts/ui/` holds reusable components so the app does not become a giant uncontrolled frontend.
- `packages/ts/api-client/` keeps transport logic out of page code.

### Backend

- `services/api-gateway/` owns REST APIs, auth/session handling, request validation, and user-facing aggregation.
- `services/agent-router/` owns routing logic and policy-aware agent selection.
- `services/orchestrator/` owns LangGraph execution, checkpoints, retries, task state, and human-in-the-loop.
- `services/rag-service/` centralizes Milvus and Elasticsearch access instead of duplicating retrieval code in every agent.
- `services/toolhub/` isolates MES, SFC, CMDB, distribution, observability, and ticket-system adapters.

### AI and agent patterns

- `packages/py/agent-patterns/` is where reusable execution patterns live.
- `docs/architecture/patterns/` keeps the architecture-facing explanation of those patterns.
- Recommended default:
  - ReAct for tool-using operational workflows
  - Markdown Planning for plan visibility, approvals, and step traceability
  - Ralph Loop for iterative critique-revise execution around higher-risk tasks

### Data and storage

- PostgreSQL: platform metadata, users, sessions, approvals, audit, LangGraph state, task ledger.
- MySQL: mirrored factory or enterprise operational data when upstream systems already use MySQL.
- Milvus: vector search, semantic memory, long-context retrieval.
- Elasticsearch: log search, issue correlation, searchable operational knowledge.

### Delivery and runtime

- `infra/docker/` supports local development and reproducible packaging.
- `infra/k8s/` uses a base plus environment overlays so deployment intent stays explicit.
- `observability/prometheus/` tracks metrics and SLO-facing alerts.
- `observability/langsmith/` tracks traces, prompts, runs, and eval-linked debugging.

### Harness Engineering

- `harness/` is intentionally a top-level peer of app code.
- All critical agent flows should be backed by harness scenarios, eval datasets, and replayable reports.
- This keeps regressions visible before production rollout and aligns well with agentic workflows.

## Placement of the existing docs

- `docs/architecture/system-architecture.md`
- `docs/architecture/diagrams/system-architecture.svg`

These are the right long-term locations for the current architecture source and diagram because they can evolve with the implementation without crowding the repository root.
