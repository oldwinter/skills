from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "sync-skills.sh"


def _write_skill(dir_path: Path) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "SKILL.md").write_text(
        "---\nname: test\ndescription: test\n---\n",
        encoding="utf-8",
    )


def _run_link_all(home: Path, system_skills: Path, targets: list[str]) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "HOME": str(home),
        "SYSTEM_SKILLS_DIR": str(system_skills),
        "AGENT_TARGET_DIRS": ",".join(targets),
    }
    return subprocess.run(
        ["bash", str(SCRIPT), "link-all"],
        cwd=SCRIPT.parent,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class LinkAllTargetGuardTests(unittest.TestCase):
    def test_link_all_refuses_non_skills_dirs_outside_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            home = root / "home"
            home.mkdir()
            registry = root / "claude-skills"
            _write_skill(registry / "skill-a")

            # Under $HOME but basename is not `skills`.
            wrong_name = home / "not-skills"
            wrong_name.mkdir()
            (wrong_name / "keepme.txt").write_text("sentinel", encoding="utf-8")

            # Named `skills` but outside $HOME.
            outside = root / "elsewhere" / "skills"
            outside.mkdir(parents=True)
            (outside / "keepme.txt").write_text("sentinel", encoding="utf-8")

            legit = home / "agent" / "skills"

            proc = _run_link_all(
                home,
                registry,
                [str(wrong_name), str(outside), str(legit)],
            )

            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(
                (wrong_name / "keepme.txt").read_text(encoding="utf-8"),
                "sentinel",
            )
            self.assertEqual(
                (outside / "keepme.txt").read_text(encoding="utf-8"),
                "sentinel",
            )
            self.assertFalse((wrong_name / "skill-a").exists())
            self.assertFalse((outside / "skill-a").exists())
            self.assertEqual(proc.stdout.count("Skipping link-all target"), 2)

            self.assertTrue((legit / "skill-a").is_symlink())
            self.assertEqual(
                os.readlink(legit / "skill-a"),
                str(registry / "skill-a"),
            )

    def test_link_all_skips_symlinked_ancestor_with_dotdot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            home = root / "home"
            home.mkdir()
            (home / "skills").mkdir()
            registry = root / "claude-skills"
            _write_skill(registry / "skill-a")

            outside_skills = root / "outside" / "skills"
            outside_skills.mkdir(parents=True)
            (outside_skills / "keepme.txt").write_text("sentinel", encoding="utf-8")
            deep = root / "outside" / "deep"
            deep.mkdir()
            (home / "alias").symlink_to(deep, target_is_directory=True)

            # Logically $HOME/skills, physically <outside>/skills.
            sneaky = str(home / "alias") + "/../skills"
            legit = home / "agent" / "skills"

            proc = _run_link_all(home, registry, [sneaky, str(legit)])

            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(
                (outside_skills / "keepme.txt").read_text(encoding="utf-8"),
                "sentinel",
            )
            self.assertFalse((outside_skills / "skill-a").exists())
            self.assertFalse((outside_skills / "skill-a").is_symlink())
            self.assertEqual(proc.stdout.count("Skipping link-all target"), 1)

            self.assertTrue((legit / "skill-a").is_symlink())
            self.assertEqual(
                os.readlink(legit / "skill-a"),
                str(registry / "skill-a"),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
