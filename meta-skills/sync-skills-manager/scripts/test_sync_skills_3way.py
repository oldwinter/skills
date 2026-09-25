from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "sync-skills-3way.sh"
HYPHEN_PAIR = ("code-review", "codebase-design")


def _locale_names() -> str:
    return subprocess.check_output(["locale", "-a"], text=True)


def _has_de_de() -> bool:
    names = _locale_names().lower()
    return "de_de.utf8" in names or "de_de.utf-8" in names


def _write_skill(dir_path: Path) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "SKILL.md").write_text(
        "---\nname: test\ndescription: test\n---\n",
        encoding="utf-8",
    )


def _run_status(claude: Path, codex: Path, lc_all: str) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "LC_ALL": lc_all,
        "LANG": lc_all,
        "CLAUDE_DIR": str(claude),
        "CODEX_DIR": str(codex),
    }
    return subprocess.run(
        ["bash", str(SCRIPT), "status"],
        cwd=SCRIPT.parent,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class SyncSkills3wayStatusTests(unittest.TestCase):
    def test_hyphen_names_disorder_under_de_de(self) -> None:
        if not _has_de_de():
            self.skipTest("de_DE.UTF-8 locale not installed")
        listing = "\n".join(HYPHEN_PAIR) + "\n"
        de_sorted = subprocess.check_output(
            ["sort"],
            input=listing,
            text=True,
            env={**os.environ, "LC_ALL": "de_DE.UTF-8"},
        )
        c_sorted = subprocess.check_output(
            ["sort"],
            input=listing,
            text=True,
            env={**os.environ, "LC_ALL": "C"},
        )
        self.assertNotEqual(de_sorted, c_sorted)

    def test_status_uses_c_collation_for_sort_and_comm(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("LC_ALL=C sort -u", text)
        self.assertIn("LC_ALL=C comm", text)
        self.assertGreaterEqual(text.count("LC_ALL=C comm"), 4)

    def test_status_exits_zero_under_de_de_locale(self) -> None:
        if not _has_de_de():
            self.skipTest("de_DE.UTF-8 locale not installed")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            claude = tmp_path / "claude"
            codex = tmp_path / "codex"
            for name in HYPHEN_PAIR:
                _write_skill(claude / name)
                _write_skill(codex / name)
            proc = _run_status(claude, codex, "de_DE.UTF-8")
            combined = proc.stdout + proc.stderr
            self.assertNotIn("not in sorted order", combined)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("name-level diff summary", proc.stdout)
