from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import sys


SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from obsidian_skill_state import (
    DEFAULT_STATE_PATH,
    SkillStateEntry,
    read_state_file,
    render_supplemental_notes,
)


DEFAULT_NOTES_DIR = Path("Atlas/Skills")
DEFAULT_BASE_PATH = Path("Atlas/Bases/skills管理.base")
TOP_LEVEL_KEY_RE = re.compile(r"^([^\s][^:]*):(?:\s*(.*))?$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)

CREATE_DEFAULT_KEYS = (
    "title",
    "tags",
    "type",
    "created",
    "publish",
    "aliases",
    "up",
    "分类",
)
PERSONAL_DEFAULT_KEYS = (
    "个人评分",
    "个人状态",
    "个人标签",
    "精选",
    "最后评估",
)
MANAGED_KEYS = (
    "skill_name",
    "skill_id",
    "仓库分类",
    "仓库子分类",
    "仓库路径",
    "作用描述",
    "触发场景",
    "英文说明",
    "来源路径",
    "同步时间",
)
PREFERRED_KEY_ORDER = (
    *CREATE_DEFAULT_KEYS,
    "skill_name",
    "skill_id",
    *PERSONAL_DEFAULT_KEYS,
    *MANAGED_KEYS[2:],
)
TRIGGER_MARKERS = (
    "This skill should be used when",
    "Use when",
    "Use for",
    "Triggers on",
)


@dataclass(frozen=True)
class SkillRecord:
    skill_id: str
    skill_name: str
    description: str
    repo_group: str
    repo_subgroup: str | None
    repo_path: str


@dataclass(frozen=True)
class FrontmatterBlock:
    key: str
    raw: str


@dataclass(frozen=True)
class SyncSummary:
    skills_count: int
    skipped_skills: int
    created_notes: int
    updated_notes: int
    unchanged_notes: int
    base_written: bool
    notes_dir: Path
    base_path: Path


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def parse_skill_frontmatter(skill_md: Path) -> tuple[str, str]:
    content = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError(f"Missing or invalid frontmatter: {skill_md}")

    name = ""
    description = ""
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"').strip("'")

    if not name or not description:
        raise ValueError(f"Missing name/description in {skill_md}")
    return name, description


def discover_skills(repo_root: Path) -> list[SkillRecord]:
    seen: dict[str, Path] = {}
    skills: list[SkillRecord] = []

    for skill_md in sorted(repo_root.glob("**/SKILL.md")):
        rel_path = skill_md.relative_to(repo_root)
        if len(rel_path.parts) < 2:
            continue

        try:
            skill_name, description = parse_skill_frontmatter(skill_md)
        except ValueError:
            continue
        skill_id = skill_name
        if skill_id in seen:
            raise ValueError(f"Duplicate skill id '{skill_id}' in {seen[skill_id]} and {skill_md}")
        seen[skill_id] = skill_md

        repo_group = rel_path.parts[0]
        repo_subgroup = rel_path.parts[1] if len(rel_path.parts) == 4 else None

        skills.append(
            SkillRecord(
                skill_id=skill_id,
                skill_name=skill_name,
                description=description,
                repo_group=repo_group,
                repo_subgroup=repo_subgroup,
                repo_path=rel_path.as_posix(),
            )
        )

    return skills


def count_invalid_skill_files(repo_root: Path) -> int:
    invalid = 0
    for skill_md in sorted(repo_root.glob("**/SKILL.md")):
        try:
            parse_skill_frontmatter(skill_md)
        except ValueError:
            invalid += 1
    return invalid


def split_description(description: str) -> tuple[str, str]:
    for marker in TRIGGER_MARKERS:
        index = description.find(marker)
        if index > 0:
            summary = description[:index].strip().rstrip(".")
            trigger = description[index:].strip()
            return summary or description, trigger
    return description.strip(), description.strip()


def build_managed_values(skill: SkillRecord, sync_date: str) -> dict[str, object]:
    summary, trigger = split_description(skill.description)
    return {
        "skill_name": skill.skill_name,
        "skill_id": skill.skill_id,
        "仓库分类": skill.repo_group,
        "仓库子分类": skill.repo_subgroup,
        "仓库路径": skill.repo_path,
        "作用描述": summary,
        "触发场景": trigger,
        "英文说明": skill.description,
        "来源路径": [skill.repo_path],
        "同步时间": sync_date,
    }


def build_create_defaults(skill: SkillRecord, sync_date: str, state_entry: SkillStateEntry | None = None) -> dict[str, object]:
    return {
        "title": skill.skill_id,
        "tags": ["skills"],
        "type": "skill-card",
        "created": sync_date,
        "publish": False,
        "aliases": state_entry.aliases if state_entry else [],
        "up": "[[∑ Skills 管理]]",
        "分类": "[[AI生成 - fileclass]]",
    }


def build_personal_defaults(state_entry: SkillStateEntry | None = None) -> dict[str, object]:
    return {
        "个人评分": state_entry.rating if state_entry else None,
        "个人状态": state_entry.status if state_entry else "待评估",
        "个人标签": state_entry.tags if state_entry else [],
        "精选": state_entry.favorite if state_entry else False,
        "最后评估": state_entry.reviewed_at if state_entry else None,
    }


def split_note(text: str) -> tuple[list[FrontmatterBlock], str]:
    if not text.startswith("---\n"):
        return [], text

    match = FRONTMATTER_RE.match(text)
    if not match:
        return [], text

    return parse_frontmatter_blocks(match.group(1)), match.group(2)


def parse_frontmatter_blocks(frontmatter_text: str) -> list[FrontmatterBlock]:
    blocks: list[FrontmatterBlock] = []
    current_key: str | None = None
    current_lines: list[str] = []

    for line in frontmatter_text.splitlines():
        top_level = TOP_LEVEL_KEY_RE.match(line)
        if top_level and not line.startswith((" ", "\t")):
            if current_key is not None:
                blocks.append(FrontmatterBlock(current_key, "\n".join(current_lines)))
            current_key = top_level.group(1)
            current_lines = [line]
        elif current_key is not None:
            current_lines.append(line)

    if current_key is not None:
        blocks.append(FrontmatterBlock(current_key, "\n".join(current_lines)))
    return blocks


def render_scalar(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_block(key: str, value: object) -> str:
    if isinstance(value, list):
        if not value:
            return f"{key}: []"
        lines = [f"{key}:"]
        for item in value:
            lines.append(f"  - {render_scalar(item)}")
        return "\n".join(lines)
    return f"{key}: {render_scalar(value)}"


def render_frontmatter(
    existing_blocks: list[FrontmatterBlock],
    managed_values: dict[str, object],
    create_defaults: dict[str, object],
    personal_defaults: dict[str, object],
) -> str:
    existing_by_key = {block.key: block for block in existing_blocks}
    rendered_by_key: dict[str, str] = {}
    ordered_keys: list[str] = []

    for block in existing_blocks:
        if block.key in managed_values:
            rendered_by_key[block.key] = render_block(block.key, managed_values[block.key])
        else:
            rendered_by_key[block.key] = block.raw
        ordered_keys.append(block.key)

    for key in PREFERRED_KEY_ORDER:
        if key in rendered_by_key:
            continue
        if key in managed_values:
            rendered_by_key[key] = render_block(key, managed_values[key])
        elif key in create_defaults:
            rendered_by_key[key] = render_block(key, create_defaults[key])
        elif key in personal_defaults:
            rendered_by_key[key] = render_block(key, personal_defaults[key])
        else:
            continue
        ordered_keys.append(key)

    for key in MANAGED_KEYS:
        if key not in rendered_by_key:
            rendered_by_key[key] = render_block(key, managed_values[key])
            ordered_keys.append(key)

    lines = [rendered_by_key[key] for key in ordered_keys]
    return "\n".join(lines).rstrip()


def render_new_note_body(skill: SkillRecord, state_entry: SkillStateEntry | None = None) -> str:
    notes_block = render_supplemental_notes(state_entry.notes if state_entry else None)
    return (
        f"# {skill.skill_id}\n\n"
        "由仓库同步脚本生成。请在 frontmatter 中维护你的个人字段：\n\n"
        "- `个人评分`\n"
        "- `个人状态`\n"
        "- `个人标签`\n"
        "- `精选`\n"
        "- `最后评估`\n\n"
        f"仓库路径：`{skill.repo_path}`\n"
        f"{notes_block}"
    )


def render_note(
    skill: SkillRecord,
    existing_text: str | None,
    sync_date: str,
    state_entry: SkillStateEntry | None = None,
) -> str:
    existing_blocks, body = split_note(existing_text or "")
    managed_values = build_managed_values(skill, sync_date)
    create_defaults = build_create_defaults(skill, sync_date, state_entry=state_entry)
    personal_defaults = build_personal_defaults(state_entry=state_entry)
    frontmatter = render_frontmatter(existing_blocks, managed_values, create_defaults, personal_defaults)

    if existing_text is None:
        body = render_new_note_body(skill, state_entry=state_entry)
    body = body.strip()
    if body:
        return f"---\n{frontmatter}\n---\n\n{body}\n"
    return f"---\n{frontmatter}\n---\n"


def render_base_file() -> str:
    return """filters:
  and:
    - file.inFolder("Atlas/Skills")
    - "!skill_name.isEmpty()"
views:
  - type: table
    name: 技能总览
    order:
      - file.name
      - 个人评分
      - 个人状态
      - 精选
      - 个人标签
      - 仓库分类
      - 仓库子分类
      - 作用描述
      - 仓库路径
      - file.mtime
    sort:
      - property: 个人评分
        direction: DESC
      - property: file.name
        direction: ASC
  - type: table
    name: 待评分
    filters:
      or:
        - 个人评分.isEmpty()
        - '个人状态 == "待评估"'
    order:
      - file.name
      - 个人状态
      - 仓库分类
      - 仓库子分类
      - 作用描述
      - 仓库路径
      - file.mtime
    sort:
      - property: file.mtime
        direction: DESC
  - type: table
    name: 高分技能
    filters:
      and:
        - "!个人评分.isEmpty()"
        - "个人评分 >= 4"
    order:
      - file.name
      - 个人评分
      - 个人状态
      - 精选
      - 仓库分类
      - 作用描述
      - 仓库路径
    sort:
      - property: 个人评分
        direction: DESC
      - property: file.name
        direction: ASC
  - type: table
    name: 常用 / 精选
    filters:
      or:
        - '个人状态 == "常用"'
        - "精选 == true"
    order:
      - file.name
      - 个人评分
      - 个人状态
      - 精选
      - 个人标签
      - 仓库分类
      - 作用描述
      - 仓库路径
      - file.mtime
    sort:
      - property: 精选
        direction: DESC
      - property: 个人评分
        direction: DESC
      - property: file.name
        direction: ASC
"""


def sync_to_vault(
    repo_root: Path,
    vault_root: Path,
    notes_dir: Path = DEFAULT_NOTES_DIR,
    base_path: Path = DEFAULT_BASE_PATH,
    state_path: Path | None = None,
    write_base: bool = False,
    dry_run: bool = False,
) -> SyncSummary:
    sync_date = date.today().isoformat()
    skills = discover_skills(repo_root)
    skipped_skills = count_invalid_skill_files(repo_root)
    resolved_state_path = state_path or (repo_root / DEFAULT_STATE_PATH)
    _, state_entries = read_state_file(resolved_state_path)
    target_notes_dir = vault_root / notes_dir
    target_base_path = vault_root / base_path

    created = 0
    updated = 0
    unchanged = 0

    if not dry_run:
        target_notes_dir.mkdir(parents=True, exist_ok=True)

    for skill in skills:
        note_path = target_notes_dir / f"{skill.skill_id}.md"
        existing_text = note_path.read_text(encoding="utf-8") if note_path.exists() else None
        rendered = render_note(
            skill,
            existing_text,
            sync_date,
            state_entry=state_entries.get(skill.skill_id),
        )

        if existing_text is None:
            created += 1
            if not dry_run:
                note_path.write_text(rendered, encoding="utf-8")
        elif existing_text != rendered:
            updated += 1
            if not dry_run:
                note_path.write_text(rendered, encoding="utf-8")
        else:
            unchanged += 1

    base_written = False
    if write_base:
        rendered_base = render_base_file()
        current_base = target_base_path.read_text(encoding="utf-8") if target_base_path.exists() else None
        if current_base != rendered_base:
            base_written = True
            if not dry_run:
                target_base_path.parent.mkdir(parents=True, exist_ok=True)
                target_base_path.write_text(rendered_base, encoding="utf-8")

    return SyncSummary(
        skills_count=len(skills),
        skipped_skills=skipped_skills,
        created_notes=created,
        updated_notes=updated,
        unchanged_notes=unchanged,
        base_written=base_written,
        notes_dir=target_notes_dir,
        base_path=target_base_path,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync repo skills into Obsidian notes.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=repo_root_from_script(),
        help="Skills repository root. Defaults to the current repository.",
    )
    parser.add_argument(
        "--vault-root",
        type=Path,
        required=True,
        help="Obsidian vault root.",
    )
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=DEFAULT_NOTES_DIR,
        help='Relative path inside the vault for synced notes. Default: "Atlas/Skills".',
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        default=DEFAULT_BASE_PATH,
        help='Relative path inside the vault for the generated base. Default: "Atlas/Bases/skills管理.base".',
    )
    parser.add_argument(
        "--state-path",
        type=Path,
        default=repo_root_from_script() / DEFAULT_STATE_PATH,
        help="Repo sidecar file containing exported personal skill state.",
    )
    parser.add_argument(
        "--write-base",
        action="store_true",
        help="Also write the Base file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    summary = sync_to_vault(
        repo_root=args.repo_root,
        vault_root=args.vault_root,
        notes_dir=args.notes_dir,
        base_path=args.base_path,
        state_path=args.state_path,
        write_base=args.write_base,
        dry_run=args.dry_run,
    )

    action = "Would sync" if args.dry_run else "Synced"
    print(
        f"{action} {summary.skills_count} skills -> {summary.notes_dir} "
        f"(created={summary.created_notes}, updated={summary.updated_notes}, unchanged={summary.unchanged_notes})"
    )
    if summary.skipped_skills:
        print(f"Skipped invalid SKILL.md files: {summary.skipped_skills}")
    if args.write_base:
        base_action = "would update" if args.dry_run and summary.base_written else "updated" if summary.base_written else "left unchanged"
        print(f"Base file {base_action}: {summary.base_path}")
    else:
        print(f"Base file not requested: {summary.base_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
