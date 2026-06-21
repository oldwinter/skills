#!/usr/bin/env python3
"""Summarize workflow packet result files into an integration checklist."""

from __future__ import annotations

import argparse
from pathlib import Path


MARKERS = (
    "Accepted",
    "Rejected",
    "Conflict",
    "Decision",
    "Risk",
    "Verification",
    "Evidence",
    "TODO",
    "Blocker",
)
SECTION_ALIASES = {
    "accepted": "Accepted",
    "accepted results": "Accepted",
    "rejected": "Rejected",
    "rejected results": "Rejected",
    "conflict": "Conflicts",
    "conflicts": "Conflicts",
    "conflicts resolved": "Conflicts",
    "decision": "Decisions",
    "decisions": "Decisions",
    "risk": "Risks",
    "risks": "Risks",
    "remaining risks": "Risks",
    "verification": "Verification Evidence",
    "verification evidence": "Verification Evidence",
    "evidence": "Verification Evidence",
    "todo": "TODO",
    "blocker": "Blockers",
    "blockers": "Blockers",
}
SECTION_ORDER = (
    "Accepted",
    "Rejected",
    "Conflicts",
    "Decisions",
    "Risks",
    "Verification Evidence",
    "TODO",
    "Blockers",
)


def heading_for(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


def interesting_lines(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        if stripped.startswith(("-", "*", "#")) or any(marker.lower() in lowered for marker in MARKERS):
            lines.append(stripped)
    return lines[:50]


def normalize_item(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith(("-", "*")):
        return stripped[1:].strip()
    return stripped


def section_name(line: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith("## "):
        title = stripped.lstrip("#").strip().lower()
        return SECTION_ALIASES.get(title)
    if stripped.startswith(("-", "*", "#")) or not stripped.endswith(":"):
        return None
    title = stripped[:-1].strip().lower()
    return SECTION_ALIASES.get(title)


def structured_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {name: [] for name in SECTION_ORDER}
    current: str | None = None
    for line in text.splitlines():
        next_section = section_name(line)
        if next_section:
            current = next_section
            continue
        if line.startswith("#"):
            current = None
            continue
        if current is None:
            continue
        item = normalize_item(line)
        if item:
            sections[current].append(item)
    return {name: items for name, items in sections.items() if items}


def prefixed_items(items: list[str], heading: str) -> list[str]:
    return [f"- {heading}: {item}" for item in items[:50]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow_dir", help="Path to .workflow/<slug>")
    parser.add_argument(
        "--output",
        help="Optional output Markdown path (default: print to stdout)",
    )
    args = parser.parse_args()

    workflow_dir = Path(args.workflow_dir)
    results_dir = workflow_dir / "results"
    if not results_dir.is_dir():
        raise SystemExit(f"Missing results directory: {results_dir}")

    files = sorted(results_dir.glob("*.md"))
    lines = [f"# Integration Checklist: {workflow_dir.name}", ""]
    if not files:
        lines.extend(["No result files found.", ""])

    grouped: dict[str, list[str]] = {name: [] for name in SECTION_ORDER}
    fallback_blocks: list[tuple[str, list[str]]] = []
    for file in files:
        text = file.read_text(encoding="utf-8")
        heading = heading_for(file)
        sections = structured_sections(text)
        if sections:
            for name, items in sections.items():
                grouped[name].extend(prefixed_items(items, heading))
        else:
            fallback_blocks.append((heading, interesting_lines(text)))

    for name in SECTION_ORDER:
        if grouped[name]:
            lines.extend([f"## {name}", "", *grouped[name], ""])

    for heading, snippets in fallback_blocks:
        lines.extend([f"## {heading}", ""])
        if snippets:
            lines.extend(snippets)
        else:
            lines.append("No checklist-like lines found; inspect this result manually.")
        lines.append("")

    lines.extend(
        [
            "## Integration Decisions",
            "",
            "Accepted:",
            "",
            "Rejected:",
            "",
            "Conflicts:",
            "",
            "Remaining risks:",
            "",
            "Verification still needed:",
            "",
        ]
    )
    output = "\n".join(lines)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
