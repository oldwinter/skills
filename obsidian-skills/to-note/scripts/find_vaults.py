#!/usr/bin/env python3
"""Print Obsidian vaults as `source<TAB>path`: every folder that contains a .obsidian directory.

OBSIDIAN_VAULT_ROOT, when it names a vault, is printed alone as `env`. Otherwise, best first:
open (open in Obsidian now), recent (opened before, newest first), found (a shallow search of the
home folder, run only when Obsidian lists no vault). Standard library only.
"""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Iterator
from pathlib import Path

HOME = Path.home()
SKIP = {"Library", "AppData", "node_modules", "Applications", "Music", "Movies", "Pictures"}
DEPTH = 4


def registries() -> list[Path]:
    """Obsidian's own vault list on macOS, Windows, Linux, Flatpak, and Snap."""
    appdata = Path(os.environ.get("APPDATA", HOME / "AppData" / "Roaming"))
    config = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
    return [
        HOME / "Library" / "Application Support" / "obsidian" / "obsidian.json",
        appdata / "obsidian" / "obsidian.json",
        config / "obsidian" / "obsidian.json",
        HOME / ".var" / "app" / "md.obsidian.Obsidian" / "config" / "obsidian" / "obsidian.json",
        HOME / "snap" / "obsidian" / "current" / ".config" / "obsidian" / "obsidian.json",
    ]


def registered() -> Iterator[tuple[str, Path]]:
    for registry in registries():
        try:
            vaults = json.loads(registry.read_text(encoding="utf-8")).get("vaults", {})
        except (OSError, ValueError, AttributeError):
            continue
        entries = [v for v in vaults.values() if isinstance(v, dict) and v.get("path")]
        for vault in sorted(entries, key=lambda v: (not v.get("open"), -float(v.get("ts") or 0))):
            yield ("open" if vault.get("open") else "recent"), Path(vault["path"])


def searched() -> Iterator[tuple[str, Path]]:
    icloud = HOME / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents"
    if icloud.is_dir():
        yield from (("found", child) for child in sorted(icloud.iterdir()))
    for root, dirs, _ in os.walk(HOME):
        here = Path(root)
        if (here / ".obsidian").is_dir():
            yield "found", here
            dirs.clear()
            continue
        depth = len(here.relative_to(HOME).parts)
        dirs[:] = [] if depth >= DEPTH else sorted(
            d for d in dirs if not d.startswith(".") and d not in SKIP
        )


def main() -> int:
    env = Path(os.environ.get("OBSIDIAN_VAULT_ROOT", "")).expanduser()
    if os.environ.get("OBSIDIAN_VAULT_ROOT") and (env / ".obsidian").is_dir():
        print(f"env\t{env.resolve()}")
        return 0
    candidates = list(registered())
    if not any((path / ".obsidian").is_dir() for _, path in candidates):
        candidates += searched()
    seen: set[Path] = set()
    for source, path in candidates:
        path = path.resolve()
        if path not in seen and (path / ".obsidian").is_dir():
            seen.add(path)
            print(f"{source}\t{path}")
    if not seen:
        print("no folder with a .obsidian directory found; ask the user for the vault path", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
