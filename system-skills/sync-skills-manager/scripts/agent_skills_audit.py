#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


def eprint(*parts: object) -> None:
    print(*parts, file=sys.stderr)


def die(message: str, exit_code: int = 1) -> None:
    eprint(f"[ERROR] {message}")
    raise SystemExit(exit_code)


@dataclass(frozen=True)
class AgentSpec:
    agent: str
    label: str
    global_path: str
    cli_commands: tuple[str, ...]


@dataclass(frozen=True)
class SkillsDirSnapshot:
    skills: set[str]
    symlink_count: int
    copy_count: int
    unmanaged_count: int


@dataclass(frozen=True)
class AgentState:
    agent: str
    label: str
    global_path: Path
    cli_found: str | None
    path_exists: bool
    is_dir: bool
    installed: bool
    skills: list[str]
    symlink_count: int
    copy_count: int
    unmanaged_count: int


@dataclass(frozen=True)
class SkillsDiff:
    left: str
    right: str
    left_count: int
    right_count: int
    common_count: int
    only_left: list[str]
    only_right: list[str]
    equal: bool


@dataclass(frozen=True)
class SyncCheck:
    canonical: str
    agent: str
    canonical_count: int
    agent_count: int
    missing_in_agent: list[str]
    extra_in_agent: list[str]
    in_sync: bool


AGENT_SPECS: tuple[AgentSpec, ...] = (
    AgentSpec("amp", "Amp", "~/.config/agents/skills", ("amp",)),
    AgentSpec("kimi-cli", "Kimi Code CLI", "~/.config/agents/skills", ("kimi-cli", "kimi")),
    AgentSpec("replit", "Replit", "~/.config/agents/skills", ("replit",)),
    AgentSpec("universal", "Universal", "~/.config/agents/skills", ("universal",)),
    AgentSpec("antigravity", "Antigravity", "~/.gemini/antigravity/skills", ("antigravity",)),
    AgentSpec("augment", "Augment", "~/.augment/skills", ("augment",)),
    AgentSpec("claude-code", "Claude Code", "~/.claude/skills", ("claude", "claude-code")),
    AgentSpec("openclaw", "OpenClaw", "~/.openclaw/skills", ("openclaw",)),
    AgentSpec("cline", "Cline", "~/.cline/skills", ("cline",)),
    AgentSpec("codebuddy", "CodeBuddy", "~/.codebuddy/skills", ("codebuddy",)),
    AgentSpec("codex", "Codex", "~/.codex/skills", ("codex",)),
    AgentSpec("command-code", "Command Code", "~/.commandcode/skills", ("command-code", "commandcode")),
    AgentSpec("continue", "Continue", "~/.continue/skills", ("continue",)),
    AgentSpec("cortex", "Cortex Code", "~/.snowflake/cortex/skills", ("cortex", "cortex-code")),
    AgentSpec("crush", "Crush", "~/.config/crush/skills", ("crush",)),
    AgentSpec("cursor", "Cursor", "~/.cursor/skills", ("cursor",)),
    AgentSpec("droid", "Droid", "~/.factory/skills", ("droid",)),
    AgentSpec("gemini-cli", "Gemini CLI", "~/.gemini/skills", ("gemini-cli", "gemini")),
    AgentSpec("github-copilot", "GitHub Copilot", "~/.copilot/skills", ("github-copilot", "copilot")),
    AgentSpec("goose", "Goose", "~/.config/goose/skills", ("goose",)),
    AgentSpec("junie", "Junie", "~/.junie/skills", ("junie",)),
    AgentSpec("iflow-cli", "iFlow CLI", "~/.iflow/skills", ("iflow-cli", "iflow")),
    AgentSpec("kilo", "Kilo Code", "~/.kilocode/skills", ("kilo", "kilocode")),
    AgentSpec("kiro-cli", "Kiro CLI", "~/.kiro/skills", ("kiro-cli", "kiro")),
    AgentSpec("kode", "Kode", "~/.kode/skills", ("kode",)),
    AgentSpec("mcpjam", "MCPJam", "~/.mcpjam/skills", ("mcpjam",)),
    AgentSpec("mistral-vibe", "Mistral Vibe", "~/.vibe/skills", ("mistral-vibe", "vibe")),
    AgentSpec("mux", "Mux", "~/.mux/skills", ("mux",)),
    AgentSpec("opencode", "OpenCode", "~/.config/opencode/skills", ("opencode",)),
    AgentSpec("openhands", "OpenHands", "~/.openhands/skills", ("openhands",)),
    AgentSpec("pi", "Pi", "~/.pi/agent/skills", ("pi",)),
    AgentSpec("qoder", "Qoder", "~/.qoder/skills", ("qoder",)),
    AgentSpec("qwen-code", "Qwen Code", "~/.qwen/skills", ("qwen-code", "qwen")),
    AgentSpec("roo", "Roo Code", "~/.roo/skills", ("roo",)),
    AgentSpec("trae", "Trae", "~/.trae/skills", ("trae",)),
    AgentSpec("trae-cn", "Trae CN", "~/.trae-cn/skills", ("trae-cn",)),
    AgentSpec("windsurf", "Windsurf", "~/.codeium/windsurf/skills", ("windsurf",)),
    AgentSpec("zencoder", "Zencoder", "~/.zencoder/skills", ("zencoder",)),
    AgentSpec("neovate", "Neovate", "~/.neovate/skills", ("neovate",)),
    AgentSpec("pochi", "Pochi", "~/.pochi/skills", ("pochi",)),
    AgentSpec("adal", "AdaL", "~/.adal/skills", ("adal",)),
)

