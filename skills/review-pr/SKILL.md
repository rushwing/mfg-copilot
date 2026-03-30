---
name: review-pr
description: "Full PR review workflow for the mfg-copilot repository. Fetches PR metadata and diff via gh, checks out the branch, runs all repo validators, cross-checks linked REQ files, and produces a structured reviewer-facing packet with a clear verdict. Trigger when the user says: 'Review PR10', 'Review PR #N', '/review-pr N', or 'review the PR' (when a PR number is in context). Do NOT trigger for general code review questions unrelated to a numbered PR."
---

# PR Review Workflow

## Step 1 — Fetch PR metadata and diff

```bash
gh pr view <N> --json title,body,headRefName,baseRefName,files,commits,state,author,url
gh pr diff <N>
```

Note `headRefName` and the `files` list before proceeding.

## Step 2 — Checkout and run all validators

```bash
git fetch origin <headRefName> && git checkout <headRefName>
```

Run every validator that exists in `scripts/` — skip silently if the file is absent:

```bash
bash scripts/check-requirements.sh
bash scripts/check-progressive-disclosure.sh
bash scripts/check-pr-review-packet-layout.sh
python3 scripts/check-pr-review-packet-contract.py
python3 scripts/check-pr-review-packet-gating.py
```

Record pass / fail / warning count for each. A check is "skipped" only when the script file
does not exist yet — not when it errors.

## Step 3 — Read key changed files

Read a file when the diff alone is insufficient:

| File type | What to check |
| --- | --- |
| New `.schema.yaml` | `additionalProperties: false` present, `required` list complete, enum coverage |
| New `scripts/check-*.py` / `*.sh` | Hardcoded strings that couple docs to the script (fragile cross-refs) |
| Changed `tasks/features/REQ-*.md` | Valid status/workflow_phase transition, owner not unassigned when in_progress or review |
| New contract / pattern docs | Cross-reference completeness, link targets exist |

Skip files whose diff is fully self-explanatory.

## Step 4 — Cross-check linked REQs

For each REQ referenced in the PR description or changed files:

1. `status` and `workflow_phase` transition is valid (see `harness/requirement-standard.md §4`)
2. `owner != unassigned` when `status` is `in_progress` or `review`
3. All `depends_on` predecessors exist in `tasks/features/`

## Step 5 — Produce the review packet

Load `references/packet-sections.md` for table column schemas, mandatory vs optional rules,
and concision limits, then output the packet.

**Verdict line comes first:**

```
**Verdict: Approve** | **Verdict: Request Changes**
```

Use **Request Changes** only when:
- a validator fails or exits non-zero
- a required schema field is missing
- a REQ transition is invalid
- a mandatory packet section is absent

Observations that need no action before merge go under the relevant section as plain notes,
not as blockers.
