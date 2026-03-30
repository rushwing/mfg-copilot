# ADR 0003: Schema-First Structured I/O with Constrained Generation

## Status

Accepted

## Context

The platform will coordinate multiple agents, approvals, retrieval results, and human review checkpoints. Several of these artifacts are consumed by other services rather than by end users:

- orchestrator-to-agent request and response envelopes
- approval requests and decisions
- retrieval results with citations
- future A2A task payloads
- future PR review packets and audit artifacts

If these artifacts are produced as free-form text only, multi-agent coordination becomes fragile:
- downstream parsing is brittle
- runbooks can drift from actual runtime behavior
- human review becomes harder because state and evidence are not normalized
- model-only review loops can hide failure modes until late

At the same time, forcing every LLM interaction into a rigid schema would over-constrain legitimate user-facing prose and exploratory reasoning.

## Decision

Use a schema-first structured I/O model for machine-consumed artifacts.

### Canonical contract rule

- canonical contracts live in `packages/py/shared-schemas/`
- schemas should be provider-agnostic and versioned
- prompt wording and decoder choice must conform to the schema, not define it

### Output generation rule

For machine-consumed outputs, use constrained or structured generation whenever the provider path supports it.

Preferred order:
1. provider-native structured output or grammar support
2. Outlines-based constrained decoding as a portability layer or fallback
3. free-form generation plus validation only when neither of the above is practical

### Input handling rule

Do not use Outlines to constrain raw human input at the UI boundary.

Instead:
- accept natural user input
- normalize it into structured request envelopes after ingestion
- validate required fields before orchestration or cross-agent handoff

### Scope rule

Use structured generation for:
- approval envelopes and decisions
- orchestrator handoff payloads
- retrieval citations and evidence references
- future A2A task messages
- review packets, risk summaries, and release gates

Do not require structured generation for:
- conversational user-facing answers
- exploratory brainstorming
- long-form drafting where only the final artifact envelope needs structure

## Consequences

Benefits:
- multi-agent handoffs become easier to validate and trace
- future A2A integration can reuse repository-owned schemas
- review and audit artifacts become comparable across runs
- provider changes do not force contract redesign

Costs:
- prompts and schemas require tighter governance
- constrained decoding can reduce flexibility for poorly scoped tasks
- some providers and model paths may need fallback logic

## Provider strategy

Use provider-native structured generation first where available.

- OpenAI paths should prefer native JSON-schema-based structured outputs for machine-consumed artifacts
- SGLang or other local-serving paths should prefer native grammar or structured-generation support when available
- Outlines is approved as a constrained-decoding adapter for local or cross-provider portability, especially when provider-native support is missing or inconsistent

Outlines is not the canonical contract layer. The schema remains canonical; Outlines is one possible enforcement mechanism.

## Follow-up

- keep adding shared schemas before implementation logic hardcodes payload shapes
- include decoder mode and validation outcome in trace metadata for structured generations
- design future A2A and review-packet payloads against shared schemas rather than ad hoc markdown
