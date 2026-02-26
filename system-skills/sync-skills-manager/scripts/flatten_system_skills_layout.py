#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path


IGNORED_FILE_NAMES = {".DS_Store"}


def guess_repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def is_skill_dir(path: Path) -> bool:
    return path.is_dir() and (path / "SKILL.md").is_file()


def list_system_categories(system_root: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in system_root.iterdir()
            if path.is_dir() and path.name.endswith("-skills") and path.name != "sync-skills-manager"
        ]
    )


def list_skills(category_dir: Path) -> list[Path]:
    return sorted([path for path in category_dir.iterdir() if is_skill_dir(path)])


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def skill_tree_fingerprint(skill_dir: Path) -> dict[str, str]:
    fingerprint: dict[str, str] = {}
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name in IGNORED_FILE_NAMES:
            continue
        rel = path.relative_to(skill_dir).as_posix()
        fingerprint[rel] = hash_file(path)
    return fingerprint


@dataclass(frozen=True)
class Action:
    kind: str  # move | duplicate | conflict | agents-move | agents-duplicate | agents-conflict
    category: str
    source: Path
    destination: Path
    reason: str


def plan_actions(repo_root: Path) -> list[Action]:
    system_root = repo_root / "system-skills"
    if not system_root.is_dir():
        raise SystemExit(f"system-skills directory not found: {system_root}")

    actions: list[Action] = []
    for src_category in list_system_categories(system_root):
        category_name = src_category.name
        dst_category = repo_root / category_name

        for src_skill in list_skills(src_category):
            dst_skill = dst_category / src_skill.name
            if not dst_skill.exists():
                actions.append(
                    Action(
                        kind="move",
                        category=category_name,
                        source=src_skill,
                        destination=dst_skill,
                        reason="missing-in-root",
                    )
                )
                continue

            if not is_skill_dir(dst_skill):
                actions.append(
                    Action(
                        kind="conflict",
                        category=category_name,
                        source=src_skill,
                        destination=dst_skill,
                        reason="destination-exists-not-skill",
                    )
                )
                continue

            if skill_tree_fingerprint(src_skill) == skill_tree_fingerprint(dst_skill):
                actions.append(
                    Action(
                        kind="duplicate",
                        category=category_name,
                        source=src_skill,
                        destination=dst_skill,
                        reason="identical-skill",
                    )
                )
            else:
                actions.append(
                    Action(
                        kind="conflict",
                        category=category_name,
                        source=src_skill,
                        destination=dst_skill,
                        reason="different-skill-content",
                    )
                )

        src_agents = src_category / "AGENTS.md"
        dst_agents = dst_category / "AGENTS.md"
        if src_agents.exists():
            if not dst_agents.exists():
                actions.append(
                    Action(
                        kind="agents-move",
                        category=category_name,
                        source=src_agents,
                        destination=dst_agents,
                        reason="missing-agents-in-root",
                    )
                )
            elif src_agents.read_text(encoding="utf-8") == dst_agents.read_text(encoding="utf-8"):
                actions.append(
                    Action(
                        kind="agents-duplicate",
                        category=category_name,
                        source=src_agents,
                        destination=dst_agents,
                        reason="identical-agents",
                    )
                )
            else:
                actions.append(
                    Action(
                        kind="agents-conflict",
                        category=category_name,
                        source=src_agents,
                        destination=dst_agents,
                        reason="different-agents-content",
                    )
                )

    return actions


def apply_actions(actions: list[Action]) -> None:
    for action in actions:
        if action.kind == "move":
            action.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(action.source), str(action.destination))
        elif action.kind == "duplicate":
            shutil.rmtree(action.source)
        elif action.kind == "agents-move":
            action.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(action.source), str(action.destination))
        elif action.kind == "agents-duplicate":
            action.source.unlink(missing_ok=True)


def cleanup_empty_system_categories(repo_root: Path) -> list[Path]:
    removed: list[Path] = []
    system_root = repo_root / "system-skills"
    for category_dir in list_system_categories(system_root):
        remaining = [p for p in category_dir.iterdir() if p.name not in {".DS_Store"}]
        if remaining:
            continue
        category_dir.rmdir()
        removed.append(category_dir)
    return removed


def print_plan(actions: list[Action], repo_root: Path) -> None:
    grouped: dict[str, int] = {
        "move": 0,
        "duplicate": 0,
        "conflict": 0,
        "agents-move": 0,
        "agents-duplicate": 0,
        "agents-conflict": 0,
    }
    for action in actions:
        grouped[action.kind] = grouped.get(action.kind, 0) + 1
        src_rel = action.source.relative_to(repo_root)
        dst_rel = action.destination.relative_to(repo_root)
        print(f"[{action.kind}] {src_rel} -> {dst_rel} ({action.reason})")

    print("")
    print("summary:")
    for key in ("move", "duplicate", "conflict", "agents-move", "agents-duplicate", "agents-conflict"):
        print(f"- {key}: {grouped.get(key, 0)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="flatten_system_skills_layout.py",
        description=(
            "Flatten system-skills/<category>/<skill> into repo-root <category>/<skill>, "
            "while keeping sync-skills-manager under system-skills."
        ),
    )
    parser.add_argument("--apply", action="store_true", help="Apply filesystem changes. Default is dry-run.")
    args = parser.parse_args()

    repo_root = guess_repo_root()
    actions = plan_actions(repo_root)

    print(f"repo_root: {repo_root}")
    print("mode: apply" if args.apply else "mode: dry-run")
    print("")
    print_plan(actions, repo_root)

    if not args.apply:
        print("")
        print("Dry-run only. Re-run with --apply to execute.")
        return 0

    apply_actions(actions)
    removed = cleanup_empty_system_categories(repo_root)
    print("")
    print(f"Removed empty system category dirs: {len(removed)}")
    for path in removed:
        print(f"- {path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
