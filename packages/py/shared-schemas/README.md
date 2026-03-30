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
- `pr-review-packet.schema.yaml`
- `retrieval-response.schema.yaml`
- `search-branch-record.schema.yaml`

Packet contract guidance:
- [`pr-review-packet-contract.md`](./pr-review-packet-contract.md)
- [`examples/pr-review-packet.example.json`](./examples/pr-review-packet.example.json)

The PR review packet contract standardizes:
- stable packet identifiers and schema versioning
- repository-relative artifact paths under `artifacts/pr-review-packets/pr-<pr_number>/`
- canonical `REQ` and ADR reference formats
- the split between reviewer-facing prose and typed machine-consumed sections
