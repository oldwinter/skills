#!/usr/bin/env python3
"""Audit this repository's two-layer skill tree against README.md.

Never writes README.md. The public catalog is handwritten.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

BUCKETS = (
    "base-skills",
    "devops-skills",
    "lenny-skills",
    "meta-skills",
    "obsidian-skills",
    "tools-skills",
)
BUCKET_HEADINGS = {
    "base-skills": "Base Skills",
    "devops-skills": "DevOps Skills",
    "lenny-skills": "Lenny Skills",
    "meta-skills": "Meta Skills",
    "obsidian-skills": "Obsidian Skills",
    "tools-skills": "Tools Skills",
}
COLLISIONS = (
    "agent-browser",
    "excalidraw-diagram",
    "find-skills",
    "mermaid-visualizer",
    "remotion-best-practices",
    "skill-creator",
)
SKILL_NAME = r"[A-Za-z0-9][A-Za-z0-9_.-]*"


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def is_skill_dir(path: Path) -> bool:
    return path.is_dir() and (path / "SKILL.md").exists()


def root_skills(repo: Path) -> list[str]:
    names = [
        child.name
        for child in repo.iterdir()
        if is_skill_dir(child) and child.name not in BUCKETS
    ]
    return sorted(names)


def bucket_skills(repo: Path) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for bucket in BUCKETS:
        bucket_dir = repo / bucket
        if not bucket_dir.is_dir():
            continue
        names = sorted({path.parent.name for path in bucket_dir.rglob("SKILL.md")})
        found[bucket] = names
    return found


def all_skill_dirs(repo: Path) -> list[Path]:
    found = [repo / name for name in root_skills(repo)]
    for bucket in BUCKETS:
        bucket_dir = repo / bucket
        if not bucket_dir.is_dir():
            continue
        found.extend(path.parent for path in bucket_dir.rglob("SKILL.md"))
    return found


def heading_section(readme: str, heading: str) -> str | None:
    match = re.search(
        rf"^### {re.escape(heading)}.*?(?=^### |\Z)",
        readme,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(0) if match else None


def standalone_section(readme: str) -> str | None:
    return heading_section(readme, "Standalone Skills")


def listed_skill_names(section: str) -> set[str]:
    names = set(re.findall(rf"\*\*({SKILL_NAME})\*\*", section))
    names.update(re.findall(rf"\[({SKILL_NAME})\]\(", section))
    return names


def parse_stat(readme: str, label: str) -> int | None:
    match = re.search(rf"\*\*{re.escape(label)}\*\*:\s*(\d+)", readme)
    return int(match.group(1)) if match else None


def check(repo: Path) -> list[str]:
    errors: list[str] = []
    readme_path = repo / "README.md"
    if not readme_path.is_file():
        return ["audit-readme: missing README.md"]

    readme = readme_path.read_text(encoding="utf-8")
    standalone = standalone_section(readme)
    if standalone is None:
        errors.append("audit-readme: README missing ### Standalone Skills section")
        standalone = ""

    roots = root_skills(repo)
    listed_standalone = listed_skill_names(standalone)
    for name in roots:
        if name not in listed_standalone:
            errors.append(f"audit-readme: Standalone Skills missing root skill {name}")
    for name in sorted(listed_standalone - set(roots)):
        errors.append(f"audit-readme: Standalone Skills lists unknown {name}")

    buckets = bucket_skills(repo)
    for bucket, heading in BUCKET_HEADINGS.items():
        if bucket not in buckets:
            continue
        tree_names = set(buckets[bucket])
        section = heading_section(readme, heading)
        if section is None:
            errors.append(f"audit-readme: README missing ### {heading} section")
            continue
        listed = listed_skill_names(section)
        for name in sorted(tree_names - listed):
            errors.append(f"audit-readme: {heading} missing {name}")
        for name in sorted(listed - tree_names):
            errors.append(f"audit-readme: {heading} lists unknown {name}")

    for name in COLLISIONS:
        if not re.search(rf"`{re.escape(name)}`", readme):
            errors.append(f"audit-readme: README missing collision mark `{name}`")

    dirs = all_skill_dirs(repo)
    unique = {path.name for path in dirs}
    want_dirs = len(dirs)
    want_unique = len(unique)
    got_dirs = parse_stat(readme, "Skill directories")
    got_unique = parse_stat(readme, "Unique names")
    if got_dirs != want_dirs:
        errors.append(
            "audit-readme: README **Skill directories** is "
            f"{got_dirs!r}, tree has {want_dirs}"
        )
    if got_unique != want_unique:
        errors.append(
            "audit-readme: README **Unique names** is "
            f"{got_unique!r}, tree has {want_unique}"
        )

    counts = Counter(path.name for path in dirs)
    live_collisions = sorted(name for name, n in counts.items() if n > 1)
    if live_collisions != list(COLLISIONS):
        errors.append(
            "audit-readme: live collisions "
            f"{live_collisions} != documented {list(COLLISIONS)}"
        )

    return errors


def print_inventory(repo: Path) -> None:
    roots = root_skills(repo)
    buckets = bucket_skills(repo)
    dirs = all_skill_dirs(repo)
    unique = {path.name for path in dirs}
    print(f"repo: {repo}")
    print(f"root / standalone: {len(roots)}")
    for name in roots:
        print(f"  {name}")
    print("category buckets:")
    for bucket in BUCKETS:
        names = buckets.get(bucket, [])
        print(f"  {bucket}: {len(names)}")
    print(f"skill directories: {len(dirs)}")
    print(f"unique names: {len(unique)}")
    collisions = sorted(
        name for name, n in Counter(path.name for path in dirs).items() if n > 1
    )
    print(f"name collisions: {', '.join(collisions) if collisions else '(none)'}")
    print("README.md is handwritten. This script does not write it.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the repo skill tree against the handwritten README. Never writes README.md."
    )
    parser.add_argument(
        "--repo",
        default=str(repo_root_from_script()),
        help="Repository root (default: this checkout)",
    )
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    print_inventory(repo)
    errors = check(repo)
    if errors:
        print("\nREADME drift:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("README two-layer map matches the repo tree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
