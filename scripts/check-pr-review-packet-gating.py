#!/usr/bin/env python3

import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKET_SCHEMA = ROOT / "packages/py/shared-schemas/pr-review-packet.schema.yaml"
GATE_SCHEMA = ROOT / "packages/py/shared-schemas/pr-review-packet-gate-decision.schema.yaml"
CONTRACT_DOC = ROOT / "packages/py/shared-schemas/pr-review-packet-contract.md"
WORKFLOW_DOC = ROOT / "docs/architecture/patterns/pr-review-packet-workflow-integration.md"
PATTERN_INDEX = ROOT / "docs/architecture/patterns/README.md"
PHASE_DOC = ROOT / "docs/architecture/patterns/phase-graph-orchestration.md"
STRUCTURED_DOC = ROOT / "docs/architecture/patterns/structured-generation.md"
GLOSSARY = ROOT / "docs/GLOSSARY.md"
FULL_EXAMPLE = ROOT / "packages/py/shared-schemas/examples/pr-review-packet-gate-decision.full.example.json"
EXEMPT_EXAMPLE = ROOT / "packages/py/shared-schemas/examples/pr-review-packet-gate-decision.exempt.example.json"
PACKET_EXAMPLE = ROOT / "packages/py/shared-schemas/examples/pr-review-packet.example.json"

DECISION_PATH = re.compile(r"^artifacts/pr-review-packets/pr-(\d+)/gate-decision\.json$")
PACKET_PATH = re.compile(r"^artifacts/pr-review-packets/pr-(\d+)/review-packet\.json$")
REVIEWER_PATH = re.compile(r"^artifacts/pr-review-packets/pr-(\d+)/review-packet\.md$")


def fail(message: str) -> None:
    print(f"check-pr-review-packet-gating: {message}", file=sys.stderr)
    raise SystemExit(1)


def ensure_file(path: pathlib.Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")


def ensure_text(path: pathlib.Path, needle: str) -> None:
    if needle not in path.read_text(encoding="utf-8"):
        fail(f"{path.relative_to(ROOT)} is missing required text: {needle}")


def ensure_schema_guidance() -> None:
    for path in [PACKET_SCHEMA, GATE_SCHEMA, CONTRACT_DOC, WORKFLOW_DOC, PATTERN_INDEX, PHASE_DOC, STRUCTURED_DOC, GLOSSARY]:
        ensure_file(path)

    for needle in [
        "trace:",
        "gating:",
        "packet_policy_class",
        "review_ready",
        "merge_ready",
    ]:
        ensure_text(PACKET_SCHEMA, needle)

    for needle in [
        "packet_exempt",
        "decision_path",
        "trace:",
        "phase_id",
    ]:
        ensure_text(GATE_SCHEMA, needle)

    for needle in [
        "pr-review-packet-gate-decision.schema.yaml",
        "trace.workflow_id",
        "gating.review_ready",
        "gate-decision.full.example.json",
        "gate-decision.exempt.example.json",
    ]:
        ensure_text(CONTRACT_DOC, needle)

    for needle in [
        "## Packet policy classes",
        "## Review-ready vs merge-ready rules",
        "## Exemption path",
        "## Trace correlation",
        "## Workflow examples",
    ]:
        ensure_text(WORKFLOW_DOC, needle)

    for needle in [
        "pr-review-packet-workflow-integration.md",
    ]:
        ensure_text(PATTERN_INDEX, needle)
        ensure_text(PHASE_DOC, needle)
        ensure_text(STRUCTURED_DOC, needle)

    for needle in [
        "### packet_policy_class",
        "### review_ready",
        "### merge_ready",
    ]:
        ensure_text(GLOSSARY, needle)


def ensure_trace_block(trace: dict) -> None:
    required = [
        "workflow_id",
        "phase_id",
        "branch_id",
        "selected_branch_id",
        "harness_run_id",
        "langsmith_run_id",
    ]
    for key in required:
        if key not in trace:
            fail(f"trace is missing required key '{key}'")
    if trace["phase_id"] != "pr_packet_and_handoff":
        fail("trace.phase_id must be pr_packet_and_handoff")


def ensure_gate_decision(path: pathlib.Path, expected_class: str, exempt: bool) -> None:
    payload = load_json(path)

    if payload.get("schema_id") != "pr-review-packet-gate-decision":
        fail(f"{path.name} must use schema_id pr-review-packet-gate-decision")
    if payload.get("schema_version") != "v1":
        fail(f"{path.name} must use schema_version v1")
    if payload.get("packet_policy_class") != expected_class:
        fail(f"{path.name} must use packet_policy_class {expected_class}")

    pr_number = payload.get("pr_number")
    if not isinstance(pr_number, int) or pr_number < 1:
        fail(f"{path.name} must use a positive integer pr_number")

    artifact = payload.get("artifact")
    if not isinstance(artifact, dict):
        fail(f"{path.name} artifact must be an object")

    decision = artifact.get("decision_path")
    if not isinstance(decision, str):
        fail(f"{path.name} must include artifact.decision_path")
    match = DECISION_PATH.fullmatch(decision)
    if not match or int(match.group(1)) != pr_number:
        fail(f"{path.name} decision_path must match artifacts/pr-review-packets/pr-<number>/gate-decision.json")

    packet_path = artifact.get("packet_path")
    reviewer_path = artifact.get("reviewer_packet_path")
    if exempt:
        if payload.get("exemption_reason") is None:
            fail(f"{path.name} must record an exemption_reason")
        if packet_path is not None or reviewer_path is not None:
            fail(f"{path.name} must not point to packet artifacts for exempt decisions")
    else:
        if payload.get("exemption_reason") is not None:
            fail(f"{path.name} must not record an exemption_reason for non-exempt decisions")
        if not isinstance(packet_path, str) or not PACKET_PATH.fullmatch(packet_path):
            fail(f"{path.name} must include a canonical packet_path")
        if not isinstance(reviewer_path, str) or not REVIEWER_PATH.fullmatch(reviewer_path):
            fail(f"{path.name} must include a canonical reviewer_packet_path")

    trace = payload.get("trace")
    if not isinstance(trace, dict):
        fail(f"{path.name} must include a trace block")
    ensure_trace_block(trace)


def ensure_packet_example() -> None:
    payload = load_json(PACKET_EXAMPLE)
    trace = payload.get("trace")
    gating = payload.get("gating")

    if not isinstance(trace, dict):
        fail("pr-review-packet.example.json must include a trace block")
    ensure_trace_block(trace)

    if not isinstance(gating, dict):
        fail("pr-review-packet.example.json must include a gating block")
    if gating.get("gate_rule_id") != "pr-review-packet-gate-v1":
        fail("packet example gating.gate_rule_id must be pr-review-packet-gate-v1")
    if gating.get("packet_policy_class") not in {"full_packet_required", "simplified_packet_allowed"}:
        fail("packet example must use a packet-backed policy class")


def main() -> None:
    for path in [FULL_EXAMPLE, EXEMPT_EXAMPLE, PACKET_EXAMPLE]:
        ensure_file(path)

    ensure_schema_guidance()
    ensure_gate_decision(FULL_EXAMPLE, "full_packet_required", exempt=False)
    ensure_gate_decision(EXEMPT_EXAMPLE, "packet_exempt", exempt=True)
    ensure_packet_example()
    print("check-pr-review-packet-gating: ok")


if __name__ == "__main__":
    main()
