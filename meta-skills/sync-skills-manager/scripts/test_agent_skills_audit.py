from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("agent_skills_audit", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AGENT_AUDIT = load_module(Path(__file__).resolve().parent / "agent_skills_audit.py")


def _write_skill(dir_path: Path) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\n", encoding="utf-8")


class AgentSkillsAuditTests(unittest.TestCase):
    def test_normalize_agent_args(self) -> None:
        got = AGENT_AUDIT.normalize_agent_args(["codex,cursor", " amp ", "", "gemini-cli"])
        self.assertEqual(got, ["codex", "cursor", "amp", "gemini-cli"])

    def test_resolve_specs_unknown_agent(self) -> None:
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit):
                AGENT_AUDIT.resolve_specs(["unknown-agent"])

    def test_scan_skills_dir_counts(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            skills_root = root / "skills"
            source_root = root / "source"

            _write_skill(skills_root / "skill-a")
            _write_skill(source_root / "skill-b")
            skills_root.mkdir(parents=True, exist_ok=True)
            os.symlink(str(source_root / "skill-b"), str(skills_root / "skill-b"))

            (skills_root / "not-a-skill").mkdir(parents=True, exist_ok=True)
            (skills_root / "README.txt").write_text("x", encoding="utf-8")

            snapshot = AGENT_AUDIT.scan_skills_dir(skills_root)
            self.assertEqual(snapshot.skills, {"skill-a", "skill-b"})
            self.assertEqual(snapshot.symlink_count, 1)
            self.assertEqual(snapshot.copy_count, 1)
            self.assertEqual(snapshot.unmanaged_count, 1)

    def test_diff_skill_sets(self) -> None:
        left = AGENT_AUDIT.AgentState(
            agent="codex",
            label="Codex",
            global_path=Path("/tmp/codex"),
            cli_found=None,
            path_exists=True,
            is_dir=True,
            installed=True,
            skills=["a", "b", "c"],
            symlink_count=3,
            copy_count=0,
            unmanaged_count=0,
        )
        right = AGENT_AUDIT.AgentState(
            agent="cursor",
            label="Cursor",
            global_path=Path("/tmp/cursor"),
            cli_found=None,
            path_exists=True,
            is_dir=True,
            installed=True,
            skills=["b", "c", "d"],
            symlink_count=3,
            copy_count=0,
            unmanaged_count=0,
        )

        diff = AGENT_AUDIT.diff_skill_sets(left, right)
        self.assertEqual(diff.only_left, ["a"])
        self.assertEqual(diff.only_right, ["d"])
        self.assertEqual(diff.common_count, 2)
        self.assertFalse(diff.equal)

    def test_check_sync_with_canonical(self) -> None:
        canonical = AGENT_AUDIT.AgentState(
            agent="claude-code",
            label="Claude Code",
            global_path=Path("/tmp/claude"),
            cli_found=None,
            path_exists=True,
            is_dir=True,
            installed=True,
            skills=["a", "b", "c"],
            symlink_count=0,
            copy_count=3,
            unmanaged_count=0,
        )
        target = AGENT_AUDIT.AgentState(
            agent="codex",
            label="Codex",
            global_path=Path("/tmp/codex"),
            cli_found=None,
            path_exists=True,
            is_dir=True,
            installed=True,
            skills=["b", "d"],
            symlink_count=2,
            copy_count=0,
            unmanaged_count=0,
        )

        check = AGENT_AUDIT.check_sync_with_canonical(canonical, target)
        self.assertEqual(check.missing_in_agent, ["a", "c"])
        self.assertEqual(check.extra_in_agent, ["d"])
        self.assertFalse(check.in_sync)


if __name__ == "__main__":
    unittest.main(verbosity=2)
