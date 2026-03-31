---
harness_id: REQ-STD-001
component: requirements / planning
owner: Engineering
version: 0.2
status: draft
last_reviewed: 2026-03-31
---

# Harness Standard — Requirement and Feature Story Management

This standard defines how implementation-facing requirements are managed inside this repository.

## 1. Purpose

- keep requirement content in one authoritative place inside the repo
- make feature scope executable by engineers and coding agents
- align phases, stories, and acceptance criteria without depending on chat history

## 2. Core rules

### 2.0 Documentation must use progressive disclosure

- root and directory `README.md` files should act as navigation hubs
- summary docs should route readers to the next layer instead of duplicating deep content
- detailed architecture belongs in dedicated docs, not repeated inside every story
- feature stories should stay narrowly implementation-facing
- repository-wide terms should prefer the definitions in `docs/GLOSSARY.md` once a term is standardized there

### 2.1 The repo is the source of truth for requirement content

- feature scope, acceptance criteria, dependencies, and phase alignment must live in the repo
- external systems may mirror or discuss the work, but should not be the only place where core requirement content exists

### 2.2 GitHub is the source of truth for collaboration state

- PR review state, reviewers, comments, approvals, and merge status live in GitHub
- do not duplicate those workflow states inside story files unless a later automation layer truly requires it

### 2.3 Stories must be small and reviewable

- one story should describe one shippable or clearly bounded deliverable
- stories should be small enough that acceptance can be judged without reopening the entire phase plan

### 2.4 Story files must be structured

Each feature story must include:
- stable ID
- title
- status
- workflow phase
- priority
- phase
- epic
- owner
- dependencies
- scope
- acceptance summary
- concrete deliverables
- validation approach

## 3. Directory structure

```text
tasks/
  README.md                # task-system entry point
  phases/                 # phase contracts
    README.md             # phase index
  features/               # REQ-xxx feature stories
    README.md             # feature index
  archive/
    done/
    cancelled/
```

## 4. Status values

This repository uses a two-layer model:

- `status` expresses story lifecycle
- `workflow_phase` expresses the current execution node inside the long-running engineering workflow

They are related, but they are not the same field and should not be collapsed into one overloaded state machine.

Allowed values:
- `draft`
- `ready`
- `in_progress`
- `blocked`
- `review`
- `done`
- `cancelled`

Starting rule:
- new stories begin as `draft`
- move to `ready` after requirement review
- use GitHub PRs for implementation review once work begins

## 4.1 Workflow phase values

Allowed values:
- `requirement_assessment`
- `test_design`
- `implementation`
- `review_and_repair`
- `pr_packet_and_handoff`

Default engineering workflow:
1. `requirement_assessment`
2. `test_design`
3. `implementation`
4. `review_and_repair`
5. `pr_packet_and_handoff`

For small or low-risk stories, `test_design` may be folded into `requirement_assessment` instead of being persisted as a separate workflow boundary.

## 4.2 Recommended mapping between status and workflow_phase

- `draft` usually maps to `requirement_assessment`
- `ready` usually means `requirement_assessment` is complete and the story is ready to enter `test_design` or, for folded small stories, move directly toward `implementation`
- `in_progress` may occur in `test_design`, `implementation`, `review_and_repair`, or `pr_packet_and_handoff`
- `blocked` may occur in any workflow phase
- `review` usually maps to `pr_packet_and_handoff`, where reviewer-facing artifacts and handoff checks are being finalized
- `done` indicates the workflow has reached a terminal successful outcome
- `cancelled` indicates the workflow has reached a terminal abandoned outcome

These mappings are intentionally coarse. `status` is for story lifecycle visibility; `workflow_phase` is for execution-state visibility.

## 5. Phase documents

Each phase doc should define:
- goal
- in-scope items
- out-of-scope items
- exit criteria
- in-scope feature story references

## 6. Feature story template

```md
---
req_id: REQ-001
title: Example story
status: draft
workflow_phase: requirement_assessment
priority: P1
phase: phase-1
epic: example-epic
owner: unassigned
depends_on: []
scope: runtime
acceptance_summary: Example acceptance summary
---

# User Story

# Goal

# Deliverables

# In Scope

# Out of Scope

# Acceptance Criteria

# Validation Notes

# Dependency Notes
```

## 6.1 Definition of Ready

A story is review-ready for status promotion to `ready` when:

- scope is narrow enough to fit one bounded implementation PR or one tightly related PR stack
- dependencies reference concrete `REQ-xxx` items rather than vague external work
- acceptance criteria are specific and testable
- deliverables identify the expected user-visible or system-visible outputs
- validation notes say whether correctness belongs primarily in `tests/`, `harness/`, or both
- major open design questions are already resolved or explicitly moved to predecessor stories
- `workflow_phase` reflects the current execution node instead of trying to encode execution progress in `status` alone

This repository may keep a story in `draft` while the content is already written to this standard, if human review is still pending.

## 7. Scope values

Allowed values:
- `runtime`
- `ui`
- `data`
- `infra`
- `observability`
- `docs`
- `harness`

## 8. Relationship to tests and evals

- `tests/` validates software correctness
- `harness/` validates agent behavior and regression quality
- story files should reference expected validation approach, but not duplicate the full test implementation

## 8.1 Relationship to architecture docs

- phase and feature files should link to architecture rationale rather than copy large design sections
- architecture indexes should route to stories, not restate their acceptance criteria in full
- if a requirement needs more than story-sized explanation, add a dedicated design doc and link it

## 9. Calibration

- `bash scripts/check-requirements.sh` is the repo-native calibration script for requirement files
- it validates frontmatter completeness, enum values, required sections, phase/story cross-references, and `workflow_phase` values
- the script should run in GitHub Actions so malformed stories do not silently enter the main branch
- `bash scripts/check-progressive-disclosure.sh` should validate the required navigation hubs and keep root entry points from linking directly to too many deep docs
- `requirements-merge-gate` should validate that PR-linked requirements are merge-eligible before protected-branch merge
- PRs should declare linked requirements in a dedicated `Linked requirements` or `Requirements` section instead of relying on incidental `REQ-xxx` mentions elsewhere in the body
- the merge gate may auto-close a linked requirement from `review` to `done` only when `workflow_phase` is already `pr_packet_and_handoff`
