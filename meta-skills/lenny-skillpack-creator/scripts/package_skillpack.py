#!/usr/bin/env python3

"""
package_skillpack.py

Zip a skill pack directory for distribution.
It runs lint_skillpack.py first.

Usage:
  python scripts/package_skillpack.py <path/to/skill-folder> [output-dir]

Example:
  python scripts/package_skillpack.py ./.claude/skills/writing-prds ./dist
"""

from __future__ import annotations
import os
from pathlib import Path
import sys
import zipfile
import subprocess

def run_lint(skill_dir: Path) -> int:
    here = Path(__file__).resolve().parent
    lint = here / "lint_skillpack.py"
    cmd = [sys.executable, str(lint), str(skill_dir)]
    return subprocess.call(cmd)

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: package_skillpack.py <skill-folder> [output-dir]", file=sys.stderr)
        return 2

    skill_dir = Path(sys.argv[1]).expanduser().resolve()
    out_dir = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) >= 3 else skill_dir.parent.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if run_lint(skill_dir) != 0:
        print("[fail] Lint failed; not packaging.", file=sys.stderr)
        return 2

    zip_path = out_dir / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            for fn in files:
                full = Path(root) / fn
                rel = full.relative_to(skill_dir.parent)  # include top-level folder
                zf.write(full, rel.as_posix())

    print(f"[ok] Wrote: {zip_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
