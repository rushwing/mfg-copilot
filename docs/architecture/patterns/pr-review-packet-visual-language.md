# PR Review Packet Visual Language

This note defines the reviewer-facing information layout for PR review packets.

Use it together with:

- [`pr-review-packet.schema.yaml`](../../../packages/py/shared-schemas/pr-review-packet.schema.yaml)
- [`pr-review-packet-contract.md`](../../../packages/py/shared-schemas/pr-review-packet-contract.md)
- [`pr-review-packet-example.md`](./pr-review-packet-example.md)
- [`pr-review-packet-layout.svg`](../diagrams/pr-review-packet-layout.svg)

## Goal

Make packet outputs fast to review without forcing approvers to reconstruct intent from raw diffs, CI logs, or long natural-language summaries.

## Standard section order

Use this reviewer-facing section order:

1. `Executive Summary`
2. `Scope And References`
3. `Changed Areas`
4. `Validation Status`
5. `Risk Matrix`
6. `Reviewer Checklist`
7. `Architecture Or Control-Flow Visual`
8. `Optional Appendix`

This order is optimized for reviewer decision speed:

- what changed
- why it matters
- whether validation passed
- what still looks risky
- what the reviewer should explicitly confirm

## Mandatory vs optional content

| Section | Required | Preferred format | Notes |
| --- | --- | --- | --- |
| Executive Summary | yes | short prose | keep to one short paragraph or 3 bullets |
| Scope And References | yes | bullet list | include linked `REQ` and ADR stems |
| Changed Areas | yes | table | group by area, not by every file |
| Validation Status | yes | table | show pass/fail/skipped and evidence |
| Risk Matrix | yes | table | severity must be visually scannable |
| Reviewer Checklist | yes | checklist | keep concrete and decision-oriented |
| Architecture Or Control-Flow Visual | conditional | Mermaid or SVG | required when the PR changes workflow, routing, control flow, or service boundaries |
| Optional Appendix | no | bullets or links | use for traces, screenshots, or extra evidence |

## Table-first guidance

Prefer tables over prose for:

- changed areas
- validation status
- risk matrix
- compatibility or contract-change summaries

Prefer prose for:

- executive summary
- residual-risk explanation
- nuanced rollout notes that do not compress well into a table

Do not use long prose when a reviewer is mainly trying to compare categories, statuses, or risk levels.

## Table conventions

### Changed Areas table

Use columns:

- `Area`
- `Impact`
- `Primary files`

Rules:

- group related files under one area
- keep file lists short and selective
- describe impact in reviewer language, not implementation jargon

### Validation Status table

Use columns:

- `Check`
- `Status`
- `Evidence`

Rules:

- surface skipped checks explicitly
- point to the strongest evidence artifact, not every command output
- put failing or skipped items first when present

### Risk Matrix table

Use columns:

- `Category`
- `Severity`
- `Reviewer concern`
- `Mitigation`

Rules:

- severity should be one of `low`, `medium`, or `high`
- `Reviewer concern` should explain what could go wrong if the change is misunderstood or wrong
- `Mitigation` should say what reduces that risk now

## Visual guidance

At least one visual is required when the PR changes:

- architecture boundaries
- orchestration phase flow
- agent routing or handoff logic
- approval or control-flow checkpoints
- artifact generation or review gating behavior

Use `Mermaid` when:

- a simple flow or sequence diagram is enough
- the packet is generated quickly and readability matters more than polish

Use `SVG` when:

- the packet will be reused in review, docs, or handoff artifacts
- layout clarity needs more control than Mermaid provides
- a static diagram is part of the long-lived packet evidence

If a PR only changes narrow implementation details with no architecture or workflow impact, the packet may omit a visual and say why.

## Concision rules

- keep the executive summary under 120 words unless there is a compelling risk reason
- keep the reviewer checklist to 3-6 items
- avoid repeating the same point in summary, risks, and checklist
- appendices should hold extra evidence, not core decision content

## Example layout

The canonical reviewer-facing example is:

- [`pr-review-packet-example.md`](./pr-review-packet-example.md)

The visual section order reference is:

- [`pr-review-packet-layout.svg`](../diagrams/pr-review-packet-layout.svg)

Future packet generators should follow that example unless a later ADR or requirement explicitly changes the reviewer-facing packet layout.
