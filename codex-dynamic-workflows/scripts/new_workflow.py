#!/usr/bin/env python3
"""Create a Codex dynamic workflow artifact directory."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_PACKETS = [
    {
        "id": "01-discovery",
        "objective": "Map the current context, sources, constraints, and acceptance criteria.",
        "ownership": "Read-only discovery.",
        "assignee": "parent",
    },
    {
        "id": "02-execution",
        "objective": "Perform the main implementation or analysis slice with a bounded write scope.",
        "ownership": "Task-specific files or artifacts.",
        "assignee": "subagent-or-parent",
    },
    {
        "id": "03-verification",
        "objective": "Verify the integrated outcome against the original success criteria.",
        "ownership": "Checks, tests, install smoke, or manual audit.",
        "assignee": "parent",
    },
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64].strip("-") or "workflow"


def write_new(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def packet_markdown(packet: dict[str, str], title: str) -> str:
    return f"""# Packet {packet["id"]}: {packet["objective"]}

Packet ID: {packet["id"]}
Objective: {packet["objective"]}
Context: Workflow `{title}`. Add task-specific context before delegation.
Files / sources:
- TBD
Ownership: {packet["ownership"]}
Assignee: {packet["assignee"]}

## Do

- Keep the packet bounded and self-contained.
- Produce evidence, not just conclusions.
- Note any assumptions that affect integration.

## Do Not

- Revert unrelated edits.
- Expand scope beyond this packet.
- Perform risky external or destructive actions without approval.

## Expected Output

- A concise Markdown result under `results/{packet["id"]}.md`.

## Verification

- TBD

## Stop Condition

- Stop when the expected output is written or a blocker is clearly documented.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Workflow title or task summary")
    parser.add_argument(
        "--root",
        default=".workflow",
        help="Directory where workflow runs are stored (default: .workflow)",
    )
    parser.add_argument("--slug", help="Optional explicit workflow slug")
    parser.add_argument(
        "--packets",
        type=int,
        default=3,
        help="Number of default packet templates to create, 0-3 (default: 3)",
    )
    args = parser.parse_args()

    slug = slugify(args.slug or args.title)
    run_dir = Path(args.root) / slug
    packets_dir = run_dir / "packets"
    results_dir = run_dir / "results"
    packets_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    packets = DEFAULT_PACKETS[: max(0, min(args.packets, len(DEFAULT_PACKETS)))]
    state = {
        "title": args.title,
        "slug": slug,
        "created_at": now,
        "status": "planned",
        "approval": {"required": None, "granted": None, "notes": ""},
        "budgets": {
            "max_concurrent_agents": 4,
            "max_total_agents": 12,
            "time_minutes": None,
            "token_budget": None,
        },
        "packets": [
            {
                "id": packet["id"],
                "objective": packet["objective"],
                "status": "pending",
                "assignee": packet["assignee"],
                "result": None,
            }
            for packet in packets
        ],
        "verification": {"status": "not_started", "checks": []},
    }

    write_new(
        run_dir / "plan.md",
        f"""# {args.title}

## Goal

## Success Criteria

## Current Context

## Constraints

## Risks

## Approval Required

## Work Packets

## Integration Policy

## Verification

## Reusable Artifacts
""",
    )
    write_new(
        run_dir / "orchestration.md",
        f"""# Orchestration: {args.title}

## Execution Rules

- Keep the original objective intact.
- Ask for approval before risky, expensive, external, or destructive actions.
- Keep immediate blocking work local.
- Delegate only bounded, disjoint, materially useful packets.
- Integrate packet results before final verification.
- Close subagents when they are no longer needed.

## Phases

1. Observe current context.
2. Plan packets and approval gates.
3. Execute local blocking work and parallel sidecar packets.
4. Integrate accepted results.
5. Verify against success criteria.
6. Learn by saving reusable recipes only when warranted.

## Branching Rules

- If a risky action is required, stop and ask for approval.
- If subagent tools are unavailable, simulate packets with isolated result notes.
- If packet results conflict, inspect authoritative sources before choosing.
- If verification fails, loop back to the smallest failing packet.

## Packet Prompts

See `packets/`.

## Completion Audit

- Success criteria satisfied:
- Verification evidence recorded:
- Risks accepted or resolved:
- Final report written:
""",
    )
    write_new(run_dir / "state.json", json.dumps(state, indent=2) + "\n")
    write_new(
        run_dir / "integration.md",
        f"""# Integration: {args.title}

## Accepted

## Rejected

## Conflicts

## Decisions

## Remaining Risks

## Verification Still Needed
""",
    )
    write_new(
        run_dir / "final-report.md",
        f"""# Final Report: {args.title}

## Outcome

## Accepted Results

## Rejected Results

## Conflicts Resolved

## Verification Evidence

## Remaining Risks

## Reusable Follow-up
""",
    )

    for packet in packets:
        write_new(packets_dir / f"{packet['id']}.md", packet_markdown(packet, args.title))

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
