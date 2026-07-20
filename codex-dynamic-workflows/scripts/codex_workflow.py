#!/usr/bin/env python3
"""Validate a Pi-style workflow script and convert it into Codex packets.

This is not a JavaScript runtime. It intentionally performs static extraction
only, so Codex can reuse the familiar `meta`, `phase`, and `agent` workflow
shape without pretending to have Pi's in-memory subagent runner.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


META_PREFIX_RE = re.compile(r"^\s*export\s+const\s+meta\s*=\s*", re.MULTILINE)
PHASE_RE = re.compile(r"\bphase\s*\(\s*(['\"`])(?P<title>[\s\S]*?)(?<!\\)\1\s*\)")
AGENT_RE = re.compile(
    r"\bagent\s*\(\s*(['\"`])(?P<prompt>[\s\S]*?)(?<!\\)\1\s*(?:,\s*(?P<opts>\{[\s\S]*?\}))?\s*\)",
    re.MULTILINE,
)
LABEL_RE = re.compile(r"\blabel\s*:\s*(['\"`])(?P<label>[\s\S]*?)(?<!\\)\1")
PHASE_OPT_RE = re.compile(r"\bphase\s*:\s*(['\"`])(?P<phase>[\s\S]*?)(?<!\\)\1")
NONDETERMINISTIC_RE = re.compile(
    r"\bDate\s*(?:\.|\[['\"]|`)\s*now\b|\bMath\s*(?:\.|\[['\"]|`)\s*random\b|\bnew\s+(?:\(?\s*)Date\s*\(",
    re.MULTILINE,
)
IDENTIFIER_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$")


@dataclass(frozen=True)
class WorkflowAgentCall:
    index: int
    prompt: str
    label: str
    phase: str | None


@dataclass(frozen=True)
class WorkflowPlan:
    meta: dict[str, Any]
    phases: list[str]
    agents: list[WorkflowAgentCall]


def js_object_to_python(value: str) -> Any:
    """Parse a small JavaScript object literal subset into Python data."""

    text = value.strip()
    text = quote_unquoted_keys(text)
    text = re.sub(r",\s*([}\]])", r"\1", text)
    text = replace_js_keywords(text)
    try:
        return ast.literal_eval(text)
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"meta must be a static object literal: {exc}") from exc


def quote_unquoted_keys(value: str) -> str:
    """Quote object keys without touching strings that look object-like."""

    result: list[str] = []
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(value):
        char = value[index]
        if quote:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue

        if char in ("'", '"', "`"):
            quote = char
            result.append(char)
            index += 1
            continue

        if char in ("{", ","):
            result.append(char)
            index += 1
            while index < len(value) and value[index].isspace():
                result.append(value[index])
                index += 1
            if index < len(value) and (value[index].isalpha() or value[index] in "_$"):
                key_start = index
                index += 1
                while index < len(value) and value[index] in IDENTIFIER_CHARS:
                    index += 1
                key = value[key_start:index]
                probe = index
                while probe < len(value) and value[probe].isspace():
                    probe += 1
                if probe < len(value) and value[probe] == ":":
                    result.append(f"'{key}'")
                    continue
                result.append(key)
                continue
            continue

        result.append(char)
        index += 1
    return "".join(result)


def replace_js_keywords(value: str) -> str:
    """Convert JS true/false/null tokens outside strings for ast.literal_eval."""

    replacements = {"true": "True", "false": "False", "null": "None"}
    result: list[str] = []
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(value):
        char = value[index]
        if quote:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue

        if char in ("'", '"', "`"):
            quote = char
            result.append(char)
            index += 1
            continue

        replaced = False
        for keyword, replacement in replacements.items():
            if not value.startswith(keyword, index):
                continue
            before = value[index - 1] if index > 0 else ""
            after_index = index + len(keyword)
            after = value[after_index] if after_index < len(value) else ""
            if before not in IDENTIFIER_CHARS and after not in IDENTIFIER_CHARS:
                result.append(replacement)
                index = after_index
                replaced = True
                break
        if replaced:
            continue

        result.append(char)
        index += 1
    return "".join(result)


def parse_script(script: str) -> WorkflowPlan:
    if NONDETERMINISTIC_RE.search(script):
        raise ValueError("workflow scripts must be deterministic: Date.now(), Math.random(), and new Date() are not allowed")

    meta_literal = extract_meta_literal(script)
    meta = js_object_to_python(meta_literal)
    if not isinstance(meta, dict):
        raise ValueError("meta must be an object")
    for key in ("name", "description"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError(f"meta.{key} must be a non-empty string")

    declared_phases = [
        phase.get("title")
        for phase in meta.get("phases", [])
        if isinstance(phase, dict) and isinstance(phase.get("title"), str)
    ]
    runtime_phases = [static_js_string(match, "title", "phase titles") for match in PHASE_RE.finditer(script)]
    phases = unique([*declared_phases, *runtime_phases])

    agents: list[WorkflowAgentCall] = []
    current_phase: str | None = None
    phase_positions = [(match.start(), static_js_string(match, "title", "phase titles")) for match in PHASE_RE.finditer(script)]
    for index, match in enumerate(AGENT_RE.finditer(script), start=1):
        for position, phase in phase_positions:
            if position < match.start():
                current_phase = phase
            else:
                break
        opts = match.group("opts") or ""
        label_match = LABEL_RE.search(opts)
        phase_match = PHASE_OPT_RE.search(opts)
        prompt = static_js_string(match, "prompt", "agent prompts").strip()
        label = static_js_string(label_match, "label", "agent labels").strip() if label_match else f"agent-{index:02d}"
        phase = static_js_string(phase_match, "phase", "agent phases").strip() if phase_match else current_phase
        agents.append(WorkflowAgentCall(index=index, prompt=prompt, label=label, phase=phase))

    if not agents:
        raise ValueError("workflow must call agent() at least once")

    return WorkflowPlan(meta=meta, phases=phases, agents=agents)


def extract_meta_literal(script: str) -> str:
    prefix = META_PREFIX_RE.match(script)
    if not prefix:
        raise ValueError("first statement must be `export const meta = { name, description }`")

    brace_start = script.find("{", prefix.end())
    if brace_start == -1:
        raise ValueError("meta must be a static object literal")

    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(brace_start, len(script)):
        char = script[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in ("'", '"', "`"):
            quote = char
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return script[brace_start : index + 1]

    raise ValueError("meta object literal is not closed")


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def static_js_string(match: re.Match[str], group_name: str, context: str) -> str:
    value = match.group(group_name)
    if match.group(1) == "`" and "${" in value:
        raise ValueError(f"{context} must be static string literals; template interpolation is not allowed")
    return unescape_js_string(value)


def unescape_js_string(value: str) -> str:
    return (
        value.replace(r"\'", "'")
        .replace(r"\"", '"')
        .replace(r"\`", "`")
        .replace(r"\n", "\n")
        .replace(r"\t", "\t")
        .replace(r"\\", "\\")
    )


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64].strip("-") or "workflow"


def looks_like_workflow_artifact(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "state.json").is_file()
        and (path / "plan.md").is_file()
        and (path / "packets").is_dir()
        and (path / "results").is_dir()
    )


def clear_generated_artifact(path: Path) -> None:
    """Remove only files this adapter generates inside an existing artifact."""

    if not looks_like_workflow_artifact(path):
        raise ValueError(f"refusing to overwrite non-workflow directory: {path}")
    for name in ("plan.md", "orchestration.md", "integration.md", "final-report.md", "state.json"):
        target = path / name
        if target.exists():
            target.unlink()
    for directory in (path / "packets", path / "results"):
        for file in directory.glob("*.md"):
            file.unlink()


def write_artifact(plan: WorkflowPlan, root: Path, slug: str | None = None, *, force: bool = False) -> Path:
    run_slug = slugify(slug or plan.meta["name"])
    run_dir = root / run_slug
    if run_dir.exists() and any(run_dir.iterdir()) and not force:
        raise FileExistsError(f"workflow artifact already exists: {run_dir} (pass --force to overwrite)")
    if run_dir.exists() and force and any(run_dir.iterdir()):
        clear_generated_artifact(run_dir)
    packets_dir = run_dir / "packets"
    results_dir = run_dir / "results"
    packets_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "plan.md").write_text(render_plan(plan), encoding="utf-8")
    (run_dir / "orchestration.md").write_text(render_orchestration(plan), encoding="utf-8")
    (run_dir / "integration.md").write_text(render_integration(plan), encoding="utf-8")
    (run_dir / "final-report.md").write_text(render_final_report(plan), encoding="utf-8")
    (run_dir / "state.json").write_text(json.dumps(render_state(plan, run_slug), indent=2) + "\n", encoding="utf-8")
    for agent in plan.agents:
        packet_id = f"{agent.index:02d}-{slugify(agent.label)}"
        (packets_dir / f"{packet_id}.md").write_text(render_packet(agent, packet_id), encoding="utf-8")
    return run_dir


def render_plan(plan: WorkflowPlan) -> str:
    phase_lines = "\n".join(f"- {phase}" for phase in plan.phases) or "- Unphased"
    packet_lines = "\n".join(f"- {agent.index:02d}: {agent.label} ({agent.phase or 'Unphased'})" for agent in plan.agents)
    return f"""# {plan.meta["name"]}

