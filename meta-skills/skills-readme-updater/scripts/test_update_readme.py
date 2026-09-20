from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "update_readme.py"


def load_module():
    spec = importlib.util.spec_from_file_location("update_readme", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load update_readme.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UpdateReadmeTests(unittest.TestCase):
    def test_parse_simple_yaml_quoted_and_plain(self) -> None:
        updater = load_module()
        parsed = updater.parse_simple_yaml('name: demo\ndescription: "hello world"\n')
        self.assertEqual(parsed["name"], "demo")
        self.assertEqual(parsed["description"], "hello world")

    def test_default_is_repo_root_not_claude_home(self) -> None:
        updater = load_module()
        self.assertEqual(updater.REPO_ROOT, SCRIPT.resolve().parents[3])
        self.assertNotEqual(str(updater.REPO_ROOT), str(Path.home() / ".claude" / "skills"))

    def test_audit_fails_when_readme_omits_a_root_skill(self) -> None:
        updater = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "alpha").mkdir()
            (root / "alpha" / "SKILL.md").write_text("---\nname: alpha\ndescription: a\n---\n")
            readme = root / "README.md"
            readme.write_text("# skills\n")
            code = updater.audit_readme(root, readme)
            self.assertEqual(code, 1)

    def test_audit_passes_when_readme_names_root_skills(self) -> None:
        updater = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "alpha").mkdir()
            (root / "alpha" / "SKILL.md").write_text("---\nname: alpha\ndescription: a\n---\n")
            readme = root / "README.md"
            readme.write_text("# skills\n\n- [alpha](alpha/SKILL.md)\n")
            self.assertEqual(updater.audit_readme(root, readme), 0)

    def test_write_is_rejected_with_try_line(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--write"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("error  --write would replace the handwritten two-layer README", result.stderr)
        self.assertIn("try: just audit-readme", result.stderr)

    def test_repo_readme_currently_lists_root_skills(self) -> None:
        updater = load_module()
        self.assertEqual(updater.audit_readme(updater.REPO_ROOT, updater.REPO_ROOT / "README.md"), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
