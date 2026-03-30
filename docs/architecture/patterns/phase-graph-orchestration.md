# Phase Graph Orchestration

Use phase graphs for long-running workflows.

Use search trees only inside the parts of a workflow that genuinely need alternative-path exploration.

## Core rule

- phase graph is the platform truth
- searchable subtrees are local problem-solving tools
- ReAct runs inside one branch
- Reflexion repairs or redirects failed branches

## Default engineering workflow

```mermaid
flowchart LR
  A["requirement_assessment"] --> B["test_design"]
  B --> C["implementation"]
  C --> D["review_and_repair"]
  D --> E["pr_packet_and_handoff"]
```

For small or low-risk stories, `test_design` may be folded into `requirement_assessment` rather than persisted as its own phase node.

## Phase responsibilities

### requirement_assessment

- read requirement, ADR, and local code context
- surface open risks and missing assumptions
- decide whether the story is ready to enter implementation flow

### test_design

- define validation strategy
- draft test cases or eval scenarios
- identify contract, integration, and edge-case coverage

### implementation

- make code or config changes
- collect artifacts and evidence
- use local ReAct loops for tool use and incremental progress

### review_and_repair

- inspect diff, tests, traces, and risk areas
- run bounded repair loops if issues are found
- produce residual-risk notes when work is not fully clean

### pr_packet_and_handoff

- generate the PR review packet
- emit the packet gate decision
- attach validation evidence and reviewer checklist
- prepare handoff artifacts for HITL review

## Searchable phases

Not every phase should branch.

Recommended searchable phases:
- `test_design`
- `implementation`
- `review_and_repair`

Usually non-searchable:
- `requirement_assessment`
- `pr_packet_and_handoff`

## Search strategy

Default strategy:
- best-first or beam search

Fallback strategy:
- limited backtracking when the current branch clearly fails

Avoid:
- unconstrained DFS over the whole workflow
- open-ended branch spawning without budgets

## Branch record

Each branch should capture:
- `branch_id`
- `parent_branch_id`
- `hypothesis`
- `attempt`
- `score`
- `score_direction`
- `failure_reason`
- `artifacts`

Recommended additional fields:
- `phase_id`
- `status`
- `selected`
- `created_at`
- `closed_at`

`score` should be interpreted only together with `score_direction`.

Recommended `score_direction` values:
- `higher_is_better`
- `lower_is_better`

## ReAct inside a branch

Inside one branch, ReAct remains useful for:
- tool selection
- observation and correction
- short-loop decision making
- context gathering

The branch should still be bounded by:
- timeout
- max attempts
- tool budget
- token budget

## Reflexion after failure

When a branch fails, Reflexion can:
- summarize what failed
- explain why the current path underperformed
- propose a revised hypothesis
- create the next branch candidate

Reflexion should update branch metadata rather than hiding failure inside a long chat transcript.

## PR review packet in the phase graph

`pr_packet_and_handoff` should emit a normalized artifact with:
- executive summary
- requirements and ADR references
- changed-area table
- validation results table
- risk matrix
- reviewer checklist
- one visual diagram of architecture or control-flow impact

The packet can use a two-step generation mode:
1. draft an explanation in prose or markdown
2. convert it into a structured review-packet schema

For reviewer-facing layout, table conventions, and visual requirements, see:
- [`pr-review-packet-visual-language.md`](./pr-review-packet-visual-language.md)
- [`pr-review-packet-example.md`](./pr-review-packet-example.md)

For gate rules, exemption paths, and trace-linked handoff behavior, see:
- [`pr-review-packet-workflow-integration.md`](./pr-review-packet-workflow-integration.md)

## Operational guidance

Trace metadata for phase-graph workflows should include:
- `workflow_id`
- `phase_id`
- `branch_id`
- `parent_branch_id`
- `generation_mode`
- `selected_branch_id`

The chosen branch outcome should be written back to the phase graph before the workflow advances.
