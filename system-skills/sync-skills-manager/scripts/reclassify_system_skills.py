#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from collections import defaultdict
from pathlib import Path


def guess_repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def list_categories(system_root: Path) -> list[str]:
    categories = [
        d.name
        for d in system_root.iterdir()
        if d.is_dir() and d.name.endswith("-skills") and d.name != "sync-skills-manager"
    ]
    return sorted(categories)


def skill_dirs_by_category(system_root: Path, categories: list[str]) -> dict[str, dict[str, Path]]:
    data: dict[str, dict[str, Path]] = {}
    for category in categories:
        cat_dir = system_root / category
        skills: dict[str, Path] = {}
        for entry in sorted(cat_dir.iterdir()):
            if not entry.is_dir():
                continue
            if not (entry / "SKILL.md").is_file():
                continue
            skills[entry.name] = entry
        data[category] = skills
    return data


def classify_skill(skill: str, current: str) -> str:
    if current != "tools-skills":
        return current

    exact: dict[str, str] = {
        "agent-browser": "tools-skills",
        "changelog-generator": "communication-skills",
        "ci-fix": "devops-skills",
        "clickhouse-io": "engineering-skills",
        "cloudflare-deploy": "devops-skills",
        "coding-standards": "engineering-skills",
        "collect-incomplete-tasks": "leadership-skills",
        "configure-ecc": "devops-skills",
        "context7": "ai-skills",
        "continuous-learning": "career-skills",
        "continuous-learning-v2": "career-skills",
        "create-pull-request": "devops-skills",
        "designing-team-rituals": "leadership-skills",
        "docker-kubectl-deploy": "devops-skills",
        "docs-update": "communication-skills",
        "documentation-lookup": "ai-skills",
        "e2e-test-automation": "engineering-skills",
        "eval-harness": "ai-skills",
        "excalidraw-diagram": "obsidian-skills",
        "find-skills": "tools-skills",
        "firecrawl": "ai-skills",
        "gh-address-comments": "devops-skills",
        "gh-fix-ci": "devops-skills",
        "github-bug-report-triage": "devops-skills",
        "github-issue-dedupe": "devops-skills",
        "humanizer": "communication-skills",
        "iterative-retrieval": "ai-skills",
        "justfile": "tools-skills",
        "lenny-skillpack-creator": "tools-skills",
        "linear": "product-skills",
        "linear-cli": "product-skills",
        "marketplace-liquidity-management": "product-skills",
        "mcp-builder": "ai-skills",
        "mdbase": "engineering-skills",
        "openai-docs": "ai-skills",
        "pearcleaner-cli": "tools-skills",
        "playwright": "engineering-skills",
        "positioning-and-messaging": "product-skills",
        "post-mortems-and-retrospectives": "leadership-skills",
        "postgres": "engineering-skills",
        "postgres-patterns": "engineering-skills",
        "project-guidelines-example": "tools-skills",
        "release-skills": "devops-skills",
        "remotion-best-practices": "engineering-skills",
        "research": "product-skills",
        "retention-and-engagement": "product-skills",
        "running-effective-11s": "leadership-skills",
        "scheduler": "obsidian-skills",
        "scoping-and-cutting": "product-skills",
        "security-review": "engineering-skills",
        "seo-aeo-audit": "marketing-skills",
        "seo-geo": "marketing-skills",
        "setting-okrs-and-goals": "leadership-skills",
        "simplex-cli-admin": "devops-skills",
        "skill-creator": "tools-skills",
        "skill-installer": "tools-skills",
        "skill-review": "tools-skills",
        "skills-readme-updater": "tools-skills",
        "slack-qa-investigate": "tools-skills",
        "strategic-compact": "leadership-skills",
        "supabase-postgres-best-practices": "engineering-skills",
        "sync-ci-to-staging": "devops-skills",
        "sync-ci-to-staging-prod": "devops-skills",
        "tasknotes-skill": "obsidian-skills",
        "tdd-workflow": "engineering-skills",
        "template": "tools-skills",
        "terraform-style-check": "devops-skills",
        "ui-ux-pro-max": "engineering-skills",
        "vercel-deploy": "devops-skills",
        "vercel-react-best-practices": "engineering-skills",
        "verification-loop": "engineering-skills",
        "warp-vibe": "tools-skills",
        "web-accessibility-audit": "engineering-skills",
        "web-design-guidelines": "engineering-skills",
        "web-performance-audit": "engineering-skills",
        "webapp-testing": "engineering-skills",
    }
    if skill in exact:
        return exact[skill]

    if skill.startswith("baoyu-"):
        return "marketing-skills"

    code_prefixes = (
        "backend-",
        "frontend-",
        "django-",
        "python-",
        "golang-",
        "java-",
        "springboot-",
    )
    if skill.startswith(code_prefixes):
        return "engineering-skills"

    engineering_suffixes = (
        "-patterns",
        "-testing",
        "-security",
        "-tdd",
        "-verification",
    )
    if skill.endswith(engineering_suffixes):
        return "engineering-skills"

    return current