AGENT_INDEX: dict[str, AgentSpec] = {spec.agent: spec for spec in AGENT_SPECS}


def normalize_agent_args(raw_values: list[str] | None) -> list[str]:
    names: list[str] = []
    for raw in raw_values or []:
        for part in raw.split(","):
            name = part.strip()
            if name:
                names.append(name)
    return names


def resolve_specs(raw_values: list[str] | None) -> list[AgentSpec]:
    names = normalize_agent_args(raw_values)
    if not names:
        return list(AGENT_SPECS)

    resolved: list[AgentSpec] = []
    seen: set[str] = set()
    unknown: list[str] = []
    for name in names:
        spec = AGENT_INDEX.get(name)
        if spec is None:
            unknown.append(name)
            continue
        if spec.agent in seen:
            continue
        seen.add(spec.agent)
        resolved.append(spec)

    if unknown:
        die(
            "Unknown agent(s): "
            + ", ".join(sorted(set(unknown)))
            + ". Valid values: "
            + ", ".join(spec.agent for spec in AGENT_SPECS)
        )
    return resolved


def scan_skills_dir(global_path: Path) -> SkillsDirSnapshot:
    if not global_path.exists() or not global_path.is_dir():
        return SkillsDirSnapshot(skills=set(), symlink_count=0, copy_count=0, unmanaged_count=0)

    skills: set[str] = set()
    symlink_count = 0
    copy_count = 0
    unmanaged_count = 0

    for entry in global_path.iterdir():
        if not (entry.is_dir() or entry.is_symlink()):
            continue
        try:
            has_skill_md = (entry / "SKILL.md").is_file()
        except OSError:
            has_skill_md = False
        if not has_skill_md:
            unmanaged_count += 1
            continue

        skills.add(entry.name)
        if entry.is_symlink():
            symlink_count += 1
        else:
            copy_count += 1

    return SkillsDirSnapshot(
        skills=skills,
        symlink_count=symlink_count,
        copy_count=copy_count,
        unmanaged_count=unmanaged_count,
    )


def find_cli(spec: AgentSpec) -> str | None:
    for cmd in spec.cli_commands:
        found = shutil.which(cmd)
        if found:
            return found
    return None


