# PR Review Packet Workflow Integration

This note defines how PR review packets participate in the engineering phase graph and how packet completeness affects review handoff and merge readiness.

Use it together with:

- [`pr-review-packet-contract.md`](../../../packages/py/shared-schemas/pr-review-packet-contract.md)
- [`pr-review-packet-visual-language.md`](./pr-review-packet-visual-language.md)
- [`pr-review-packet-gate-decision.schema.yaml`](../../../packages/py/shared-schemas/pr-review-packet-gate-decision.schema.yaml)

## Phase placement

Packet generation belongs in `pr_packet_and_handoff`.

That phase is where the workflow must:

- finalize the packet artifact
- evaluate packet completeness
- record a gate decision
- prepare reviewer-facing handoff

It is not the phase where implementation or repair should continue indefinitely.

## Packet policy classes

| Policy class | Use when | Packet required | Visual required | Gate artifact required |
| --- | --- | --- | --- | --- |
| `full_packet_required` | workflow, routing, architecture, control-flow, contract, security, approval, or execution behavior changed | yes | yes when visual guidance says required | yes |
| `simplified_packet_allowed` | low-risk implementation changes with no architecture or workflow impact | yes | no by default | yes |
| `packet_exempt` | docs-only, comment-only, formatting-only, or dependency metadata-only PRs | no | no | yes |

`packet_exempt` is intentionally narrow.

If there is any uncertainty about whether a change alters workflow, architecture, or reviewer risk, prefer `full_packet_required` or `simplified_packet_allowed`.

## Review-ready vs merge-ready rules

### Review-ready

A PR is review-ready when:

- a packet exists for `full_packet_required` and `simplified_packet_allowed` classes
- the packet is schema-valid
- the reviewer checklist is present
- the gate decision artifact exists
- exempt PRs record a valid exemption reason instead of silently skipping packet generation

### Merge-ready

A PR is merge-ready when:

- it is already review-ready
- required validation checks passed or were explicitly accepted as skipped
- a required visual exists for `full_packet_required` changes
- the gate decision marks `merge_ready: true`

This repository treats merge readiness as stricter than review readiness.

## Exemption path

Allowed exemption reasons:

- `docs_only`
- `comment_only`
- `formatting_only`
- `dependency_metadata_only`

Exempt PRs must still emit a gate decision artifact under:

```text
artifacts/pr-review-packets/pr-<pr_number>/gate-decision.json
```

The exemption path is invalid if:

- the reason is missing
- the PR actually changes workflow or architecture behavior
- the exemption is inferred informally instead of recorded as a workflow decision

## Trace correlation

Every packet-backed or exempt decision must be trace-linked.

Required correlation fields:

- `workflow_id`
- `phase_id`
- `branch_id`
- `selected_branch_id`
- `harness_run_id`
- `langsmith_run_id`

This lets reviewers and future debugging tools jump from:

- packet or gate decision
- to workflow execution
- to harness report
- to LangSmith trace

without reconstructing the run from PR comments alone.

## Required artifacts by policy class

| Policy class | Required artifacts |
| --- | --- |
| `full_packet_required` | machine packet JSON, reviewer packet markdown, gate decision, visuals directory |
| `simplified_packet_allowed` | machine packet JSON, reviewer packet markdown, gate decision |
| `packet_exempt` | gate decision only |

## Workflow examples

### Full packet path

1. `review_and_repair` finishes with residual-risk notes and validation evidence.
2. `pr_packet_and_handoff` drafts and structures the packet.
3. The workflow evaluates whether a visual is required.
4. The workflow emits both:
   - `review-packet.json`
   - `gate-decision.json`
5. The PR becomes review-ready and, if checks are complete, merge-ready.

Reference example:

- [`pr-review-packet-gate-decision.full.example.json`](../../../packages/py/shared-schemas/examples/pr-review-packet-gate-decision.full.example.json)

### Exempt path

1. `pr_packet_and_handoff` classifies the PR as `packet_exempt`.
2. The workflow records a valid exemption reason.
3. No packet markdown or packet JSON is required.
4. The workflow still emits `gate-decision.json`.
5. Reviewers can see why the packet was omitted and how to trace the decision.

Reference example:

- [`pr-review-packet-gate-decision.exempt.example.json`](../../../packages/py/shared-schemas/examples/pr-review-packet-gate-decision.exempt.example.json)
