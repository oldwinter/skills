from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
JUSTFILE = REPO_ROOT / "justfile"
LOCAL_SCRIPT_RE = re.compile(r"(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.(?:py|sh)")
MISSING_OBSIDIAN_SCRIPTS = (
    "meta-skills/sync-skills-manager/scripts/import_obsidian_skill_state.py",
    "meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py",
    "meta-skills/sync-skills-manager/scripts/test_export_skills_to_obsidian.py",
    "meta-skills/sync-skills-manager/scripts/test_obsidian_skill_state.py",
)
OBSIDIAN_PLAN = "docs/plans/2026-03-08-obsidian-skill-state-sync.md"


class JustfileTests(unittest.TestCase):
    def test_local_script_references_exist(self) -> None:
        content = JUSTFILE.read_text(encoding="utf-8")
        referenced = sorted(set(LOCAL_SCRIPT_RE.findall(content)))
        missing = [path for path in referenced if not (REPO_ROOT / path).is_file()]
        self.assertGreater(len(referenced), 0)
        self.assertEqual(missing, [], f"justfile still points at missing scripts: {missing}")

    def test_obsidian_recipes_fail_closed_with_plan_try(self) -> None:
        content = JUSTFILE.read_text(encoding="utf-8")
        still_present = [path for path in MISSING_OBSIDIAN_SCRIPTS if path in content]
        self.assertEqual(still_present, [])
        result = subprocess.run(
            ["just", "obsidian-sync"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
        self.assertIn("try: " + OBSIDIAN_PLAN, result.stdout + result.stderr)
        self.assertNotIn("No such file", result.stdout + result.stderr)

    def test_test_sync_recipe_uses_discovery_for_path_based_tests(self) -> None:
        result = subprocess.run(
            ["just", "--dry-run", "test-sync"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        dry_run = result.stdout + result.stderr
        self.assertIn("python3 -m unittest discover", dry_run)
        self.assertNotIn("meta-skills/sync-skills-manager/scripts/test_", dry_run)


if __name__ == "__main__":
    unittest.main(verbosity=2)