def inspect_agent(spec: AgentSpec) -> AgentState:
    global_path = Path(spec.global_path).expanduser()
    snapshot = scan_skills_dir(global_path)
    cli_found = find_cli(spec)
    path_exists = global_path.exists()
    is_dir = global_path.is_dir()
    installed = path_exists or cli_found is not None
    return AgentState(
        agent=spec.agent,
        label=spec.label,
        global_path=global_path,
        cli_found=cli_found,
        path_exists=path_exists,
        is_dir=is_dir,
        installed=installed,
        skills=sorted(snapshot.skills),
        symlink_count=snapshot.symlink_count,
        copy_count=snapshot.copy_count,
        unmanaged_count=snapshot.unmanaged_count,
    )


def inspect_agents(specs: list[AgentSpec]) -> list[AgentState]:
    return [inspect_agent(spec) for spec in specs]


def diff_skill_sets(left: AgentState, right: AgentState) -> SkillsDiff:
    left_skills = set(left.skills)
    right_skills = set(right.skills)
    only_left = sorted(left_skills - right_skills)
    only_right = sorted(right_skills - left_skills)
    common_count = len(left_skills & right_skills)
    return SkillsDiff(
        left=left.agent,
        right=right.agent,
        left_count=len(left_skills),
        right_count=len(right_skills),
        common_count=common_count,
        only_left=only_left,
        only_right=only_right,
        equal=not only_left and not only_right,
    )


def check_sync_with_canonical(canonical: AgentState, target: AgentState) -> SyncCheck:
    canonical_skills = set(canonical.skills)
    target_skills = set(target.skills)
    missing_in_agent = sorted(canonical_skills - target_skills)
    extra_in_agent = sorted(target_skills - canonical_skills)
    return SyncCheck(
        canonical=canonical.agent,
        agent=target.agent,
        canonical_count=len(canonical_skills),
        agent_count=len(target_skills),
        missing_in_agent=missing_in_agent,
        extra_in_agent=extra_in_agent,
        in_sync=not missing_in_agent and not extra_in_agent,
    )


def trim_items(items: list[str], limit: int) -> tuple[list[str], int]:
    if limit <= 0 or len(items) <= limit:
        return items, 0
    return items[:limit], len(items) - limit


def print_scan(states: list[AgentState], with_skills: bool, skill_limit: int) -> None:
    print("agent-skills-audit scan")
    print("----------------------------------------------------------------")
    for state in states:
        cli_text = state.cli_found if state.cli_found else "-"
        print(
            f"[{state.agent}] installed={'yes' if state.installed else 'no'} "
            f"cli={cli_text} path={'yes' if state.path_exists else 'no'} "
            f"skills={len(state.skills)} links={state.symlink_count} copies={state.copy_count} "
            f"unmanaged={state.unmanaged_count}"
        )
        print(f"  global_path: {state.global_path}")
        if with_skills:
            preview, remaining = trim_items(state.skills, skill_limit)
            if preview:
                print("  skills: " + ", ".join(preview) + (f" ... (+{remaining})" if remaining else ""))
            else:
                print("  skills: (none)")
    print("")


def print_skills(states: list[AgentState]) -> None:
    print("agent-skills-audit skills")
    print("----------------------------------------------------------------")
    for state in states:
        print(f"[{state.agent}] skills={len(state.skills)}")
        print(f"  global_path: {state.global_path}")
        for skill in state.skills:
            print(f"  - {skill}")
        if not state.skills:
            print("  - (none)")
    print("")


def print_diffs(diffs: list[SkillsDiff], limit: int) -> None:
    print("agent-skills-audit diff")
    print("----------------------------------------------------------------")
    for diff in diffs:
        print(
            f"[{diff.left} vs {diff.right}] "
            f"equal={'yes' if diff.equal else 'no'} "
            f"left={diff.left_count} right={diff.right_count} common={diff.common_count}"
        )
        left_items, left_remaining = trim_items(diff.only_left, limit)
        right_items, right_remaining = trim_items(diff.only_right, limit)
        print(
            "  only_left: "
            + (", ".join(left_items) if left_items else "(none)")
            + (f" ... (+{left_remaining})" if left_remaining else "")
        )
        print(
            "  only_right: "
            + (", ".join(right_items) if right_items else "(none)")
            + (f" ... (+{right_remaining})" if right_remaining else "")
        )
    print("")


