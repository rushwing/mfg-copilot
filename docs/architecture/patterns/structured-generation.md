# Structured Generation

This note explains how the project should use schema-constrained generation without over-structuring the whole system.

## Core idea

Use free-form language for human interaction.

Use schema-constrained generation for machine-consumed artifacts.

That split keeps the UX natural while making multi-agent coordination reliable.

## Where to use it

Good candidates:
- approval requests and approval decisions
- orchestrator step outputs
- agent handoff payloads
- retrieval citations and evidence bundles
- review packets and release-gate summaries

Poor candidates:
- raw user prompts
- open-ended discovery chat
- long narrative answers shown directly to humans

## Input rule

Human input should arrive as natural language or forms.

After ingestion, the gateway or orchestrator can normalize it into structured fields such as:
- intent
- requested scope
- project, phase, site, or station context
- risk class
- expected output mode

Normalization should be validated against shared schemas before agent routing or remote handoff.

## Output rule

When another service, agent, or review workflow consumes the result, the producer should emit:
- a schema-aligned payload
- trace metadata
- validation status

If a human-facing explanation is also needed, include it as a field inside the structured envelope instead of making the whole artifact unstructured.

## Decoder strategy

Use this order:

1. provider-native structured output
2. provider-native grammar support
3. Outlines constrained decoding
4. free-form generation with strict post-validation

## How Outlines fits

Outlines is a good fit when:
- a local or open-weight model path lacks reliable native structured outputs
- the same schema needs to run across more than one backend
- regex, grammar, or JSON-shape enforcement is needed for control-plane artifacts

Outlines is a poor fit when:
- the provider already offers stronger native structured-output support
- the artifact is mostly prose and only lightly structured
- decoding cost or latency is more important than portability

## Operational guidance

For structured generations, traces should record:
- `schema_id`
- `schema_version`
- `decoder_mode`
- `validation_passed`
- `repair_count`

Recommended `decoder_mode` values:
- `native_json_schema`
- `native_grammar`
- `outlines_json`
- `outlines_regex`
- `freeform_validated`

## Suggested early rollout

Phase 0 and Phase 1 should apply structured generation first to:
- approval envelopes
- retrieval evidence payloads
- orchestrator handoff envelopes

Later phases can extend the same pattern to:
- A2A task payloads
- review packets
- execution evidence packages
