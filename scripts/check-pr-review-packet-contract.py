#!/usr/bin/env python3

import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "packages/py/shared-schemas/pr-review-packet.schema.yaml"
CONTRACT_DOC_PATH = ROOT / "packages/py/shared-schemas/pr-review-packet-contract.md"
EXAMPLE_PATH = ROOT / "packages/py/shared-schemas/examples/pr-review-packet.example.json"
README_PATH = ROOT / "packages/py/shared-schemas/README.md"

REQ_PATTERN = re.compile(r"^REQ-\d{3}$")
ADR_PATTERN = re.compile(r"^\d{4}-[a-z0-9][a-z0-9-]*$")
PACKET_ID_PATTERN = re.compile(r"^pr-(\d+)-review-packet$")
ARTIFACT_ROOT_PATTERN = re.compile(r"^artifacts/pr-review-packets/pr-(\d+)$")


def fail(message: str) -> None:
    print(f"check-pr-review-packet-contract: {message}", file=sys.stderr)
    raise SystemExit(1)


def ensure_file(path: pathlib.Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_example() -> dict:
    try:
        return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"example fixture is not valid JSON: {exc}")


def ensure_required_keys(payload: dict) -> None:
    required = [
        "schema_id",
        "schema_version",
        "packet_id",
        "pr_number",
        "pr_title",
        "generation_mode",
        "artifact",
        "linked_requirements",
        "linked_adrs",
        "summary",
        "validation",
        "risks",
        "reviewer_checklist",
        "visuals",
    ]
    for key in required:
        if key not in payload:
            fail(f"example fixture is missing required key '{key}'")


def ensure_identifier_formats(payload: dict) -> int:
    if payload["schema_id"] != "pr-review-packet":
        fail("schema_id must be 'pr-review-packet'")

    if not re.fullmatch(r"v\d+", payload["schema_version"]):
        fail("schema_version must match v<number>")

    match = PACKET_ID_PATTERN.fullmatch(payload["packet_id"])
    if not match:
        fail("packet_id must match pr-<number>-review-packet")

    pr_number = payload["pr_number"]
    if not isinstance(pr_number, int) or pr_number < 1:
        fail("pr_number must be a positive integer")

    if int(match.group(1)) != pr_number:
        fail("packet_id PR number must match pr_number")

    for req in payload["linked_requirements"]:
        if not isinstance(req, str) or not REQ_PATTERN.fullmatch(req):
            fail("linked_requirements entries must match REQ-<3 digits>")

    for adr in payload["linked_adrs"]:
        if not isinstance(adr, str) or not ADR_PATTERN.fullmatch(adr):
            fail("linked_adrs entries must use the ADR file stem format")

    return pr_number


def ensure_artifact_paths(payload: dict, pr_number: int) -> None:
    artifact = payload["artifact"]
    if not isinstance(artifact, dict):
        fail("artifact must be an object")

    required = [
        "artifact_root",
        "machine_packet_path",
        "reviewer_packet_path",
        "visuals_dir",
    ]
    for key in required:
        if key not in artifact:
            fail(f"artifact is missing required key '{key}'")

    root_match = ARTIFACT_ROOT_PATTERN.fullmatch(artifact["artifact_root"])
    if not root_match:
        fail("artifact_root must match artifacts/pr-review-packets/pr-<number>")

    if int(root_match.group(1)) != pr_number:
        fail("artifact_root PR number must match pr_number")

    expected_root = f"artifacts/pr-review-packets/pr-{pr_number}"
    if artifact["machine_packet_path"] != f"{expected_root}/review-packet.json":
        fail("machine_packet_path must use the canonical review-packet.json path")
    if artifact["reviewer_packet_path"] != f"{expected_root}/review-packet.md":
        fail("reviewer_packet_path must use the canonical review-packet.md path")
    if artifact["visuals_dir"] != f"{expected_root}/visuals":
        fail("visuals_dir must use the canonical visuals path")

    for visual in payload["visuals"]:
        if "path" in visual and not visual["path"].startswith(f"{artifact['visuals_dir']}/"):
            fail("visual paths must live under artifact.visuals_dir")


def ensure_section_completeness(payload: dict) -> None:
    summary = payload["summary"]
    if not isinstance(summary, dict):
        fail("summary must be an object")
    if not summary.get("executive_summary"):
        fail("summary.executive_summary must be non-empty")
    if not isinstance(summary.get("changed_areas"), list) or not summary["changed_areas"]:
        fail("summary.changed_areas must be a non-empty array")

    if not isinstance(payload["validation"], list) or not payload["validation"]:
        fail("validation must be a non-empty array")
    for item in payload["validation"]:
        if item.get("status") not in {"passed", "failed", "skipped"}:
            fail("validation status must be passed, failed, or skipped")

    if not isinstance(payload["risks"], list) or not payload["risks"]:
        fail("risks must be a non-empty array")
    for item in payload["risks"]:
        if item.get("severity") not in {"low", "medium", "high"}:
            fail("risk severity must be low, medium, or high")

    if not isinstance(payload["reviewer_checklist"], list) or not payload["reviewer_checklist"]:
        fail("reviewer_checklist must be a non-empty array")

    if not isinstance(payload["visuals"], list):
        fail("visuals must be an array")


def ensure_docs_reference_conventions() -> None:
    contract_doc = CONTRACT_DOC_PATH.read_text(encoding="utf-8")
    schema_doc = SCHEMA_PATH.read_text(encoding="utf-8")
    package_readme = README_PATH.read_text(encoding="utf-8")

    for needle in [
        "artifacts/pr-review-packets/pr-<pr_number>/",
        "draft_then_structure",
        "REQ-018",
        "0004-phase-based-orchestration-over-pure-react",
    ]:
        if needle not in contract_doc:
            fail(f"contract doc is missing required guidance: {needle}")

    for needle in [
        "schema_id",
        "schema_version",
        "artifact:",
        "reviewer_packet_path",
        "visuals:",
    ]:
        if needle not in schema_doc:
            fail(f"schema file is missing expected contract field: {needle}")

    if "pr-review-packet-contract.md" not in package_readme:
        fail("shared schema README must link to pr-review-packet-contract.md")


def main() -> None:
    for path in [SCHEMA_PATH, CONTRACT_DOC_PATH, EXAMPLE_PATH, README_PATH]:
        ensure_file(path)

    payload = load_example()
    ensure_required_keys(payload)
    pr_number = ensure_identifier_formats(payload)
    ensure_artifact_paths(payload, pr_number)
    ensure_section_completeness(payload)
    ensure_docs_reference_conventions()
    print("check-pr-review-packet-contract: ok")


if __name__ == "__main__":
    main()
