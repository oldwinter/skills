#!/usr/bin/env python3

"""
init_skillpack.py

Create a new, agent-executable skill pack skeleton.

Usage:
  python scripts/init_skillpack.py <skill-name> --path <output-directory>

Example:
  python scripts/init_skillpack.py writing-prds --path ./.claude/skills
"""

from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import sys

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_name", help="Skill name (slug preferred).")
    parser.add_argument("--path", required=True, help="Output directory where the skill folder will be created.")
    args = parser.parse_args()

    skill = slugify(args.skill_name)
    if not SLUG_RE.match(skill):
        print(f"[error] Invalid skill name after slugify: {skill}", file=sys.stderr)
        return 2

    out_root = Path(args.path).expanduser().resolve()
    skill_dir = out_root / skill
    if skill_dir.exists():
        print(f"[error] Target already exists: {skill_dir}", file=sys.stderr)
        return 2

    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)

    # skillpack.json (package-like metadata for the repo; tools will ignore this file)
    skillpack_json = {
        "schema_version": 1,
        "skill_slug": skill,
        "version": "0.1.0",
        "authors": ["CHANGE_ME"],
        "contributors": [],
        "origin": "original",
    }
    (skill_dir / "skillpack.json").write_text(
        json.dumps(skillpack_json, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # SKILL.md template
    skill_md = f"""---
name: {skill}
description: >
  TODO: When to use this skill + trigger phrases + expected outputs.
---

# TODO: Skill Title

## Outputs
- TODO

## Inputs
- TODO

## Workflow
1) TODO
2) TODO
3) TODO

## Where humans decide
- TODO

## Quality checks
- Use references/RUBRIC.md and references/CHECKLISTS.md

## Boundaries & risks
- TODO

## Reference files
- references/INTAKE.md
- references/WORKFLOW.md
- references/TEMPLATES.md
- references/CHECKLISTS.md
- references/RUBRIC.md
- references/SOURCE_SUMMARY.md
- references/EXAMPLES.md

## Examples
- TODO: 3 positive + 1 negative example
"""

    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # references templates
    (skill_dir / "references" / "INTAKE.md").write_text("# INTAKE\n\n- TODO: Questions to ask when information is missing.\n", encoding="utf-8")
    (skill_dir / "references" / "WORKFLOW.md").write_text("# WORKFLOW\n\n- TODO: Detailed steps + branches + troubleshooting.\n", encoding="utf-8")
    (skill_dir / "references" / "TEMPLATES.md").write_text("# TEMPLATES\n\n- TODO: Copy/paste templates.\n", encoding="utf-8")
    (skill_dir / "references" / "CHECKLISTS.md").write_text("# CHECKLISTS\n\n- TODO: Execution checklist.\n", encoding="utf-8")
    (skill_dir / "references" / "RUBRIC.md").write_text("# RUBRIC\n\n- TODO: Definition of Done + scoring.\n", encoding="utf-8")
    (skill_dir / "references" / "SOURCE_SUMMARY.md").write_text("# SOURCE_SUMMARY\n\n- TODO: Actionable rules distilled from the source.\n", encoding="utf-8")
    (skill_dir / "references" / "EXAMPLES.md").write_text("# EXAMPLES\n\n## Positive examples\n- TODO\n\n## Negative examples\n- TODO\n", encoding="utf-8")

    print(f"[ok] Created skill pack skeleton: {skill_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
