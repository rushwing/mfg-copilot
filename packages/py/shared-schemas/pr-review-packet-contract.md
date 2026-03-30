# PR Review Packet Contract

This document defines the repository-owned contract and artifact envelope for PR review packets.

Use it as the canonical companion to [`pr-review-packet.schema.yaml`](./pr-review-packet.schema.yaml).

## Purpose

- give packet generators one shared machine contract
- keep reviewer-facing prose separate from typed review metadata
- standardize artifact naming before workflow automation and merge gates depend on packet outputs

## Contract boundary

The packet contract covers:

- stable identifiers such as `schema_id`, `schema_version`, `packet_id`, and `pr_number`
- linked `REQ` and `ADR` references
- the minimum review sections required for downstream tooling
- repository-relative artifact paths for the machine packet, reviewer packet, and visuals directory
- workflow trace correlation fields that tie the packet back to `pr_packet_and_handoff`
- packet gating metadata for review readiness and merge readiness
- generation mode guidance for `direct_structured` and `draft_then_structure`

The contract does not define:

- the final reviewer-facing visual layout
- organization-wide GitHub merge policy outside this repository

Those follow-on concerns are layered through `REQ-019` and `REQ-020`.

## Required sections

Every packet must include these top-level sections:

- `summary`
- `validation`
- `risks`
- `reviewer_checklist`
- `visuals`
- `trace`
- `gating`

Within `summary`, `executive_summary` is the primary reviewer-facing prose field.

The remaining top-level sections should stay typed and machine-consumable so later generators, CI checks, and workflow tooling do not need to parse free-form markdown to understand packet completeness.

`trace` ties the packet back to workflow execution.

`gating` records whether the packet satisfies the repository gate baseline for review handoff.

## Artifact envelope

Runtime packet artifacts should use repository-relative paths under:

```text
artifacts/pr-review-packets/pr-<pr_number>/
```

Expected paths:

- machine packet JSON: `artifacts/pr-review-packets/pr-<pr_number>/review-packet.json`
- reviewer-facing markdown packet: `artifacts/pr-review-packets/pr-<pr_number>/review-packet.md`
- visuals directory: `artifacts/pr-review-packets/pr-<pr_number>/visuals/`

The schema stores these values under the `artifact` object so generators do not invent local path variants.

## Reference formats

Use these reference formats inside the packet:

- requirements: `REQ-018`
- ADRs: repository ADR file stem such as `0004-phase-based-orchestration-over-pure-react`

Do not use ad hoc labels like `adr-4`, `phase-graph-adr`, or free-text requirement names inside `linked_requirements` and `linked_adrs`.

## Generation mode guidance

Use `draft_then_structure` by default for PR review packets.

Reason:

- reviewer packets mix prose explanation with typed metadata
- forcing one-pass constrained output can reduce summary quality
- the machine contract still remains stable after the structuring pass

Use `direct_structured` only when a producer already has clean typed data and only needs a compact packet with minimal prose synthesis.

## Workflow integration

Packets are emitted in the `pr_packet_and_handoff` workflow phase.

Each packet must carry enough metadata to answer:

- which workflow run produced it
- which phase produced it
- whether the PR is review-ready
- whether the PR is merge-ready under the repository packet gate

The packet schema now carries:

- `trace.workflow_id`
- `trace.phase_id`
- `trace.branch_id`
- `trace.selected_branch_id`
- `trace.harness_run_id`
- `trace.langsmith_run_id`
- `gating.packet_policy_class`
- `gating.review_ready`
- `gating.merge_ready`
- `gating.required_visual`

For exempt PRs where no packet is required, the workflow should still emit a gate decision artifact using [`pr-review-packet-gate-decision.schema.yaml`](./pr-review-packet-gate-decision.schema.yaml).

## Example fixture

The canonical example fixture lives at:

- [`examples/pr-review-packet.example.json`](./examples/pr-review-packet.example.json)
- [`examples/pr-review-packet-gate-decision.full.example.json`](./examples/pr-review-packet-gate-decision.full.example.json)
- [`examples/pr-review-packet-gate-decision.exempt.example.json`](./examples/pr-review-packet-gate-decision.exempt.example.json)
- reviewer-facing layout guidance lives at [`docs/architecture/patterns/pr-review-packet-visual-language.md`](../../../docs/architecture/patterns/pr-review-packet-visual-language.md)
- workflow integration guidance lives at [`docs/architecture/patterns/pr-review-packet-workflow-integration.md`](../../../docs/architecture/patterns/pr-review-packet-workflow-integration.md)

That fixture exists to show:

- minimum required sections
- canonical artifact paths
- correct `REQ` and `ADR` reference formats
- the intended separation between reviewer prose and typed packet metadata
