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


COLLISIONS = update_readme.COLLISIONS


def collision_marks() -> str:
    return " ".join(f"`{name}`" for name in COLLISIONS)


def bullets(names: tuple[str, ...] | list[str], *, link: str | None = None) -> str:
    lines = []
    for name in names:
        if link:
            lines.append(f"- [{name}]({link}/{name}/SKILL.md) — demo")
        else:
            lines.append(f"- **{name}** — demo")
    return "\n".join(lines)


def matching_readme(*, obsidian_canvas: bool = True) -> str:
    standalone = ("add-just-doctor", *COLLISIONS)
    obsidian = (
        "- [canvas-atlas](obsidian-skills/canvas-atlas/SKILL.md) — demo\n"
        if obsidian_canvas
        else ""
    )
    return f"""### Standalone Skills
{bullets(standalone)}

Collisions: {collision_marks()}

### Base Skills
{bullets(["context7"])}

### Meta Skills
{bullets(COLLISIONS)}

### Obsidian Skills
{obsidian}### Tools Skills
- **lev8-multi-case-pressure-test** — demo

## Statistics
- **Skill directories**: 16
- **Unique names**: 10
"""


def matching_tree(repo: Path, *, with_obsidian: bool = True, with_tools: bool = True) -> None:
    write_skill(repo / "add-just-doctor", "add-just-doctor")
    write_skill(repo / "base-skills" / "context7", "context7")
    for name in COLLISIONS:
        write_skill(repo / name, name)
        write_skill(repo / "meta-skills" / name, name)
    if with_obsidian:
        write_skill(repo / "obsidian-skills" / "canvas-atlas", "canvas-atlas")
    if with_tools:
        write_skill(
            repo / "tools-skills" / "lev8-multi-case-pressure-test",
            "lev8-multi-case-pressure-test",
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
            matching_tree(repo)
            (repo / "README.md").write_text(matching_readme(), encoding="utf-8")
            self.assertEqual(update_readme.check(repo), [])

    def test_missing_category_bullet_fails_when_counts_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            matching_tree(repo)
            (repo / "README.md").write_text(
                matching_readme(obsidian_canvas=False),
                encoding="utf-8",
            )
            errors = update_readme.check(repo)
            joined = "\n".join(errors)
            self.assertTrue(any("Obsidian Skills missing canvas-atlas" in e for e in errors), joined)

    def test_link_and_bold_listings_are_both_recognized(self) -> None:
        names = update_readme.listed_skill_names(
            "- [canvas-atlas](obsidian-skills/canvas-atlas/SKILL.md) — demo\n"
            "- **json-canvas** — demo\n"
        )
        self.assertEqual(names, {"canvas-atlas", "json-canvas"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