## Goal

{plan.meta["description"]}

## Success Criteria

- All packets produce auditable results.
- Parent agent integrates packet outputs before final answer.
- Verification evidence is recorded.

## Current Context

Generated from a Pi-style workflow script for Codex execution.

## Phases

{phase_lines}

## Work Packets

{packet_lines}

## Constraints

- This artifact is static. Codex must execute packets using available tools or simulated packet notes.
- Risky external, destructive, or expensive actions still require approval.

## Verification

- Run packet-specific checks.
- Run `scripts/verify_workflow.py` on this directory after results are written.
"""


def render_orchestration(plan: WorkflowPlan) -> str:
    phases = "\n".join(f"- {phase}" for phase in plan.phases) or "- Unphased"
    return f"""# Orchestration: {plan.meta["name"]}

## Execution Rules

- Keep immediate blocking work local.
- Delegate bounded packet work only when subagent tools are available and authorized.
- If no subagent runner exists, process packets sequentially and write isolated results.
- Integrate results before final verification.

## Phases

{phases}

## Packet Prompts

See `packets/`.

## Abort Policy

Stop spawning new work, preserve partial results, and mark unfinished packets as skipped.
"""


def render_integration(plan: WorkflowPlan) -> str:
    return f"""# Integration: {plan.meta["name"]}

