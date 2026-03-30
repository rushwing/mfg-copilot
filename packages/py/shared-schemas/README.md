# Shared Schemas

This package is the home for repository-wide Python schemas and contracts.

Early priority schemas:
- approval request and approval decision contracts
- orchestrator task envelopes
- agent request and response envelopes
- retrieval request and retrieval result contracts
- trace correlation metadata such as `task_id`, `approval_id`, `plan_id`, and `langsmith_run_id`

Phase 1 recommendation:
- define the approval schema now, even if approval execution logic ships later

That keeps `services/api-gateway/`, `services/orchestrator/`, and frontend approval views aligned before Phase 2 expands execution flows.

Scaffolded contracts:
- `approval-envelope.schema.yaml`
- `retrieval-response.schema.yaml`

