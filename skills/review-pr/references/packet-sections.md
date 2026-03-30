# PR Review Packet — Sections Reference

## Standard section order

1. **Executive Summary** — short prose, ≤120 words, one paragraph or ≤3 bullets
2. **Scope And References** — bullet list: linked REQ IDs, ADR stems, workflow phase
3. **Changed Areas** — table (columns: Area / Impact / Primary files); group by area not by file
4. **Validation Status** — table (columns: Check / Status / Evidence); put failures first
5. **Risk Matrix** — table (columns: Category / Severity / Reviewer concern / Mitigation)
6. **Reviewer Checklist** — 3–6 concrete checklist items, decision-oriented not descriptive
7. **Architecture Or Control-Flow Visual** — Mermaid or SVG; see visual rule below
8. **Optional Appendix** — extra traces, screenshots, or links; never core decision content

## Mandatory vs optional

| Section | Required |
| --- | --- |
| Executive Summary | yes |
| Scope And References | yes |
| Changed Areas | yes |
| Validation Status | yes |
| Risk Matrix | yes |
| Reviewer Checklist | yes |
| Architecture Or Control-Flow Visual | conditional — required when the PR changes workflow, routing, control flow, service boundaries, or artifact generation |
| Optional Appendix | no |

## Table column schemas

### Changed Areas
`Area` / `Impact` / `Primary files`
- Group related files under one area label
- Impact in reviewer language, not implementation jargon

### Validation Status
`Check` / `Status` / `Evidence`
- Status values: `passed` / `failed` / `skipped`
- Surface skipped checks explicitly; put failures and skipped first

### Risk Matrix
`Category` / `Severity` / `Reviewer concern` / `Mitigation`
- Severity: `low` / `medium` / `high` only
- Reviewer concern: what could go wrong if the change is wrong or misunderstood
- Mitigation: what reduces that risk now

## Concision rules

- Executive summary ≤120 words
- Reviewer checklist 3–6 items
- Do not repeat the same point across summary, risks, and checklist
- Appendix holds extra evidence, not core decisions
