from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("reclassify_system_skills", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RECLASSIFY = load_module(Path(__file__).resolve().parent / "reclassify_system_skills.py")


class ReclassifySystemSkillsTests(unittest.TestCase):
    def test_keeps_non_tools_category(self) -> None:
        self.assertEqual(RECLASSIFY.classify_skill("aws-cli", "devops-skills"), "devops-skills")

    def test_baoyu_goes_marketing(self) -> None:
        self.assertEqual(RECLASSIFY.classify_skill("baoyu-image-gen", "tools-skills"), "marketing-skills")

    def test_framework_patterns_go_engineering(self) -> None:
        self.assertEqual(RECLASSIFY.classify_skill("django-security", "tools-skills"), "engineering-skills")

    def test_engineering_suffix_goes_engineering(self) -> None:
        self.assertEqual(RECLASSIFY.classify_skill("jpa-patterns", "tools-skills"), "engineering-skills")

    def test_known_tool_stays_tools(self) -> None:
        self.assertEqual(RECLASSIFY.classify_skill("skill-creator", "tools-skills"), "tools-skills")


if __name__ == "__main__":
    unittest.main(verbosity=2)
