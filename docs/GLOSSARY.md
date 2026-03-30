# Glossary

This file standardizes repository-level terms that appear across requirements, ADRs, schemas, runbooks, and review artifacts.

Use these definitions as the default meaning unless a document explicitly scopes a term more narrowly.

## How To Use This File

- prefer glossary terms in new ADRs, REQs, schemas, and reviewer packets
- link here when a term could be misunderstood by new contributors or coding agents
- update this file when a platform-level term becomes stable enough to deserve a canonical meaning

## Workflow Terms

### story lifecycle

The requirement-level status model used for backlog and delivery visibility.

Canonical values:
- `draft`
- `ready`
- `in_progress`
- `blocked`
- `review`
- `done`
- `cancelled`

### workflow_phase

The current execution node inside the long-running engineering workflow.

Canonical values:
- `requirement_assessment`
- `test_design`
- `implementation`
- `review_and_repair`
- `pr_packet_and_handoff`

`workflow_phase` is not the same thing as story lifecycle status.

### phase

The roadmap or delivery bucket used in `tasks/phases/PHASE-xxx.md`, such as `phase-0` or `phase-2`.

This term refers to delivery sequencing, not execution-state nodes inside a workflow graph.

### phase graph

The long-running engineering workflow model where execution moves through explicit nodes such as `requirement_assessment`, `implementation`, and `pr_packet_and_handoff`.

In this repository, the phase graph is the platform truth for workflow execution.

### searchable node

A phase-graph node that is allowed to explore multiple candidate paths before selecting a branch outcome.

Searchable nodes typically use best-first or beam search and may use limited backtracking when needed.

### branch

A candidate path explored inside a searchable node.

A branch carries its own hypothesis, attempt count, score, artifacts, and outcome metadata.

## Search And Execution Terms

### ReAct

The local branch-level pattern of reasoning, acting, observing, and iterating with tools.

In this repository, ReAct is for branch execution, not the platform-level workflow runtime.

### Reflexion

The repair and redirection mechanism used after a branch fails or underperforms.

It summarizes failure and proposes a better next branch rather than hiding the failure in chat history alone.

### branch_id

The unique identifier for one explored branch within a searchable node.

### parent_branch_id

The identifier of the branch that directly preceded the current branch.

Used to reconstruct branch lineage during retries, branching, and repair.

### hypothesis

The explicit idea or explanation a branch is testing, such as a suspected failure cause or implementation approach.

### score

The ranking value used to compare branches within the same searchable node.

`score` must be interpreted together with `score_direction`.

### score_direction

The declared meaning of a branch score.

Canonical values:
- `higher_is_better`
- `lower_is_better`

### artifact

A durable output produced by a workflow or branch, such as a schema, packet, evidence bundle, report, trace reference, or diagram.

## Structured I/O Terms

### schema-first

The rule that machine-consumed contracts are defined in repository-owned schemas first, and decoder choice comes afterward.

### structured generation

Output generation constrained or validated against a machine-consumed schema, grammar, or equivalent contract.

### direct_structured

A generation mode where the model emits the structured artifact directly.

Best for low-entropy control-plane outputs with small typed fields.

### draft_then_structure

A generation mode where the model first produces a natural-language or markdown draft, then converts it into the required structured artifact.

Best for reasoning-heavy or synthesis-heavy outputs.

### PR review packet

The reviewer-facing artifact emitted by `pr_packet_and_handoff`.

It typically includes:
- executive summary
- linked REQs and ADRs
- changed-area table
- validation evidence
- risk matrix
- reviewer checklist
- at least one visual when architecture or control-flow impact matters

## Platform Terms

### orchestrator

The service and runtime layer that owns long-running workflow control, checkpoints, retries, human-in-the-loop pauses, and cross-agent handoff state.

### agent service

A domain-specific service such as `doc-copilot`, `deploy-agent`, or `ops-agent` that owns prompts, tool selection, and domain cognition.

### toolhub

The platform-owned integration surface for enterprise reads and approved execution actions.

Agents should not bypass `toolhub` to talk directly to enterprise systems.

### rag-service

The single normalized retrieval interface for knowledge and evidence lookup.

Agents should not talk directly to Milvus or Elasticsearch.

### HITL

Human in the loop.

A workflow checkpoint where human review, approval, or correction is required before the workflow continues.

### A2A

Agent-to-agent communication protocol used for remote or cross-service agent collaboration.

In this repository, A2A is distinct from MCP and is intended for agent collaboration rather than tool invocation.

### MCP

Model Context Protocol.

Used for tool and resource access, not as the primary protocol for remote agent-to-agent coordination.

## Governance Rule

When a term here conflicts with a looser or informal usage elsewhere in the repo, this glossary should be treated as the default repository meaning until a newer ADR or glossary update changes it.
