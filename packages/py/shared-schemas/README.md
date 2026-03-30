# Shared Schemas

This package is the home for repository-wide Python schemas and contracts.

Early priority schemas:
- approval request and approval decision contracts
- orchestrator task envelopes
- agent request and response envelopes
- retrieval request and retrieval result contracts
- trace correlation metadata such as `task_id`, `approval_id`, `plan_id`, and `langsmith_run_id`

Schema-first rule:
- these schemas are the canonical contract layer for machine-consumed artifacts
- decoder choices such as provider-native structured outputs or Outlines must conform to these schemas
- raw human input should be normalized into these contracts after ingestion, not constrained at the UI boundary

Phase 1 recommendation:
- define the approval schema now, even if approval execution logic ships later

That keeps `services/api-gateway/`, `services/orchestrator/`, and frontend approval views aligned before Phase 2 expands execution flows.

Scaffolded contracts:
- `approval-envelope.schema.yaml`
- `retrieval-response.schema.yaml`
- `search-branch-record.schema.yaml`
- `pr-review-packet.schema.yaml`

Planned next contracts:
- orchestrator handoff envelopes
- agent request and response envelopes
- future A2A task payloads

Workflow rule:
- phase-based workflows should persist searchable-branch metadata through `search-branch-record.schema.yaml`
- the final `pr_packet_and_handoff` phase should emit `pr-review-packet.schema.yaml`
