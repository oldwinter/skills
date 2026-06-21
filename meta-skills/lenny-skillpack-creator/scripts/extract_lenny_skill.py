#!/usr/bin/env python3

"""
extract_lenny_skill.py

Extract a structured JSON summary from a Lenny/Refound SKILL.md file.

Usage:
  python scripts/extract_lenny_skill.py <path/to/SKILL.md> [output.json]

The parser is heuristic (best-effort) and optimized for Refound/Lenny's SKILL.md style.
"""

from __future__ import annotations
import json
from pathlib import Path
import re
import sys

FRONTMATTER_RE = re.compile(r"^---\s*$")

def parse_frontmatter(lines: list[str]) -> tuple[dict, int]:
    if not lines or not FRONTMATTER_RE.match(lines[0]):
        return {}, 0
    end = None
    for i in range(1, len(lines)):
        if FRONTMATTER_RE.match(lines[i]):
            end = i
            break
    if end is None:
        return {}, 0
    fm = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm, end + 1

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: extract_lenny_skill.py <SKILL.md> [output.json]", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).expanduser().resolve()
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    fm, idx = parse_frontmatter(lines)
    body = "\n".join(lines[idx:])

    title = None
    m = re.search(r"^#\s+(.+)$", body, flags=re.M)
    if m:
        title = m.group(1).strip()

    covers = []
    m = re.search(r"^##\s+What This Covers\s*(.+?)(\n##\s+|\Z)", body, flags=re.S | re.M)
    if m:
        block = m.group(1)
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("- "):
                covers.append(line[2:].strip())

    insights = []
    # Split by "### From "
    parts = re.split(r"^###\s+From\s+", body, flags=re.M)
    for p in parts[1:]:
        # guest name until newline
        first_line, *rest = p.splitlines()
        guest = first_line.strip()
        chunk = "\n".join(rest)
        key = None
        km = re.search(r"\*\*Key insight:\*\*\s*(.+)", chunk)
        if km:
            key = km.group(1).strip()
        apply = []
        am = re.search(r"\*\*Apply this by:\*\*\s*(.+?)(\n###\s+From\s+|\n##\s+|\Z)", chunk, flags=re.S | re.M)
        if am:
            ablock = am.group(1)
            for line in ablock.splitlines():
                line = line.strip()
                if line.startswith("- "):
                    apply.append(line[2:].strip())
        if guest:
            insights.append({"guest": guest, "key_insight": key, "apply": apply})

    out = {
        "frontmatter": fm,
        "title": title,
        "covers": covers,
        "top_insights": insights,
        "source_path": str(path),
    }

    out_json = json.dumps(out, ensure_ascii=False, indent=2)
    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2]).expanduser().resolve()
        out_path.write_text(out_json, encoding="utf-8")
        print(f"[ok] Wrote {out_path}")
    else:
        print(out_json)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
