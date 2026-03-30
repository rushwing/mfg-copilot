# Architecture Overview

This is the shortest useful description of the platform.

## What The System Is

MFG Copilot is a multi-agent manufacturing workspace with:
- a React portal for user interaction
- FastAPI services for gateway, orchestration, retrieval, and tools
- shared policy, trace, and schema contracts
- observability and eval layers for safe rollout

## Core Runtime Shape

1. The portal sends user requests through the API gateway.
2. The gateway resolves identity, context, and policy.
3. The orchestrator chooses the right agent workflow.
4. Retrieval and tool adapters provide grounded read or execution paths.
5. Trace, audit, eval, and approval layers make the workflow governable.

## Delivery Shape

- Phase 0 builds the platform baseline, contracts, retrieval, and policy foundations.
- Phase 1 delivers read-only manufacturing assistance and Doc Copilot workflows.
- Phase 2 adds approvals and controlled execution.
- Phase 3 expands into ops triage, RCA, and stronger governance loops.

## Read Next

- Need the repo layout: [Project Layout](./project-layout.md)
- Need phased delivery: [Phase Plan](./phase-plan.md)
- Need implementation detail: [Solution Design](./solution-design.md)
- Need the source architecture notes and diagram: [Architecture Index](./README.md)
