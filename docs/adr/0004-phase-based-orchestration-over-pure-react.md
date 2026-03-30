# ADR 0004: Phase-Based Orchestration Over Pure ReAct

## Status

Accepted

## Context

Pure ReAct loops are useful for local reasoning, tool use, and short iterative work. They become fragile when used as the only control structure for long-running engineering workflows.

In practice, pure ReAct tends to create several problems:
- workflow progress depends too heavily on single-run model quality
- long tasks can loop or drift without a durable phase boundary
- human review and approval checkpoints are hard to place consistently
- failures are difficult to localize because state is implicit in message history
- multi-agent collaboration lacks a stable platform truth for handoff and resume

The platform needs a workflow model that supports:
- explicit phase progression
- checkpoints and resumability
- human-in-the-loop pauses
- bounded retries and alternate strategies
- traceable branch exploration for difficult subproblems

## Decision

Use phase-based orchestration as the primary workflow model.

### Platform truth

- `LangGraph` owns the phase state machine
- `LangGraph` checkpoints are the durable runtime truth
- `LangGraph` handles HITL pauses, resume, retries, and terminal states

### Phase model

Long-running engineering workflows should be expressed as a phase graph, not as one unconstrained ReAct loop.

Default phase sequence:
1. `requirement_assessment`
2. `test_design`
3. `implementation`
4. `review_and_repair`
5. `pr_packet_and_handoff`

For small or low-risk stories, `test_design` may be folded into `requirement_assessment` as part of that phase's output instead of being persisted as a separate phase boundary.

### Search model

Some phase nodes may be marked `searchable`.

Inside a searchable node:
- use best-first or beam search by default
- use backtracking only when needed
- keep search bounded by branch count, depth, and budget

Each branch should record:
- `branch_id`
- `parent_branch_id`
- `hypothesis`
- `attempt`
- `score`
- `score_direction`
- `failure_reason`
- `artifacts`

`score` is a branch-ranking value, not a provider-specific raw metric dump. Branch ordering must interpret the score together with `score_direction`, so different agents do not silently invert selection behavior.

### Execution model

- `ReAct` is the default execution mode inside a single branch
- `Reflexion` is the default repair mechanism after a branch fails or underperforms
- search results should collapse back into the phase graph as the chosen branch outcome

### Review packet rule

`pr_packet_and_handoff` is a first-class workflow phase, not an informal afterthought.

Before merge, the workflow should produce a normalized PR review packet containing:
- change summary
- linked requirements and ADRs
- validation evidence
- risk matrix
- reviewer checklist
- visual flow or architecture impact summary

## Consequences

Benefits:
- durable workflow state no longer depends on chat history alone
- phase completion criteria become explicit and reviewable
- search-heavy tasks can explore alternatives without turning the whole system into DFS
- human review can happen at stable checkpoints with consistent artifacts
- PR review quality improves because handoff materials are mandatory workflow outputs

Costs:
- orchestration design becomes more explicit and structured
- searchable phases require branch scoring and budget control
- some simple workflows may feel more formal than a single free-form agent loop

## Non-goals

- do not model every workflow as a search tree
- do not use DFS as the default strategy for the entire system
- do not treat ReAct as the platform-level workflow runtime

## Follow-up

- define shared schemas for branch records and PR review packets
- add trace fields for branch lineage and selected-branch outcome
- document which phase nodes are searchable by default for each major workflow
