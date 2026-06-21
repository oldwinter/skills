#!/usr/bin/env python3

"""
batch_init_skillpacks.py

Create skeleton skill packs for a directory of source Lenny SKILL.md files.
This does NOT auto-generate high-quality content; it creates a consistent structure
that you (or an AI agent) can then fill in.

Usage:
  python scripts/batch_init_skillpacks.py <input-dir> --out <output-dir>

Example:
  python scripts/batch_init_skillpacks.py ./lenny-src --out ./.claude/skills
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys
from datetime import date

FRONTMATTER_RE = re.compile(r"^---\s*$")

def parse_name_from_frontmatter(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or not FRONTMATTER_RE.match(lines[0]):
        return None
    end = None
    for i in range(1, len(lines)):
        if FRONTMATTER_RE.match(lines[i]):
            end = i
            break
    if end is None:
        return None
    for line in lines[1:end]:
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return None

def safe_slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s

def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Directory containing source SKILL.md files (recursively).")
    parser.add_argument("--out", required=True, help="Output directory for generated skill pack folders.")
    args = parser.parse_args()

    in_dir = Path(args.input_dir).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    src_files = list(in_dir.rglob("SKILL.md"))
    if not src_files:
        print(f"[error] No SKILL.md found under {in_dir}", file=sys.stderr)
        return 2

    created = 0
    for src in src_files:
        txt = src.read_text(encoding="utf-8", errors="replace")
        name = parse_name_from_frontmatter(txt) or src.parent.name
        slug = safe_slug(name)
        skill_dir = out_dir / slug
        if skill_dir.exists():
            continue
        (skill_dir / "references").mkdir(parents=True, exist_ok=True)
        (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)

        # minimal SKILL.md with pointers back to source
        skill_md = f"""---
name: {slug}
description: >
  TODO: Convert from source skill: {src.name} (from {src.parent}).
  Add trigger phrases + expected outputs.
license: Apache-2.0
metadata:
  version: "0.1.0"
  generated: "{date.today().isoformat()}"
source:
  file: "{src.as_posix()}"
---

# TODO: {slug}

## 目标与输出（Outputs）
- TODO

## 需要的输入（Inputs）
- TODO

## 工作流（Workflow）
1) TODO

## 引用的参考文件（Reference files）
- references/INTAKE.md
- references/WORKFLOW.md
- references/TEMPLATES.md
- references/CHECKLISTS.md
- references/RUBRIC.md
- references/SOURCE_SUMMARY.md
"""
        (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

        write_if_missing(skill_dir / "references" / "INTAKE.md", "# INTAKE\n\n- TODO\n")
        write_if_missing(skill_dir / "references" / "WORKFLOW.md", "# WORKFLOW\n\n- TODO\n")
        write_if_missing(skill_dir / "references" / "TEMPLATES.md", "# TEMPLATES\n\n- TODO\n")
        write_if_missing(skill_dir / "references" / "CHECKLISTS.md", "# CHECKLISTS\n\n- TODO\n")
        write_if_missing(skill_dir / "references" / "RUBRIC.md", "# RUBRIC\n\n- TODO\n")
        write_if_missing(skill_dir / "references" / "SOURCE_SUMMARY.md", "# SOURCE_SUMMARY\n\n- TODO\n")

        created += 1

    print(f"[ok] Created {created} skeleton skill packs under {out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
