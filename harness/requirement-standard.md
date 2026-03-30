---
harness_id: REQ-STD-001
component: requirements / planning
owner: Engineering
version: 0.1
status: draft
last_reviewed: 2026-03-30
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
- it validates frontmatter completeness, enum values, required sections, and phase/story cross-references
- the script should run in GitHub Actions so malformed stories do not silently enter the main branch
- `bash scripts/check-progressive-disclosure.sh` should validate the required navigation hubs and keep root entry points from linking directly to too many deep docs