def print_sync_checks(checks: list[SyncCheck], limit: int) -> None:
    print("agent-skills-audit sync-check")
    print("----------------------------------------------------------------")
    for check in checks:
        print(
            f"[{check.agent} <- {check.canonical}] "
            f"in_sync={'yes' if check.in_sync else 'no'} "
            f"canonical={check.canonical_count} agent={check.agent_count} "
            f"missing={len(check.missing_in_agent)} extra={len(check.extra_in_agent)}"
        )
        missing_items, missing_remaining = trim_items(check.missing_in_agent, limit)
        extra_items, extra_remaining = trim_items(check.extra_in_agent, limit)
        print(
            "  missing_in_agent: "
            + (", ".join(missing_items) if missing_items else "(none)")
            + (f" ... (+{missing_remaining})" if missing_remaining else "")
        )
        print(
            "  extra_in_agent: "
            + (", ".join(extra_items) if extra_items else "(none)")
            + (f" ... (+{extra_remaining})" if extra_remaining else "")
        )
    print("")


def as_scan_json(states: list[AgentState], include_skills: bool) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for state in states:
        item: dict[str, object] = {
            "agent": state.agent,
            "label": state.label,
            "installed": state.installed,
            "global_path": str(state.global_path),
            "path_exists": state.path_exists,
            "is_dir": state.is_dir,
            "cli_found": state.cli_found,
            "skills_count": len(state.skills),
            "symlink_count": state.symlink_count,
            "copy_count": state.copy_count,
            "unmanaged_count": state.unmanaged_count,
        }
        if include_skills:
            item["skills"] = state.skills
        out.append(item)
    return out


def as_diff_json(diffs: list[SkillsDiff]) -> list[dict[str, object]]:
    return [
        {
            "left": diff.left,
            "right": diff.right,
            "left_count": diff.left_count,
            "right_count": diff.right_count,
            "common_count": diff.common_count,
            "equal": diff.equal,
            "only_left": diff.only_left,
            "only_right": diff.only_right,
        }
        for diff in diffs
    ]


def as_sync_check_json(checks: list[SyncCheck]) -> list[dict[str, object]]:
    return [
        {
            "canonical": check.canonical,
            "agent": check.agent,
            "canonical_count": check.canonical_count,
            "agent_count": check.agent_count,
            "missing_count": len(check.missing_in_agent),
            "extra_count": len(check.extra_in_agent),
            "in_sync": check.in_sync,
            "missing_in_agent": check.missing_in_agent,
            "extra_in_agent": check.extra_in_agent,
        }
        for check in checks
    ]


def cmd_scan(args: argparse.Namespace) -> int:
    states = inspect_agents(resolve_specs(args.agent))
    if args.installed_only:
        states = [state for state in states if state.installed]

    if args.json:
        print(json.dumps(as_scan_json(states, include_skills=args.with_skills), ensure_ascii=False, indent=2))
        return 0

    print_scan(states, with_skills=args.with_skills, skill_limit=args.skill_limit)
    return 0


def cmd_skills(args: argparse.Namespace) -> int:
    states = inspect_agents(resolve_specs(args.agent))
    if args.installed_only:
        states = [state for state in states if state.installed]

    if args.json:
        print(json.dumps(as_scan_json(states, include_skills=True), ensure_ascii=False, indent=2))
        return 0

    print_skills(states)
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    left_spec = resolve_specs([args.left])[0]
    right_specs = resolve_specs(args.right)
    right_specs = [spec for spec in right_specs if spec.agent != left_spec.agent]
    if not right_specs:
        die("No valid --right target after filtering duplicates.")

    inspected = inspect_agents([left_spec] + right_specs)
    states = {state.agent: state for state in inspected}
    left_state = states[left_spec.agent]
    diffs = [diff_skill_sets(left_state, states[spec.agent]) for spec in right_specs]

    if args.json:
        print(json.dumps(as_diff_json(diffs), ensure_ascii=False, indent=2))
        return 0

    print_diffs(diffs, limit=args.limit)
    return 0


