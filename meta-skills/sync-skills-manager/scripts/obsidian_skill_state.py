from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re


DEFAULT_STATE_PATH = Path("meta-skills/sync-skills-manager/data/obsidian-skill-state.yaml")
DEFAULT_NOTES_DIR = Path("Atlas/Skills")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)
SUPPLEMENTAL_NOTES_HEADING = "## 补充笔记"
DEFAULT_STATUS = "待评估"


@dataclass(frozen=True)
class SkillStateEntry:
    rating: int | str | None = None
    status: str = DEFAULT_STATUS
    tags: list[str] = field(default_factory=list)
    favorite: bool = False
    reviewed_at: str | None = None
    aliases: list[str] = field(default_factory=list)
    notes: str | None = None


def split_frontmatter_and_body(text: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return "", text
    return match.group(1), match.group(2)


def parse_scalar(text: str) -> object:
    value = text.strip()
    if value == "":
        return None
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value in {"null", "Null", "NULL"}:
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def render_scalar(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def parse_simple_frontmatter(frontmatter_text: str) -> dict[str, object]:
    lines = frontmatter_text.splitlines()
    index = 0
    data: dict[str, object] = {}

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            index += 1
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if raw_value != "":
            data[key] = parse_scalar(raw_value)
            index += 1
            continue

        list_items: list[object] = []
        probe = index + 1
        while probe < len(lines):
            nested = lines[probe]
            if not nested.startswith((" ", "\t")):
                break
            stripped = nested.strip()
            if stripped.startswith("- "):
                list_items.append(parse_scalar(stripped[2:]))
                probe += 1
                continue
            break

        if list_items:
            data[key] = list_items
            index = probe
        else:
            data[key] = None
            index += 1

    return data


def normalize_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = [value]
    normalized: list[str] = []
    for item in items:
        text = normalize_string(item)
        if text is not None:
            normalized.append(text)
    return normalized


def normalize_rating(value: object) -> int | str | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if not text:
        return None
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return text


def extract_supplemental_notes(body: str) -> str | None:
    lines = body.splitlines()
    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == SUPPLEMENTAL_NOTES_HEADING:
            start_index = index + 1
            break

    if start_index is None:
        return None

    collected: list[str] = []
    for line in lines[start_index:]:
        if re.match(r"^##\s+", line):
            break
        collected.append(line)

    text = "\n".join(collected).strip()
    return text or None


def render_supplemental_notes(notes: str | None) -> str:
    if not notes:
        return ""
    return f"\n\n{SUPPLEMENTAL_NOTES_HEADING}\n{notes.strip()}\n"


def extract_state_from_note(note_path: Path) -> tuple[str | None, SkillStateEntry]:
    text = note_path.read_text(encoding="utf-8")
    frontmatter_text, body = split_frontmatter_and_body(text)
    data = parse_simple_frontmatter(frontmatter_text)

    skill_id = normalize_string(data.get("skill_id")) or normalize_string(data.get("skill_name"))
    entry = SkillStateEntry(
        rating=normalize_rating(data.get("个人评分")),
        status=normalize_string(data.get("个人状态")) or DEFAULT_STATUS,
        tags=normalize_list(data.get("个人标签")),
        favorite=bool(data.get("精选")),
        reviewed_at=normalize_string(data.get("最后评估")),
        aliases=normalize_list(data.get("aliases")),
        notes=extract_supplemental_notes(body),
    )
    return skill_id, entry


def is_meaningful_state(entry: SkillStateEntry) -> bool:
    return any(
        (
            entry.rating is not None,
            entry.status != DEFAULT_STATUS,
            bool(entry.tags),
            entry.favorite,
            entry.reviewed_at is not None,
            bool(entry.aliases),
            entry.notes is not None,
        )
    )


def write_state_file(path: Path, entries: dict[str, SkillStateEntry], generated_at: str) -> None:
    lines = [f'generated_at: {render_scalar(generated_at)}']
    if not entries:
        lines.append("skills: {}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    lines.append("skills:")
    for skill_id in sorted(entries):
        entry = entries[skill_id]
        lines.append(f"  {skill_id}:")
        if entry.rating is not None:
            lines.append(f"    rating: {render_scalar(entry.rating)}")
        if entry.status:
            lines.append(f"    status: {render_scalar(entry.status)}")
        if entry.tags:
            lines.append("    tags:")
            for tag in entry.tags:
                lines.append(f"      - {render_scalar(tag)}")
        if entry.favorite:
            lines.append("    favorite: true")
        if entry.reviewed_at is not None:
            lines.append(f"    reviewed_at: {render_scalar(entry.reviewed_at)}")
        if entry.aliases:
            lines.append("    aliases:")
            for alias in entry.aliases:
                lines.append(f"      - {render_scalar(alias)}")
        if entry.notes:
            lines.append("    notes: |")
            for note_line in entry.notes.splitlines():
                lines.append(f"      {note_line}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_state_file(path: Path) -> tuple[str | None, dict[str, SkillStateEntry]]:
    if not path.exists():
        return None, {}

    lines = path.read_text(encoding="utf-8").splitlines()
    generated_at: str | None = None
    entries: dict[str, SkillStateEntry] = {}
    current_skill: str | None = None
    current_fields: dict[str, object] = {}
    index = 0

    def flush_current() -> None:
        nonlocal current_skill, current_fields
        if current_skill is None:
            return
        entries[current_skill] = SkillStateEntry(
            rating=normalize_rating(current_fields.get("rating")),
            status=normalize_string(current_fields.get("status")) or DEFAULT_STATUS,
            tags=normalize_list(current_fields.get("tags")),
            favorite=bool(current_fields.get("favorite")),
            reviewed_at=normalize_string(current_fields.get("reviewed_at")),
            aliases=normalize_list(current_fields.get("aliases")),
            notes=normalize_string(current_fields.get("notes")),
        )
        current_skill = None
        current_fields = {}

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if not line.startswith(" "):
            if stripped == "skills: {}":
                return generated_at, {}
            if stripped == "skills:":
                index += 1
                continue
            key, raw_value = stripped.split(":", 1)
            if key == "generated_at":
                generated_at = normalize_string(parse_scalar(raw_value.strip()))
            index += 1
            continue

        if line.startswith("  ") and not line.startswith("    "):
            flush_current()
            current_skill = stripped[:-1] if stripped.endswith(":") else stripped
            index += 1
            continue

        if current_skill is None:
            index += 1
            continue

        field_line = line[4:]
        key, raw_value = field_line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if raw_value == "|":
            block_lines: list[str] = []
            probe = index + 1
            while probe < len(lines) and lines[probe].startswith("      "):
                block_lines.append(lines[probe][6:])
                probe += 1
            current_fields[key] = "\n".join(block_lines).rstrip() or None
            index = probe
            continue

        if raw_value == "":
            items: list[object] = []
            probe = index + 1
            while probe < len(lines) and lines[probe].startswith("      - "):
                items.append(parse_scalar(lines[probe][8:]))
                probe += 1
            current_fields[key] = items
            index = probe
            continue

        current_fields[key] = parse_scalar(raw_value)
        index += 1

    flush_current()
    return generated_at, entries