def plan_moves(
    system_root: Path,
    categories: list[str],
    only_from: set[str],
) -> tuple[list[tuple[str, str, str]], dict[str, dict[str, Path]]]:
    skill_map = skill_dirs_by_category(system_root, categories)
    moves: list[tuple[str, str, str]] = []
    for source_category, skills in skill_map.items():
        if only_from and source_category not in only_from:
            continue
        for skill_name in sorted(skills.keys()):
            target = classify_skill(skill_name, source_category)
            if target != source_category:
                moves.append((skill_name, source_category, target))
    return moves, skill_map


def summarize_counts(skill_map: dict[str, dict[str, Path]]) -> dict[str, int]:
    return {category: len(skills) for category, skills in sorted(skill_map.items())}


def apply_moves(
    system_root: Path,
    moves: list[tuple[str, str, str]],
    skill_map: dict[str, dict[str, Path]],
) -> None:
    for skill_name, source, target in moves:
        src = skill_map[source][skill_name]
        dst_dir = system_root / target
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / skill_name
        if dst.exists():
            raise RuntimeError(f"Target already exists: {dst}")
        shutil.move(str(src), str(dst))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="reclassify_system_skills.py",
        description="Reclassify system-skills directories into more balanced categories.",
    )
    parser.add_argument(
        "--from-category",
        action="append",
        help="Only reclassify from these categories (repeatable, default: tools-skills).",
    )
    parser.add_argument("--apply", action="store_true", help="Apply moves. Default is dry-run.")
    args = parser.parse_args()

    repo_root = guess_repo_root()
    system_root = repo_root / "system-skills"
    categories = list_categories(system_root)
    only_from = set(args.from_category or ["tools-skills"])

    invalid = sorted(only_from - set(categories))
    if invalid:
        raise SystemExit(f"Invalid --from-category values: {', '.join(invalid)}")

    before_map = skill_dirs_by_category(system_root, categories)
    moves, skill_map = plan_moves(system_root, categories, only_from)

    print("reclassify-system-skills")
    print(f"repo_root: {repo_root}")
    print(f"system_root: {system_root}")
    print(f"from_categories: {', '.join(sorted(only_from))}")
    print(f"planned_moves: {len(moves)}")
    print("")
    for skill_name, source, target in moves:
        print(f"- {skill_name}: {source} -> {target}")

    if not args.apply:
        print("")
        print("Dry-run only. Re-run with --apply to make changes.")
        return 0

    apply_moves(system_root, moves, skill_map)
    after_map = skill_dirs_by_category(system_root, categories)
    print("")
    print("Category counts (before -> after):")
    before_counts = summarize_counts(before_map)
    after_counts = summarize_counts(after_map)
    for category in sorted(categories):
        print(f"- {category}: {before_counts.get(category, 0)} -> {after_counts.get(category, 0)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
