from __future__ import annotations

import re
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


class JustfileTests(unittest.TestCase):
    def test_local_script_references_exist(self) -> None:
        content = JUSTFILE.read_text(encoding="utf-8")
        referenced = sorted(set(LOCAL_SCRIPT_RE.findall(content)))
        missing = [path for path in referenced if not (REPO_ROOT / path).is_file()]

        self.assertGreater(len(referenced), 0, "Expected the justfile to invoke local scripts")
        self.assertEqual(missing, [], f"Missing scripts referenced by justfile: {missing}")

    def test_obsidian_recipes_are_not_advertised_without_scripts(self) -> None:
        content = JUSTFILE.read_text(encoding="utf-8")
        still_present = [path for path in MISSING_OBSIDIAN_SCRIPTS if path in content]
        self.assertEqual(
            still_present,
            [],
            f"justfile still points at scripts that are not in the tree: {still_present}",
        )
        self.assertNotIn("obsidian-import", content)
        self.assertNotIn("obsidian-export", content)
        self.assertNotIn("obsidian-sync", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
