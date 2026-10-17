#!/usr/bin/env python3
"""Dependency-free length counter for long-form fiction manuscripts.

Count rule: every CJK ideograph is one unit; every run of Latin letters or digits is one
word. The default `count` is CJK ideographs plus Latin word tokens, which matches the
character targets used for Chinese manuscripts while staying sane for English text.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LATIN = re.compile(r"[A-Za-z0-9]+(?:['\u2019-][A-Za-z0-9]+)*")
SUFFIXES = {".md", ".markdown", ".txt"}
SKIP_DIRS = {"node_modules", ".git", "__pycache__"}


def count_text(text: str) -> dict[str, int]:
    cjk = len(CJK.findall(text))
    latin = len(LATIN.findall(text))
    return {
        "count": cjk + latin,
        "cjk_chars": cjk,
        "latin_words": latin,
        "non_space_chars": sum(1 for char in text if not char.isspace()),
        "lines": len(text.splitlines()),
    }


def manuscript_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.is_dir():
        raise OSError(f"not a file or directory: {path}")
    return [
        item
        for item in sorted(path.rglob("*"))
        if item.is_file() and item.suffix.lower() in SUFFIXES and not SKIP_DIRS & set(item.parts)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="manuscript files or directories")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    rows: list[dict] = []
    for raw in args.paths:
        try:
            files = manuscript_files(raw)
        except OSError as exc:
            print(f"count_words: {exc}", file=sys.stderr)
            return 2
        for path in files:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                print(f"count_words: cannot read {path}: {exc}", file=sys.stderr)
                return 2
            rows.append({"file": str(path), **count_text(text)})

    if not rows:
        print("count_words: no manuscript files found", file=sys.stderr)
        return 2

    total = {
        key: sum(row[key] for row in rows)
        for key in ("count", "cjk_chars", "latin_words", "non_space_chars")
    }
    total["files"] = len(rows)
    if args.json:
        print(json.dumps({"files": rows, "total": total}, ensure_ascii=False, indent=2))
        return 0

    width = max(len(row["file"]) for row in rows)
    print(f"{'file'.ljust(width)}  {'count':>8}  {'cjk':>8}  {'words':>8}  {'lines':>8}")
    for row in rows:
        print(
            f"{row['file'].ljust(width)}  {row['count']:>8}  {row['cjk_chars']:>8}  "
            f"{row['latin_words']:>8}  {row['lines']:>8}"
        )
    print(
        f"{'TOTAL'.ljust(width)}  {total['count']:>8}  {total['cjk_chars']:>8}  "
        f"{total['latin_words']:>8}  {'':>8}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
