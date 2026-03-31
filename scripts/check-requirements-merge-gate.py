#!/usr/bin/env python3

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Dict, List, Optional, Sequence, Tuple


ROOT = pathlib.Path(__file__).resolve().parent.parent
REQ_PATTERN = re.compile(r"\bREQ-\d{3}\b")
REQ_FILE_PATTERNS = [
    re.compile(r"^tasks/features/(REQ-\d{3})\.md$"),
    re.compile(r"^tasks/archive/done/(REQ-\d{3})\.md$"),
    re.compile(r"^tasks/archive/cancelled/(REQ-\d{3})\.md$"),
]
AUTOFIX_STATUS = "review"
AUTOFIX_PHASE = "pr_packet_and_handoff"


def fail(message: str) -> None:
    print(f"check-requirements-merge-gate: {message}", file=sys.stderr)
    raise SystemExit(1)


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def load_event(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"event payload not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"event payload is not valid JSON: {exc}")


def get_pr_payload(event: dict) -> dict:
    pr = event.get("pull_request")
    if not isinstance(pr, dict):
        fail("this gate expects a pull_request event payload")
    return pr


def changed_files(base_sha: str, head_sha: str) -> List[str]:
    output = git("diff", "--name-only", base_sha, head_sha)
    return [line.strip() for line in output.splitlines() if line.strip()]


def extract_linked_requirements(pr: dict, files: Sequence[str]) -> List[str]:
    reqs = set()
    body = pr.get("body") or ""
    if isinstance(body, str):
        reqs.update(REQ_PATTERN.findall(body))

    for file_path in files:
        for pattern in REQ_FILE_PATTERNS:
            match = pattern.fullmatch(file_path)
            if match:
                reqs.add(match.group(1))
                break

    return sorted(reqs)


def find_req_path(req_id: str) -> Optional[pathlib.Path]:
    for rel in [
        f"tasks/features/{req_id}.md",
        f"tasks/archive/done/{req_id}.md",
        f"tasks/archive/cancelled/{req_id}.md",
    ]:
        path = ROOT / rel
        if path.is_file():
            return path
    return None


def parse_frontmatter(path: pathlib.Path) -> Dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        fail(f"{path.relative_to(ROOT)} is missing YAML frontmatter")

    data: Dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()

    fail(f"{path.relative_to(ROOT)} is missing the closing YAML frontmatter marker")
    return {}


def update_status(path: pathlib.Path, new_status: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    updated = False
    for index, line in enumerate(lines):
        if line.startswith("status:"):
            lines[index] = f"status: {new_status}"
            updated = True
            break
    if not updated:
        fail(f"{path.relative_to(ROOT)} is missing a status field")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(path: Optional[pathlib.Path], outputs: Dict[str, str]) -> None:
    if path is None:
        return
    with path.open("a", encoding="utf-8") as handle:
        for key, value in outputs.items():
            if "\n" in value:
                handle.write(f"{key}<<EOF\n{value}\nEOF\n")
            else:
                handle.write(f"{key}={value}\n")


def summarize_blockers(blockers: Sequence[Tuple[str, str]]) -> str:
    return "; ".join(f"{req_id}: {reason}" for req_id, reason in blockers)


def evaluate_requirements(
    linked_requirements: Sequence[str],
    allow_autofix: bool,
    same_repository_branch: bool,
) -> Tuple[List[str], List[Tuple[str, str]]]:
    autofixed: List[str] = []
    blockers: List[Tuple[str, str]] = []

    for req_id in linked_requirements:
        path = find_req_path(req_id)
        if path is None:
            blockers.append((req_id, "linked requirement file does not exist"))
            continue

        frontmatter = parse_frontmatter(path)
        status = frontmatter.get("status", "")
        workflow_phase = frontmatter.get("workflow_phase", "")

        if status == "done":
            continue

        if status == AUTOFIX_STATUS and workflow_phase == AUTOFIX_PHASE:
            if not allow_autofix:
                blockers.append((req_id, "merge gate requires autofix but autofix mode is disabled"))
                continue
            if not same_repository_branch:
                blockers.append((req_id, "fork PR cannot auto-update requirement status to done"))
                continue

            update_status(path, "done")
            autofixed.append(req_id)
            continue

        blockers.append(
            (
                req_id,
                f"status={status or '<missing>'}, workflow_phase={workflow_phase or '<missing>'} is not merge-eligible",
            )
        )

    return autofixed, blockers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--event-path",
        default=os.environ.get("GITHUB_EVENT_PATH"),
        help="Path to the GitHub event JSON payload",
    )
    parser.add_argument(
        "--github-output",
        default=os.environ.get("GITHUB_OUTPUT"),
        help="Optional GitHub Actions output file",
    )
    parser.add_argument(
        "--autofix",
        action="store_true",
        help="Allow status=review + workflow_phase=pr_packet_and_handoff requirements to be closed to done",
    )
    args = parser.parse_args()

    if not args.event_path:
        fail("missing --event-path and GITHUB_EVENT_PATH is not set")

    event = load_event(pathlib.Path(args.event_path))
    pr = get_pr_payload(event)

    head = pr.get("head") or {}
    base = pr.get("base") or {}
    head_sha = head.get("sha")
    base_sha = base.get("sha")
    if not isinstance(head_sha, str) or not isinstance(base_sha, str):
        fail("pull_request payload is missing base/head SHAs")

    files = changed_files(base_sha, head_sha)
    linked_requirements = extract_linked_requirements(pr, files)
    same_repository_branch = (
        isinstance(head.get("repo"), dict)
        and isinstance(base.get("repo"), dict)
        and head["repo"].get("full_name") == base["repo"].get("full_name")
    )

    outputs: Dict[str, str] = {
        "status": "skipped",
        "linked_requirements": ",".join(linked_requirements),
        "autofixed": "false",
        "autofixed_requirements": "",
        "summary": "",
    }

    if not linked_requirements:
        outputs["summary"] = "No linked REQ references were found in the PR body or changed requirement files."
        write_outputs(pathlib.Path(args.github_output) if args.github_output else None, outputs)
        print(f"check-requirements-merge-gate: {outputs['summary']}")
        return

    autofixed, blockers = evaluate_requirements(
        linked_requirements=linked_requirements,
        allow_autofix=args.autofix,
        same_repository_branch=same_repository_branch,
    )

    if blockers:
        outputs["status"] = "failed"
        outputs["autofixed"] = "true" if autofixed else "false"
        outputs["autofixed_requirements"] = ",".join(autofixed)
        outputs["summary"] = summarize_blockers(blockers)
        write_outputs(pathlib.Path(args.github_output) if args.github_output else None, outputs)
        fail(outputs["summary"])

    outputs["status"] = "autofixed" if autofixed else "passed"
    outputs["autofixed"] = "true" if autofixed else "false"
    outputs["autofixed_requirements"] = ",".join(autofixed)
    if autofixed:
        outputs["summary"] = f"Autofixed linked requirements to done: {', '.join(autofixed)}"
    else:
        outputs["summary"] = f"All linked requirements are merge-eligible: {', '.join(linked_requirements)}"

    write_outputs(pathlib.Path(args.github_output) if args.github_output else None, outputs)
    print(f"check-requirements-merge-gate: {outputs['summary']}")


if __name__ == "__main__":
    main()