def cmd_sync_check(args: argparse.Namespace) -> int:
    canonical_spec = resolve_specs([args.canonical_agent])[0]
    target_specs = resolve_specs(args.agent)
    target_specs = [spec for spec in target_specs if spec.agent != canonical_spec.agent]
    if not target_specs:
        die("No target agents to compare (after excluding canonical agent).")

    inspected = inspect_agents([canonical_spec] + target_specs)
    state_by_agent = {state.agent: state for state in inspected}
    canonical_state = state_by_agent[canonical_spec.agent]
    if not canonical_state.path_exists or not canonical_state.is_dir:
        die(f"Canonical path unavailable: {canonical_state.global_path}")

    checks = [check_sync_with_canonical(canonical_state, state_by_agent[spec.agent]) for spec in target_specs]
    if args.installed_only:
        checks = [check for check in checks if state_by_agent[check.agent].installed]

    if args.json:
        print(json.dumps(as_sync_check_json(checks), ensure_ascii=False, indent=2))
        return 0

    print_sync_checks(checks, limit=args.limit)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent_skills_audit.py",
        description="Inspect installed agent skills directories and diff skill sets between agents.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="Scan supported agents and show installation/skills summary.")
    p_scan.add_argument("--agent", action="append", help="Agent ids (repeatable or comma-separated).")
    p_scan.add_argument("--installed-only", action="store_true", help="Show only detected installed agents.")
    p_scan.add_argument("--with-skills", action="store_true", help="Include skills preview in text output/json.")
    p_scan.add_argument("--skill-limit", type=int, default=20, help="Max skills shown per agent for preview (0 = all).")
    p_scan.add_argument("--json", action="store_true", help="Output JSON.")

    p_skills = sub.add_parser("skills", help="List skills recognized by selected agents.")
    p_skills.add_argument("--agent", action="append", help="Agent ids (repeatable or comma-separated).")
    p_skills.add_argument("--installed-only", action="store_true", help="Show only detected installed agents.")
    p_skills.add_argument("--json", action="store_true", help="Output JSON.")

    p_diff = sub.add_parser("diff", help="Diff skills between a left agent and one or more right agents.")
    p_diff.add_argument("--left", required=True, help="Baseline agent id.")
    p_diff.add_argument("--right", action="append", required=True, help="Target agent ids (repeatable or comma-separated).")
    p_diff.add_argument("--limit", type=int, default=100, help="Max items shown for only_left/only_right (0 = all).")
    p_diff.add_argument("--json", action="store_true", help="Output JSON.")

    p_sync_check = sub.add_parser(
        "sync-check",
        help="Compare selected agents against a canonical agent to detect missing/extra skills.",
    )
    p_sync_check.add_argument(
        "--canonical-agent",
        default="claude-code",
        help="Canonical baseline agent id (default: claude-code).",
    )
    p_sync_check.add_argument("--agent", action="append", help="Target agent ids (repeatable or comma-separated).")
    p_sync_check.add_argument("--installed-only", action="store_true", help="Compare only installed target agents.")
    p_sync_check.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Max items shown for missing/extra lists (0 = all).",
    )
    p_sync_check.add_argument("--json", action="store_true", help="Output JSON.")

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "scan":
        return cmd_scan(args)
    if args.cmd == "skills":
        return cmd_skills(args)
    if args.cmd == "diff":
        return cmd_diff(args)
    if args.cmd == "sync-check":
        return cmd_sync_check(args)

    die(f"Unknown command: {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
