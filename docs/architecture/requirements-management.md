# Requirements Management

This repository should manage implementation-facing requirements as markdown files in Git, with code review through pull requests and without duplicating GitHub review state inside the repo.

It should also expose those requirements through progressive disclosure so readers and coding agents do not load the entire planning corpus at once.

## Recommended model

- high-level architecture and roadmap stay under `docs/architecture/`
- executable planning inputs live under `tasks/`
- GitHub remains the source of truth for PR review, comments, approvals, and merge state
- the repo remains the source of truth for requirement content, scope, acceptance criteria, and phase alignment

## Why this model

It combines two useful patterns:

- the `open-workhorse` repo-native `tasks/` model, where requirements are broken into small markdown work items with structured frontmatter
- community docs-as-code and RFC-style practices, where content lives in Git, is reviewed by PR, and is validated like code

## Design principles

### 0. Progressive disclosure first

- root docs should point to index docs, not to every detailed planning artifact
- `tasks/README.md` should route readers to phase and feature indexes before individual stories
- detailed design should be loaded only when a story or review actually needs it
- requirement files should stay implementation-focused and avoid re-explaining whole-system architecture

### 1. Single source of truth for requirement content

- if a feature must be implemented, its scope and acceptance criteria should exist in this repo
- critical acceptance details should not live only in chat, tickets, or meeting notes

### 2. Structured markdown over free-form backlog prose

- each feature story should be a small, reviewable markdown file
- metadata should be in frontmatter so future automation and validation stay possible

### 3. Repo content, GitHub workflow

- requirement content belongs in the repo
- review state, reviewer assignment, PR discussion, and merge status belong in GitHub
- do not maintain a second parallel review state machine in markdown unless automation truly requires it

### 4. Phase-first decomposition

- phase docs define boundaries, entry conditions, and exit criteria
- feature stories point back to phases and dependencies
- this keeps backlog growth from drifting outside the active roadmap

### 5. Tests and evals stay linked, not duplicated

- software correctness belongs in `tests/`
- agent quality and regression belong in `harness/`
- feature stories should name the expected validation strategy, but not duplicate test implementation details

## Directory model

```text
tasks/
  README.md               # tasks entry point
  phases/                # phase contracts and scope boundaries
    README.md            # phase index
  features/              # feature stories (REQ-xxx)
    README.md            # feature index
  archive/
    done/
    cancelled/
```

Later, if needed:

```text
tasks/
  test-cases/            # optional explicit TC docs
  bugs/                  # optional repo-native long-lived bugs
```

## Calibration and CI

- requirement files should be machine-checked, not only reviewed by eye
- this repo uses `bash scripts/check-requirements.sh` to validate `tasks/phases/` and `tasks/features/`
- GitHub Actions should run the script on pull requests and pushes to `main`

## What we are intentionally not copying from open-workhorse

`open-workhorse` has a richer multi-agent workflow with claim and routing states such as `review_ready`, `req_review`, and `test_designed`.

For this repo, the recommended starting point is lighter:

- keep the markdown requirement shape
- keep phase docs and frontmatter metadata
- keep the small-work-item discipline
- do not adopt the full multi-agent requirement state machine yet

That avoids premature process complexity while preserving the most valuable part: a stable in-repo source of requirement truth.

## References

- [Write the Docs: Docs as Code](https://www.writethedocs.org/guide/docs-as-code.html)
- [Write the Docs: Documentation principles](https://www.writethedocs.org/guide/writing/docs-principles.html)
- [Doctave: Docs as code](https://www.doctave.com/docs-as-code)
- RFC-style change proposals are widely used in repo-centric engineering communities, for example [Rust RFCs](https://github.com/rust-lang/rfcs)
