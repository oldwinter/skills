#!/usr/bin/env python3
"""Audit this repository's two-layer skill tree against the handwritten README.

Prints the tree and the README drift. Does not write README.md.
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
LENNY_SUBBUCKETS = (
    "leadership-skills",
    "marketing-skills",
    "product-skills",
    "sales-skills",
)


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def is_skill_dir(path: Path) -> bool:
    return path.is_dir() and (path / "SKILL.md").exists()


def scan_tree(repo: Path) -> dict[str, list[str]]:
    tree: dict[str, list[str]] = {"root": []}
    for child in sorted(repo.iterdir(), key=lambda p: p.name):
        if child.name in BUCKETS or child.name.startswith("."):
            continue
        if is_skill_dir(child):
            tree["root"].append(child.name)

    for bucket in BUCKETS:
        bucket_dir = repo / bucket
        names: list[str] = []
        if bucket_dir.is_dir():
            names = sorted(
                path.parent.name
                for path in bucket_dir.rglob("SKILL.md")
            )
        tree[bucket] = names

        if bucket == "lenny-skills":
            for sub in LENNY_SUBBUCKETS:
                sub_dir = bucket_dir / sub
                tree[f"lenny-skills/{sub}"] = (
                    sorted(child.name for child in sub_dir.iterdir() if is_skill_dir(child))
                    if sub_dir.is_dir()
                    else []
                )
            tree["lenny-skills/direct"] = (
                sorted(child.name for child in bucket_dir.iterdir() if is_skill_dir(child))
                if bucket_dir.is_dir()
                else []
            )
    return tree


def skill_paths(repo: Path) -> list[Path]:
    paths = [repo / name for name in scan_tree(repo)["root"]]
    for bucket in BUCKETS:
        bucket_dir = repo / bucket
        if bucket_dir.is_dir():
            paths.extend(path.parent for path in bucket_dir.rglob("SKILL.md"))
    return paths


def readme_skill_names(readme: str) -> set[str]:
    names = set(re.findall(r"\*\*([a-z0-9][a-z0-9-]*)\*\*", readme))
    names.update(re.findall(r"\[([a-z0-9][a-z0-9-]*)\]\([^)]*SKILL\.md\)", readme))
    return names


def collisions(repo: Path) -> dict[str, list[str]]:
    rels = [str(path.relative_to(repo)) for path in skill_paths(repo)]
    counts = Counter(Path(rel).name for rel in rels)
    found: dict[str, list[str]] = {}
    for name, n in counts.items():
        if n > 1:
            found[name] = sorted(rel for rel in rels if Path(rel).name == name)
    return found


def audit(repo: Path) -> dict[str, object]:
    tree = scan_tree(repo)
    readme_path = repo / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    listed = readme_skill_names(readme_text)
    tree_names = set(tree["root"])
    for bucket in BUCKETS:
        tree_names.update(tree[bucket])
    return {
        "tree": tree,
        "collisions": collisions(repo),
        "in_tree_not_readme": sorted(tree_names - listed),
        "in_readme_not_tree": sorted(listed - tree_names),
    }


def render(report: dict[str, object]) -> str:
    lines: list[str] = ["# skills README audit", ""]
    tree = report["tree"]
    assert isinstance(tree, dict)
    for key in ("root", *BUCKETS):
        names = tree[key]
        assert isinstance(names, list)
        lines.append(f"## {key} ({len(names)})")
        for name in names:
            lines.append(f"- {name}")
        lines.append("")
    for sub in LENNY_SUBBUCKETS:
        key = f"lenny-skills/{sub}"
        names = tree[key]
        assert isinstance(names, list)
        lines.append(f"## {key} ({len(names)})")
        for name in names:
            lines.append(f"- {name}")
        lines.append("")
    direct = tree["lenny-skills/direct"]
    assert isinstance(direct, list)
    lines.append(f"## lenny-skills/direct ({len(direct)})")
    for name in direct:
        lines.append(f"- {name}")
    lines.append("")

    found = report["collisions"]
    assert isinstance(found, dict)
    lines.append(f"## collisions ({len(found)})")
    for name in sorted(found):
        lines.append(f"- {name}: {', '.join(found[name])}")
    lines.append("")

    missing = report["in_tree_not_readme"]
    extra = report["in_readme_not_tree"]
    assert isinstance(missing, list)
    assert isinstance(extra, list)
    lines.append(f"## in tree, not in README ({len(missing)})")
    for name in missing:
        lines.append(f"- {name}")
    lines.append("")
    lines.append(f"## in README, not in tree ({len(extra)})")
    for name in extra:
        lines.append(f"- {name}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the repo skill tree against README.md. Never writes README.md."
    )
    parser.add_argument(
        "--repo",
        default=str(repo_root_from_script()),
        help="Repository root (defaults to this skills checkout)",
    )
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    print(render(audit(repo)), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
