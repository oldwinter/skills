from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("flatten_system_skills_layout", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


FLATTEN = load_module(Path(__file__).resolve().parent / "flatten_system_skills_layout.py")


def _write_skill(path: Path, content: str, extra: dict[str, str] | None = None) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(content, encoding="utf-8")
    for rel, text in (extra or {}).items():
        file_path = path / rel
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(text, encoding="utf-8")


class FlattenSystemSkillsLayoutTests(unittest.TestCase):
    def test_move_when_root_skill_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            _write_skill(repo_root / "system-skills" / "ai-skills" / "context7", "a")

            actions = FLATTEN.plan_actions(repo_root)
            kinds = {(a.kind, a.source.name, a.destination.parent.name) for a in actions}

            self.assertIn(("move", "context7", "ai-skills"), kinds)

    def test_duplicate_when_same_skill_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            _write_skill(
                repo_root / "system-skills" / "devops-skills" / "kubectl",
                "same",
                {"references/a.md": "x"},
            )
            _write_skill(
                repo_root / "devops-skills" / "kubectl",
                "same",
                {"references/a.md": "x"},
            )

            actions = FLATTEN.plan_actions(repo_root)
            kinds = {(a.kind, a.source.name) for a in actions}

            self.assertIn(("duplicate", "kubectl"), kinds)

    def test_conflict_when_skill_content_differs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            _write_skill(repo_root / "system-skills" / "obsidian-skills" / "tasknotes", "v1")
            _write_skill(repo_root / "obsidian-skills" / "tasknotes", "v2")

            actions = FLATTEN.plan_actions(repo_root)
            kinds = {(a.kind, a.source.name) for a in actions}

            self.assertIn(("conflict", "tasknotes"), kinds)

    def test_agents_move_when_root_agents_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            category = repo_root / "system-skills" / "marketing-skills"
            category.mkdir(parents=True, exist_ok=True)
            (category / "AGENTS.md").write_text("marketing", encoding="utf-8")

            actions = FLATTEN.plan_actions(repo_root)
            kinds = {(a.kind, a.source.name, a.destination.parent.name) for a in actions}

            self.assertIn(("agents-move", "AGENTS.md", "marketing-skills"), kinds)


if __name__ == "__main__":
    unittest.main()
