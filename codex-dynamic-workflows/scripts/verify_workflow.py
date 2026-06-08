#!/usr/bin/env python3
"""Check that a Codex dynamic workflow artifact is complete enough to audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = ("plan.md", "state.json", "orchestration.md", "integration.md", "final-report.md")
REQUIRED_DIRS = ("packets", "results")
STATE_STATUSES = {"planned", "in_progress", "complete", "blocked", "skipped"}
PACKET_STATUSES = {"pending", "in_progress", "complete", "blocked", "skipped"}


def nonempty_markdown_files(path: Path) -> list[Path]:
    if not path.is_dir():
        return []
    return [file for file in sorted(path.glob("*.md")) if file.read_text(encoding="utf-8").strip()]


def validate_state_schema(
    workflow_dir: Path,
    state: dict,
    packet_files: list[Path],
    result_files: list[Path],
) -> list[str]:
    failures: list[str] = []
    if state.get("slug") != workflow_dir.name:
        failures.append("state.slug must match workflow directory name")

    status = state.get("status")
    if not isinstance(status, str) or status not in STATE_STATUSES:
        failures.append(f"state.status has invalid value: {status}")

    approval = state.get("approval")
    if not isinstance(approval, dict):
        failures.append("state.approval must be an object")

    budgets = state.get("budgets")
    if not isinstance(budgets, dict):
        failures.append("state.budgets must be an object")

    verification = state.get("verification")
    if not isinstance(verification, dict):
        failures.append("state.verification must be an object")

    packets = state.get("packets")
    if not isinstance(packets, list):
        return failures

    packet_file_ids = {file.stem for file in packet_files}
    result_file_ids = {file.stem for file in result_files}
    seen_packet_ids: set[str] = set()
    for index, packet in enumerate(packets):
        if not isinstance(packet, dict):
            failures.append(f"state.packets[{index}] must be an object")
            continue
        packet_id = packet.get("id")
        if not isinstance(packet_id, str) or not packet_id.strip():
            failures.append(f"state.packets[{index}].id must be a non-empty string")
            continue
        if packet_id in seen_packet_ids:
            failures.append(f"Duplicate packet id: {packet_id}")
        seen_packet_ids.add(packet_id)
        if packet_id not in packet_file_ids:
            failures.append(f"Missing packet file for state packet: {packet_id}")

        packet_status = packet.get("status")
        if not isinstance(packet_status, str) or packet_status not in PACKET_STATUSES:
            failures.append(f"packet {packet_id} status has invalid value: {packet_status}")

        objective = packet.get("objective")
        if objective is not None and not isinstance(objective, str):
            failures.append(f"packet {packet_id} objective must be a string")

        result = packet.get("result")
        if result is None:
            continue
        if not isinstance(result, str):
            failures.append(f"packet {packet_id} result must be a string or null")
            continue
        result_path = Path(result)
        if result_path.is_absolute() or result_path.parts[:1] != ("results",):
            failures.append(f"packet {packet_id} result must be a relative results/ path")
            continue
        if result_path.suffix != ".md":
            failures.append(f"packet {packet_id} result must point to a Markdown file")
        if result_path.stem != packet_id:
            failures.append(f"Result file stem must match packet id for {packet_id}")
        if result_path.stem not in result_file_ids:
            failures.append(f"Missing result file referenced by packet {packet_id}: {result}")

    orphan_packet_files = packet_file_ids - seen_packet_ids
    for packet_id in sorted(orphan_packet_files):
        failures.append(f"Packet file missing from state: {packet_id}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow_dir", help="Path to .workflow/<slug>")
    parser.add_argument(
        "--allow-empty-results",
        action="store_true",
        help="Allow verification before result files exist.",
    )
    parser.add_argument(
        "--require-all-results",
        action="store_true",
        help="Require a non-empty result file for every packet in state.json.",
    )
    args = parser.parse_args()

    workflow_dir = Path(args.workflow_dir)
    failures: list[str] = []

    if not workflow_dir.is_dir():
        failures.append(f"Missing workflow directory: {workflow_dir}")
    for name in REQUIRED_FILES:
        path = workflow_dir / name
        if not path.is_file():
            failures.append(f"Missing file: {path}")
        elif not path.read_text(encoding="utf-8").strip():
            failures.append(f"Empty file: {path}")
    for name in REQUIRED_DIRS:
        path = workflow_dir / name
        if not path.is_dir():
            failures.append(f"Missing directory: {path}")

    state_path = workflow_dir / "state.json"
    state: dict | None = None
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"Invalid JSON in {state_path}: {exc}")
        else:
            for key in ("title", "slug", "status", "approval", "budgets", "packets", "verification"):
                if key not in state:
                    failures.append(f"Missing state key: {key}")
            if not isinstance(state.get("packets"), list):
                failures.append("state.packets must be a list")

    packet_files = nonempty_markdown_files(workflow_dir / "packets")
    result_files = nonempty_markdown_files(workflow_dir / "results")
    if not packet_files:
        failures.append("No non-empty packet files found under packets/")
    if not result_files and not args.allow_empty_results:
        failures.append("No non-empty result files found under results/")
    if state:
        failures.extend(validate_state_schema(workflow_dir, state, packet_files, result_files))
    if args.require_all_results and state and isinstance(state.get("packets"), list):
        result_ids = {file.stem for file in result_files}
        missing_results = [
            packet.get("id")
            for packet in state["packets"]
            if isinstance(packet, dict) and packet.get("id") not in result_ids
        ]
        for packet_id in missing_results:
            failures.append(f"Missing result for packet: {packet_id}")

    if failures:
        print("Workflow verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Workflow verification passed: {workflow_dir}")
    print(f"Packets: {len(packet_files)}")
    print(f"Results: {len(result_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
