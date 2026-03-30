# Solution Design

This document translates the current architecture into a concrete implementation design aligned to the planned phases.

## Design goals

- deliver business value early with read-only, grounded workflows
- keep service boundaries clear without overcommitting to heavy microservices too soon
- make approvals, traces, and evals first-class from the beginning
- isolate enterprise integrations behind stable internal contracts

## System topology by responsibility

### User-facing layer

- `apps/portal-web`
  - React and Tailwind portal
  - chat, forms, approval inbox, history, and reporting views

- `services/api-gateway`
  - FastAPI north-south boundary
  - auth/session handling
  - approval APIs
  - task submission and result retrieval APIs

### Control layer

- `services/agent-router`
  - intent classification
  - role and policy aware route selection
  - task-class assignment for model routing

- `services/orchestrator`
  - LangGraph runtime host
  - checkpointing, retries, and state transitions
  - human-in-loop pauses and approval gating
  - trace metadata propagation

### Agent layer

- `services/agents/doc-copilot`
  - documentation workflows
  - template completion and schema validation

- `services/agents/deploy-agent`
  - deployment planning
  - pre-checks and execution orchestration requests

- `services/agents/ops-agent`
  - triage, diagnostics, and RCA support

### Platform services

- `services/rag-service`
  - single retrieval interface
  - Milvus + Elasticsearch fusion
  - reranking and citation assembly

- `services/toolhub`
  - MES, SFC, software distribution, CMDB, observability, ticketing, and Git adapters
  - read / execute boundary enforcement at integration points

## Recommended deployment shape by phase

### Phase 1 deployment shape

Deployables:
- portal-web
- api-gateway
- agent-router
- orchestrator
- doc-copilot
- rag-service
- toolhub with read-only adapters
- PostgreSQL
- Milvus
- Elasticsearch

Rationale:
- keeps the main workflow observable and modular
- allows read-only value without operational execution risk

### Phase 2 deployment shape

Add:
- deploy-agent
- approval inbox activation
- execute-capable toolhub adapters for approved environments

### Phase 3 deployment shape

Add:
- ops-agent
- stronger observability pipelines
- optional coding or remediation helper paths behind policy controls

## Core bounded contexts

### 1. Identity and session context

Owned by:
- `api-gateway`

Key data:
- user identity
- roles
- site and station context
- session metadata

### 2. Task orchestration

Owned by:
- `orchestrator`

Key data:
- task envelope
- task state
- checkpoint state
- retry history
- approval dependencies

### 3. Approval and audit

Owned by:
- `api-gateway` for north-south API
- `orchestrator` for enforced workflow transitions

Key data:
- approval request
- approval decision
- audit trail
- execution ledger

### 4. Retrieval and knowledge

Owned by:
- `rag-service`

Key data:
- retrieval request
- retrieval response
- citations
- KB release metadata

### 5. Enterprise integration

Owned by:
- `toolhub`

Key data:
- adapter request and response payloads
- integration-specific audit entries
- mirrored data access mappings

## Key schemas to stabilize early

- task envelope
- approval envelope
- retrieval request and response
- plan summary and execution plan
- trace correlation envelope

Early stabilization matters because these contracts connect portal, gateway, orchestrator, agents, harness, and observability.

## Data architecture

### PostgreSQL

Use for:
- users, sessions, roles
- task ledger and orchestration checkpoints
- approvals and audit trail
- platform-owned reporting metadata

### MySQL

Use as:
- upstream enterprise source where necessary

Access pattern:
- through `toolhub`
- optionally mirrored by one-way sync into platform-readable stores

### Milvus

Use for:
- semantic search over KB and selected contextual corpora

### Elasticsearch

Use for:
- operational log search
- issue and history search
- hybrid retrieval alongside Milvus

## Main workflow designs

### Document Copilot workflow

1. User submits question or draft request through portal
2. Gateway resolves identity and context
3. Router classifies request as doc workflow
4. Orchestrator starts doc-copilot workflow with trace metadata
5. Doc-copilot requests normalized retrieval from rag-service
6. RAG response returns fused, reranked evidence with citations
7. Doc-copilot generates structured output and validates against template requirements
8. Gateway returns final output, citations, and any gap report

### Deployment workflow

1. User requests deployment planning for a site and station scope
2. Gateway and router assign deploy workflow
3. Orchestrator builds a deployment task with approval-ready metadata
4. Deploy-agent gathers context and toolhub pre-check data
5. Deploy-agent produces plan, risks, and evidence
6. Gateway persists approval request
7. After approval, orchestrator transitions task state to executable
8. Toolhub runs approved actions and returns evidence
9. Orchestrator persists execution ledger and final result package

### Ops triage workflow

1. User or alert creates issue context
2. Router assigns ops workflow
3. Orchestrator invokes ops-agent with task and policy metadata
4. Ops-agent queries toolhub and rag-service for logs, metrics, build history, and known issues
5. Agent generates triage summary, likely causes, and next actions
6. Gateway returns reviewable summary and escalation options

## Model routing design

- task classes are defined in `config/model-routing/task-routing.schema.yaml`
- router or orchestrator resolves task class before agent execution
- final model profile selection should be policy-driven, not agent-specific hardcoding
- export-controlled or PII-restricted tasks must prefer approved local profiles

## Approval design

- approval objects are created through shared schemas in Phase 1
- approval gating becomes active in Phase 2
- all execution tasks should carry:
  - `task_id`
  - `plan_id`
  - `approval_id`
  - `agent_id`
  - `langsmith_run_id`

## Harness and eval design

- `tests/` validates software correctness
- `harness/` validates agent behavior and regression quality
- every critical workflow should have:
  - happy-path harness scenario
  - adversarial or edge-case dataset
  - trace correlation with LangSmith

## Implementation strategy by phase

### Phase 1 design priorities

- make doc copilot excellent before widening scope
- prefer read-only adapters and stable retrieval quality over broad feature count
- build portal history, citations, and summaries so users trust outputs

### Phase 2 design priorities

- invest in approval UX and execution ledger clarity
- keep execution surface narrow and explicitly whitelisted
- harden idempotency, retries, and evidence capture before widening rollout

### Phase 3 design priorities

- improve data quality and search breadth for triage
- expand observability and guardrails before adding remediation autonomy
- gate bug-fix or code-generating workflows behind explicit policy

## Open design questions to resolve next

- final SSO provider and role-mapping source
- exact approval ownership model by organization and site
- KB ingestion workflow and release cadence
- first station families and environments to support in Phase 2
- operational data sources available for Phase 3 triage

