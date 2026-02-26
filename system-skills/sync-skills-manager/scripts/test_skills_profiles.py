from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("skills_profiles", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SKILLS_PROFILES = load_module(Path(__file__).resolve().parent / "skills_profiles.py")


def _write_skill(dir_path: Path) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\n", encoding="utf-8")


class DesiredSetTests(unittest.TestCase):
    def test_desired_set_by_category(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"

            _write_skill(repo / "system-skills" / "product-skills" / "skill-a")
            _write_skill(repo / "system-skills" / "product-skills" / "skill-b")
            _write_skill(repo / "system-skills" / "devops-skills" / "skill-c")
            _write_skill(repo / "writing-skills" / "humanizer-zh")

            categories = SKILLS_PROFILES.build_categories(repo)
            registry_skills = {"skill-a", "skill-b", "skill-c", "humanizer-zh"}

            profiles = {"p": {"include_categories": ["product-skills"]}}
            desired = SKILLS_PROFILES.merge_profile_sets(["p"], profiles, categories, registry_skills)
            self.assertEqual(desired.desired, {"skill-a", "skill-b"})

    def test_desired_set_by_glob(self) -> None:
        categories: dict[str, set[str]] = {}
        registry_skills = {"baoyu-a", "baoyu-b", "other"}
        profiles = {"p": {"include_globs": ["baoyu-*"]}}

        desired = SKILLS_PROFILES.merge_profile_sets(["p"], profiles, categories, registry_skills)
        self.assertEqual(desired.desired, {"baoyu-a", "baoyu-b"})


class ApplyNormalizeTests(unittest.TestCase):
    def test_apply_creates_symlinks(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "registry"
            agent_dir = root / "agent"

            _write_skill(registry / "skill-a")
            registry_skills, _ = SKILLS_PROFILES.list_registry_skills(registry)

            inspection = SKILLS_PROFILES.inspect_agent_dir(
                "agent",
                agent_dir,
                registry,
                registry_skills,
                reserved_names=set(),
            )
            plan = SKILLS_PROFILES.apply_agent(
                inspection,
                registry,
                desired={"skill-a"},
                do_apply=True,
            )
            self.assertEqual(plan.to_add, ["skill-a"])
            self.assertTrue((agent_dir / "skill-a").is_symlink())
            target = (agent_dir / "skill-a").resolve(strict=False)
            self.assertEqual(target, (registry / "skill-a").resolve(strict=False))

    def test_apply_removes_extra_symlinks(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "registry"
            agent_dir = root / "agent"
            agent_dir.mkdir(parents=True, exist_ok=True)

            _write_skill(registry / "skill-a")
            _write_skill(registry / "skill-b")
            registry_skills, _ = SKILLS_PROFILES.list_registry_skills(registry)

            os.symlink(
                SKILLS_PROFILES.relative_symlink_target(agent_dir, registry / "skill-a"),
                agent_dir / "skill-a",
            )
            os.symlink(
                SKILLS_PROFILES.relative_symlink_target(agent_dir, registry / "skill-b"),
                agent_dir / "skill-b",
            )

            inspection = SKILLS_PROFILES.inspect_agent_dir(
                "agent",
                agent_dir,
                registry,
                registry_skills,
                reserved_names=set(),
            )
            plan = SKILLS_PROFILES.apply_agent(
                inspection,
                registry,
                desired={"skill-a"},
                do_apply=True,
            )
            self.assertEqual(plan.to_remove, ["skill-b"])
            self.assertTrue((agent_dir / "skill-a").exists())
            self.assertFalse((agent_dir / "skill-b").exists())

    def test_normalize_moves_dirs_to_backup_and_symlinks(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            registry = root / "registry"
            agent_dir = root / "agent"
            backups = root / "backups"

            _write_skill(registry / "skill-a")
            registry_skills, _ = SKILLS_PROFILES.list_registry_skills(registry)

            # Simulate a copied (non-symlink) directory in the agent.
            copied = agent_dir / "skill-a"
            copied.mkdir(parents=True, exist_ok=True)
            (copied / "local.txt").write_text("local", encoding="utf-8")

            inspection = SKILLS_PROFILES.inspect_agent_dir(
                "agent",
                agent_dir,
                registry,
                registry_skills,
                reserved_names=set(),
            )
            ts = "ts"
            plan = SKILLS_PROFILES.normalize_agent(
                inspection,
                registry,
                registry_skills,
                backup_root=backups,
                timestamp=ts,
                do_apply=True,
            )
            self.assertEqual(plan.to_replace, ["skill-a"])
            self.assertTrue((agent_dir / "skill-a").is_symlink())
            self.assertTrue((backups / ts / "agent" / "skill-a").exists())
            self.assertTrue((backups / ts / "agent" / "skill-a" / "local.txt").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
