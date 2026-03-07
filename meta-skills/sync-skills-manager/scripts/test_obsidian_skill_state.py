from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SCRIPTS_DIR = Path(__file__).resolve().parent
STATE = load_module(SCRIPTS_DIR / "obsidian_skill_state.py", "obsidian_skill_state")
IMPORT = load_module(SCRIPTS_DIR / "import_obsidian_skill_state.py", "import_obsidian_skill_state")
EXPORT = load_module(SCRIPTS_DIR / "export_skills_to_obsidian.py", "export_skills_to_obsidian_roundtrip")


def _write_skill(skill_dir: Path, name: str, description: str) -> None:
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
        encoding="utf-8",
    )


class ObsidianSkillStateTests(unittest.TestCase):
    def test_extract_state_from_note_whitelist_and_notes_section(self) -> None:
        with TemporaryDirectory() as td:
            note = Path(td) / "agent-browser.md"
            note.write_text(
                "---\n"
                "skill_id: agent-browser\n"
                '个人评分: "7"\n'
                "个人状态: 常用\n"
                "个人标签:\n"
                '  - "browser"\n'
                "精选: true\n"
                "最后评估: 2026-03-08\n"
                "aliases:\n"
                '  - "浏览器 cli"\n'
                "---\n\n"
                "# agent-browser\n\n"
                "## 作用\n"
                "generated\n\n"
                "## 补充笔记\n"
                "- GitHub 仓库：[vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)\n"
                "- Playwright 的轻量替代\n\n"
                "## 其他段落\n"
                "ignore me\n",
                encoding="utf-8",
            )

            skill_id, entry = STATE.extract_state_from_note(note)
            self.assertEqual(skill_id, "agent-browser")
            self.assertEqual(entry.rating, 7)
            self.assertEqual(entry.status, "常用")
            self.assertEqual(entry.tags, ["browser"])
            self.assertTrue(entry.favorite)
            self.assertEqual(entry.reviewed_at, "2026-03-08")
            self.assertEqual(entry.aliases, ["浏览器 cli"])
            self.assertIn("GitHub 仓库", entry.notes or "")
            self.assertNotIn("ignore me", entry.notes or "")

    def test_state_file_round_trip(self) -> None:
        with TemporaryDirectory() as td:
            path = Path(td) / "obsidian-skill-state.yaml"
            entries = {
                "agent-browser": STATE.SkillStateEntry(
                    rating=7,
                    status="常用",
                    tags=["browser"],
                    favorite=True,
                    reviewed_at="2026-03-08",
                    aliases=["浏览器 cli"],
                    notes="- extra note",
                )
            }

            STATE.write_state_file(path, entries, generated_at="2026-03-08")
            generated_at, loaded = STATE.read_state_file(path)

            self.assertEqual(generated_at, "2026-03-08")
            self.assertEqual(loaded["agent-browser"].rating, 7)
            self.assertEqual(loaded["agent-browser"].aliases, ["浏览器 cli"])
            self.assertEqual(loaded["agent-browser"].notes, "- extra note")

    def test_import_obsidian_state_writes_meaningful_entries_only(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            vault = root / "vault"
            notes_dir = vault / "Atlas" / "Skills"
            notes_dir.mkdir(parents=True, exist_ok=True)
            state_path = root / "state.yaml"

            _write_skill(
                repo / "tools-skills" / "agent-browser",
                "agent-browser",
                "Browser automation CLI for AI agents.",
            )
            _write_skill(
                repo / "obsidian-skills" / "obsidian-bases",
                "obsidian-bases",
                "Create and edit Obsidian Bases.",
            )

            (notes_dir / "agent-browser.md").write_text(
                "---\n"
                "skill_id: agent-browser\n"
                "个人评分: 7\n"
                "个人状态: 常用\n"
                "个人标签:\n"
                '  - "browser"\n'
                "精选: true\n"
                "最后评估: 2026-03-08\n"
                "---\n\n"
                "# agent-browser\n\n"
                "## 补充笔记\n"
                "- useful note\n",
                encoding="utf-8",
            )
            (notes_dir / "obsidian-bases.md").write_text(
                "---\n"
                "skill_id: obsidian-bases\n"
                "个人评分: null\n"
                "个人状态: 待评估\n"
                "个人标签: []\n"
                "精选: false\n"
                "最后评估: null\n"
                "---\n\n"
                "# obsidian-bases\n",
                encoding="utf-8",
            )

            summary = IMPORT.import_obsidian_state(
                vault_root=vault,
                notes_dir=Path("Atlas/Skills"),
                state_path=state_path,
                repo_root=repo,
                dry_run=False,
            )

            self.assertEqual(summary.imported_notes, 2)
            self.assertEqual(summary.state_entries, 1)
            _, loaded = STATE.read_state_file(state_path)
            self.assertEqual(list(loaded.keys()), ["agent-browser"])

    def test_import_skips_notes_not_present_in_repo(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            vault = root / "vault"
            notes_dir = vault / "Atlas" / "Skills"
            notes_dir.mkdir(parents=True, exist_ok=True)
            state_path = root / "state.yaml"

            _write_skill(
                repo / "tools-skills" / "agent-browser",
                "agent-browser",
                "Browser automation CLI for AI agents.",
            )

            (notes_dir / "agent-browser.md").write_text(
                "---\n"
                "skill_id: agent-browser\n"
                "个人评分: 7\n"
                "---\n",
                encoding="utf-8",
            )
            (notes_dir / "legacy-skill.md").write_text(
                "---\n"
                "skill_id: legacy-skill\n"
                "个人评分: 6\n"
                "---\n",
                encoding="utf-8",
            )

            summary = IMPORT.import_obsidian_state(
                vault_root=vault,
                notes_dir=Path("Atlas/Skills"),
                state_path=state_path,
                repo_root=repo,
                dry_run=False,
            )

            self.assertEqual(summary.imported_notes, 1)
            _, loaded = STATE.read_state_file(state_path)
            self.assertEqual(list(loaded.keys()), ["agent-browser"])

    def test_export_seeds_new_note_from_state_file(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            vault = root / "vault"
            state_path = root / "obsidian-skill-state.yaml"

            _write_skill(
                repo / "tools-skills" / "agent-browser",
                "agent-browser",
                "Browser automation CLI for AI agents. Use when websites need automation.",
            )
            STATE.write_state_file(
                state_path,
                {
                    "agent-browser": STATE.SkillStateEntry(
                        rating=7,
                        status="常用",
                        tags=["browser"],
                        favorite=True,
                        reviewed_at="2026-03-08",
                        aliases=["浏览器 cli"],
                        notes="- useful note",
                    )
                },
                generated_at="2026-03-08",
            )

            EXPORT.sync_to_vault(
                repo_root=repo,
                vault_root=vault,
                write_base=False,
                dry_run=False,
                state_path=state_path,
            )

            text = (vault / "Atlas" / "Skills" / "agent-browser.md").read_text(encoding="utf-8")
            self.assertIn("个人评分: 7", text)
            self.assertIn('个人状态: "常用"', text)
            self.assertIn('  - "浏览器 cli"', text)
            self.assertIn("## 补充笔记", text)
            self.assertIn("- useful note", text)

    def test_export_keeps_existing_personal_fields_over_state_seed(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            repo = root / "repo"
            vault = root / "vault"
            notes_dir = vault / "Atlas" / "Skills"
            notes_dir.mkdir(parents=True, exist_ok=True)
            state_path = root / "obsidian-skill-state.yaml"

            _write_skill(
                repo / "tools-skills" / "agent-browser",
                "agent-browser",
                "Browser automation CLI for AI agents. Use when websites need automation.",
            )
            STATE.write_state_file(
                state_path,
                {
                    "agent-browser": STATE.SkillStateEntry(
                        rating=7,
                        status="常用",
                        tags=["browser"],
                        favorite=True,
                        reviewed_at="2026-03-08",
                        aliases=["浏览器 cli"],
                        notes="- useful note",
                    )
                },
                generated_at="2026-03-08",
            )
            (notes_dir / "agent-browser.md").write_text(
                "---\n"
                "skill_id: agent-browser\n"
                "aliases:\n"
                '  - "现有别名"\n'
                "个人评分: 3\n"
                "个人状态: 候选\n"
                "个人标签:\n"
                '  - "existing"\n'
                "精选: false\n"
                "最后评估: 2026-03-01\n"
                "---\n\n"
                "# agent-browser\n\n"
                "## 补充笔记\n"
                "- keep existing note\n",
                encoding="utf-8",
            )

            EXPORT.sync_to_vault(
                repo_root=repo,
                vault_root=vault,
                write_base=False,
                dry_run=False,
                state_path=state_path,
            )

            text = (notes_dir / "agent-browser.md").read_text(encoding="utf-8")
            self.assertIn("个人评分: 3", text)
            self.assertIn("个人状态: 候选", text)
            self.assertIn('  - "现有别名"', text)
            self.assertIn("- keep existing note", text)
            self.assertNotIn("- useful note", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
