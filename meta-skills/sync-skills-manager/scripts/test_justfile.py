from __future__ import annotations

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[3]


class JustfileTests(unittest.TestCase):
    def test_test_sync_recipe_uses_discovery_for_path_based_tests(self) -> None:
        result = subprocess.run(
            ["just", "--dry-run", "test-sync"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        dry_run = result.stdout + result.stderr
        self.assertIn("python3 -m unittest discover", dry_run)
        self.assertNotIn("meta-skills/sync-skills-manager/scripts/test_", dry_run)


if __name__ == "__main__":
    unittest.main()