## Accepted

## Rejected

## Conflicts

## Decisions

## Remaining Risks

## Verification Still Needed
"""


def render_final_report(plan: WorkflowPlan) -> str:
    return f"""# Final Report: {plan.meta["name"]}

## Outcome

## Accepted Results

## Rejected Results

## Conflicts Resolved

## Verification Evidence

## Remaining Risks
"""


def render_state(plan: WorkflowPlan, slug: str) -> dict[str, Any]:
    return {
        "title": plan.meta["name"],
        "slug": slug,
        "status": "planned",
        "source": "codex_workflow.py",
        "approval": {"required": None, "granted": None, "notes": ""},
        "budgets": {"max_concurrent_agents": 4, "max_total_agents": len(plan.agents), "time_minutes": None, "token_budget": None},
        "phases": plan.phases,
        "packets": [
            {
                "id": f"{agent.index:02d}-{slugify(agent.label)}",
                "label": agent.label,
                "phase": agent.phase,
                "status": "pending",
                "assignee": "subagent-or-simulated",
            }
            for agent in plan.agents
        ],
        "verification": {"status": "not_started", "checks": []},
    }


def render_packet(agent: WorkflowAgentCall, packet_id: str) -> str:
    return f"""# Packet {packet_id}: {agent.label}

Packet ID: {packet_id}
Objective: Execute the extracted `agent()` task.
Phase: {agent.phase or "Unphased"}
Ownership: Bounded to this packet prompt.

## Prompt

{agent.prompt}

## Do

- Run only the work needed to answer this prompt.
- Return concise evidence and any verification commands.
- Note blockers or assumptions.

## Do Not

- Revert unrelated edits.
- Perform risky external or destructive actions without approval.
- Expand the task beyond this packet.

## Expected Output

Write `results/{packet_id}.md`.

## Verification

- Packet-specific evidence required.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", help="Path to a Pi-style workflow script")
    parser.add_argument("--json", action="store_true", help="Print parsed workflow metadata as JSON")
    parser.add_argument("--root", help="Create a Codex workflow artifact under this root")
    parser.add_argument("--slug", help="Optional artifact slug")
    parser.add_argument("--force", action="store_true", help="Regenerate an existing workflow artifact")
    args = parser.parse_args(argv)

    try:
        script = Path(args.script).read_text(encoding="utf-8")
        plan = parse_script(script)
        if args.root:
            run_dir = write_artifact(plan, Path(args.root), args.slug, force=args.force)
            print(run_dir)
        elif args.json:
            print(
                json.dumps(
                    {
                        "meta": plan.meta,
                        "phases": plan.phases,
                        "agents": [agent.__dict__ for agent in plan.agents],
                    },
                    indent=2,
                )
            )
        else:
            print(f"Workflow {plan.meta['name']} parsed with {len(plan.agents)} agent(s).")
        return 0
    except Exception as exc:
        print(f"codex_workflow.py: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
