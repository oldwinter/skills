from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


HAS_YAML = importlib.util.find_spec("yaml") is not None

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATORS = {
    "meta-skills": "meta-skills/skill-creator/scripts/quick_validate.py",
    "root": "skill-creator/scripts/quick_validate.py",
}
MODULES = (
    {name: load_module(f"quick_validate_{name}", REPO_ROOT / rel) for name, rel in VALIDATORS.items()}
    if HAS_YAML
    else {}
)


def _write_skill(dir_path: Path, frontmatter: str) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n\nBody.\n", encoding="utf-8")


@unittest.skipIf(not HAS_YAML, "requires PyYAML")
class QuickValidateTests(unittest.TestCase):
    def validate(self, frontmatter: str, validator: str) -> tuple[bool, str]:
        with TemporaryDirectory() as td:
            skill_dir = Path(td) / "skill"
            _write_skill(skill_dir, frontmatter)
            return MODULES[validator].validate_skill(skill_dir)

    def assert_valid(self, frontmatter: str) -> None:
        for validator in VALIDATORS:
            with self.subTest(validator=validator):
                valid, message = self.validate(frontmatter, validator)
                self.assertTrue(valid, message)

    def assert_invalid(self, frontmatter: str) -> None:
        for validator in VALIDATORS:
            with self.subTest(validator=validator):
                valid, _ = self.validate(frontmatter, validator)
                self.assertFalse(valid)

    def test_minimal_frontmatter_passes(self):
        self.assert_valid("name: ok-skill\ndescription: does a thing")

    def test_spec_optional_fields_pass(self):
        self.assert_valid(
            "name: ok-skill\n"
            "description: does a thing\n"
            "license: MIT\n"
            "compatibility: Requires git in PATH\n"
            "allowed-tools: Bash(git:*)\n"
            "metadata:\n  version: 1.0.0"
        )

    def test_agent_behavioral_keys_pass(self):
        for key_line in [
            'argument-hint: "hint"',
            "disable-model-invocation: true",
            "user-invocable: true",
            "hidden: true",
            "hooks:\n  PreToolUse:\n    - matcher: Write\n      hooks:\n        - type: command\n          command: echo hi",
        ]:
            with self.subTest(key=key_line):
                self.assert_valid(f"name: ok-skill\ndescription: does a thing\n{key_line}")

    def test_informational_keys_belong_under_metadata(self):
        self.assert_invalid("name: ok-skill\ndescription: does a thing\nversion: 1.0.0")
        self.assert_valid("name: ok-skill\ndescription: does a thing\nmetadata:\n  version: 1.0.0")

    def test_unknown_key_fails(self):
        self.assert_invalid("name: ok-skill\ndescription: does a thing\nbogus-key: x")

    def test_missing_name_fails(self):
        self.assert_invalid("description: does a thing")


if __name__ == "__main__":
    unittest.main()
