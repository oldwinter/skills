from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("update_readme", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SCRIPTS_DIR = Path(__file__).resolve().parent
update_readme = load_module(SCRIPTS_DIR / "update_readme.py")


def write_skill(path: Path, name: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: demo\n---\n",
        encoding="utf-8",
    )


class UpdateReadmeTests(unittest.TestCase):
    def test_live_readme_matches_tree(self) -> None:
        errors = update_readme.check(update_readme.repo_root_from_script())
        self.assertEqual(errors, [])

    def test_incomplete_readme_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo / "add-just-doctor", "add-just-doctor")
            write_skill(repo / "base-skills" / "context7", "context7")
            (repo / "README.md").write_text(
                "### Other\nnothing\n## Statistics\n- **Total Skills**: 1\n",
                encoding="utf-8",
            )
            errors = update_readme.check(repo)
            joined = "\n".join(errors)
            self.assertTrue(any("Standalone Skills" in e for e in errors), joined)
            self.assertTrue(any("add-just-doctor" in e for e in errors), joined)
            self.assertTrue(any("Skill directories" in e for e in errors), joined)

    def test_matching_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo / "add-just-doctor", "add-just-doctor")
            write_skill(repo / "base-skills" / "context7", "context7")
            for name in (
                "agent-browser",
                "excalidraw-diagram",
                "find-skills",
                "mermaid-visualizer",
                "remotion-best-practices",
                "skill-creator",
            ):
                write_skill(repo / name, name)
                write_skill(repo / "meta-skills" / name, name)
            (repo / "README.md").write_text(
                """### Standalone Skills
- **add-just-doctor** — demo
- **agent-browser** — demo
- **excalidraw-diagram** — demo
- **find-skills** — demo
- **mermaid-visualizer** — demo
- **remotion-best-practices** — demo
- **skill-creator** — demo

Collisions: `agent-browser` `excalidraw-diagram` `find-skills` `mermaid-visualizer` `remotion-best-practices` `skill-creator`

## Statistics
- **Skill directories**: 14
- **Unique names**: 8
""",
                encoding="utf-8",
            )
            self.assertEqual(update_readme.check(repo), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
