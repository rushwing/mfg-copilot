# ADR 0001: Orchestrator and Agent Service Boundary

## Status

Accepted

## Context

The platform includes an `orchestrator` service plus specialized agent services such as `doc-copilot`, `deploy-agent`, and `ops-agent`.

Without a written boundary, teams tend to mix workflow control with domain behavior:
- orchestration logic drifts into each agent
- agent-specific prompts and tools drift into the orchestrator
- approvals, retries, and human-in-the-loop behavior become inconsistent

This gets harder to unwind once multiple agents are active in production.

## Decision

Use the following split:

- `services/orchestrator/` owns execution control
- `services/agents/*` own domain-specific cognition and tool selection

### Orchestrator responsibilities

- host LangGraph execution runtime
- own task state machine and checkpoint persistence
- coordinate retries, timeouts, resumability, and cancellations
- enforce approval gates and human-in-the-loop transitions
- persist task ledger, execution metadata, and cross-agent handoff state
- attach trace metadata such as `task_id`, `plan_id`, `approval_id`, and `langsmith_run_id`

### Agent responsibilities

- define prompts, domain instructions, and sub-workflows
- choose domain tools from approved tool surfaces
- interpret retrieved context and produce outputs
- expose structured request and response contracts
- remain stateless with respect to long-running workflow control whenever possible

### Explicit non-goals

- agents do not persist their own long-running workflow state outside orchestrator-owned state stores
- orchestrator does not embed agent-specific prompt logic beyond wiring and policy controls

## Consequences

Benefits:
- approval, replay, retries, and audit behavior stay consistent
- domain teams can evolve agent logic without rewriting workflow runtime behavior
- harness and observability integrations attach cleanly at the orchestration layer

Costs:
- an extra contract boundary is required between orchestrator and agents
- some simple cases may feel slightly over-structured early on

## Follow-up

- keep agent request and response schemas under `packages/py/shared-schemas/`
- document approval and execution metadata in shared schemas before Phase 2 execution paths expand
- add gRPC contracts in `proto/` only if agent services become independently deployable and latency-sensitive

