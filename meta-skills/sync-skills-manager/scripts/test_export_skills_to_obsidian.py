from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("export_skills_to_obsidian", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


EXPORT = load_module(Path(__file__).resolve().parent / "export_skills_to_obsidian.py")


def _write_skill(skill_dir: Path, name: str, description: str) -> None:
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
        encoding="utf-8",
    )


class ExportSkillsToObsidianTests(unittest.TestCase):
    def test_discover_skills_skips_invalid_example_skill(self) -> None:
        with TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            _write_skill(
                repo / "base-skills" / "alpha-skill",
                "alpha-skill",
                "Alpha summary. Use when alpha work appears.",
            )
            invalid_dir = repo / "tools-skills" / "example-skill"
            invalid_dir.mkdir(parents=True, exist_ok=True)
            (invalid_dir / "SKILL.md").write_text("# example only\n", encoding="utf-8")

            skills = EXPORT.discover_skills(repo)
            self.assertEqual([skill.skill_id for skill in skills], ["alpha-skill"])

    def test_discover_skills_reads_repo_structure(self) -> None:
        with TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            _write_skill(
                repo / "base-skills" / "alpha-skill",
                "alpha-skill",
                "Alpha summary. Use when alpha work appears.",
            )
            _write_skill(
                repo / "lenny-skills" / "marketing-skills" / "beta-skill",
                "beta-skill",
                "Beta summary. Use when beta work appears.",
            )

            skills = EXPORT.discover_skills(repo)
            self.assertEqual([skill.skill_id for skill in skills], ["alpha-skill", "beta-skill"])
            self.assertEqual(skills[0].repo_group, "base-skills")
            self.assertEqual(skills[1].repo_subgroup, "marketing-skills")

    def test_discover_skills_prefers_frontmatter_name_for_skill_id(self) -> None:
        with TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            _write_skill(
                repo / "devops-skills" / "aws-api-billing-service-onboarding",
                "api-billing-service-onboarding",
                "Onboard billing service integrations.",
            )

            skills = EXPORT.discover_skills(repo)
            self.assertEqual(skills[0].skill_id, "api-billing-service-onboarding")
            self.assertEqual(
                skills[0].repo_path,
                "devops-skills/aws-api-billing-service-onboarding/SKILL.md",
            )

    def test_sync_creates_new_note_with_default_personal_fields(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            vault = root / "vault"
            _write_skill(
                repo / "obsidian-skills" / "obsidian-bases",
                "obsidian-bases",
                "Create and edit Obsidian Bases. Use when working with .base files.",
            )

            summary = EXPORT.sync_to_vault(repo_root=repo, vault_root=vault, write_base=False, dry_run=False)
            self.assertEqual(summary.created_notes, 1)

            note = vault / "Atlas" / "Skills" / "obsidian-bases.md"
            text = note.read_text(encoding="utf-8")
            self.assertIn("个人评分: null", text)
            self.assertIn('个人状态: "待评估"', text)
            self.assertIn("个人标签: []", text)
            self.assertIn('仓库路径: "obsidian-skills/obsidian-bases/SKILL.md"', text)

    def test_sync_preserves_personal_fields_and_body(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            vault = root / "vault"
            notes_dir = vault / "Atlas" / "Skills"
            notes_dir.mkdir(parents=True, exist_ok=True)

            _write_skill(
                repo / "tools-skills" / "agent-browser",
                "agent-browser",
                "Automates browser interactions. Use when websites need automation.",
            )

            existing = notes_dir / "agent-browser.md"
            existing.write_text(
                "---\n"
                'title: "agent-browser"\n'
                "个人评分: 5\n"
                '个人状态: "常用"\n'
                "个人标签:\n"
                '  - "browser"\n'
                "精选: true\n"
                '自定义字段: "keep-me"\n'
                "---\n\n"
                "# agent-browser\n\n"
                "这是我自己的备注。\n",
                encoding="utf-8",
            )

            summary = EXPORT.sync_to_vault(repo_root=repo, vault_root=vault, write_base=False, dry_run=False)
            self.assertEqual(summary.updated_notes, 1)

            text = existing.read_text(encoding="utf-8")
            self.assertIn("个人评分: 5", text)
            self.assertIn('个人状态: "常用"', text)
            self.assertIn('自定义字段: "keep-me"', text)
            self.assertIn("这是我自己的备注。", text)
            self.assertIn('英文说明: "Automates browser interactions. Use when websites need automation."', text)

    def test_render_base_includes_rating_views(self) -> None:
        content = EXPORT.render_base_file()
        self.assertIn("个人评分", content)
        self.assertIn("待评分", content)
        self.assertIn("高分技能", content)
        self.assertIn('个人状态 == "常用"', content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
