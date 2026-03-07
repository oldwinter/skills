from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import sys


SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from obsidian_skill_state import (
    DEFAULT_NOTES_DIR,
    DEFAULT_STATE_PATH,
    extract_state_from_note,
    is_meaningful_state,
    write_state_file,
)
from export_skills_to_obsidian import discover_skills


@dataclass(frozen=True)
class ImportSummary:
    imported_notes: int
    state_entries: int
    state_path: Path


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def import_obsidian_state(
    vault_root: Path,
    notes_dir: Path = DEFAULT_NOTES_DIR,
    state_path: Path | None = None,
    repo_root: Path | None = None,
    dry_run: bool = False,
) -> ImportSummary:
    notes_root = vault_root / notes_dir
    resolved_repo_root = repo_root or repo_root_from_script()
    target_state_path = state_path or (resolved_repo_root / DEFAULT_STATE_PATH)
    repo_skill_ids = {skill.skill_id for skill in discover_skills(resolved_repo_root)}

    entries = {}
    imported_notes = 0

    for note_path in sorted(notes_root.glob("*.md")):
        skill_id, entry = extract_state_from_note(note_path)
        if not skill_id:
            continue
        if skill_id not in repo_skill_ids:
            continue
        imported_notes += 1
        if is_meaningful_state(entry):
            entries[skill_id] = entry

    if not dry_run:
        write_state_file(target_state_path, entries, generated_at=date.today().isoformat())

    return ImportSummary(
        imported_notes=imported_notes,
        state_entries=len(entries),
        state_path=target_state_path,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import personal skill state from Obsidian notes into a repo sidecar.")
    parser.add_argument(
        "--vault-root",
        type=Path,
        required=True,
        help="Obsidian vault root.",
    )
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=DEFAULT_NOTES_DIR,
        help='Relative path inside the vault for skill notes. Default: "Atlas/Skills".',
    )
    parser.add_argument(
        "--state-path",
        type=Path,
        default=repo_root_from_script() / DEFAULT_STATE_PATH,
        help="Target sidecar file path in the repository.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=repo_root_from_script(),
        help="Skills repository root used to filter valid skill ids.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show summary without writing the sidecar file.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    summary = import_obsidian_state(
        vault_root=args.vault_root,
        notes_dir=args.notes_dir,
        state_path=args.state_path,
        repo_root=args.repo_root,
        dry_run=args.dry_run,
    )

    action = "Would import" if args.dry_run else "Imported"
    print(
        f"{action} {summary.imported_notes} Obsidian skill notes -> {summary.state_path} "
        f"(meaningful entries={summary.state_entries})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
