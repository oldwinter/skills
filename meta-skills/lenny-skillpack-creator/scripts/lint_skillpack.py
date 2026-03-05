#!/usr/bin/env python3

"""
lint_skillpack.py

Validate a skill pack directory against the expected structure.

Usage:
  python skills/lenny-skillpack-creator/scripts/lint_skillpack.py <path/to/skill-folder>
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore

FRONTMATTER_RE = re.compile(r"^---\s*$")
REQ_FIELDS = ["name", "description"]
CODEX_NAME_MAX = 100
CODEX_DESCRIPTION_MAX = 500
REQ_SKILLPACK_METADATA = ["schema_version", "skill_slug", "version", "authors", "origin"]
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
ALLOWED_ORIGINS = {"refound", "original", "community"}
REQ_REF_FILES = [
    "INTAKE.md",
    "WORKFLOW.md",
    "TEMPLATES.md",
    "CHECKLISTS.md",
    "RUBRIC.md",
    "SOURCE_SUMMARY.md",
    "EXAMPLES.md",
]

def read_frontmatter(text: str) -> tuple[dict, str | None]:
    lines = text.splitlines()
    if not lines or not FRONTMATTER_RE.match(lines[0]):
        return {}, "SKILL.md missing YAML frontmatter opening marker (---)."
    # find second --- line
    end = None
    for i in range(1, len(lines)):
        if FRONTMATTER_RE.match(lines[i]):
            end = i
            break
    if end is None:
        return {}, "SKILL.md missing YAML frontmatter closing marker (---)."

    raw = "\n".join(lines[1:end]).strip()

    # Codex expects `name` and `description` to be single-line scalars in the YAML frontmatter.
    # Multi-line YAML (e.g., `description: >`) is a common validation failure mode.
    # See: https://developers.openai.com/codex/skills/create-skill/
    for k in REQ_FIELDS:
        m = re.search(rf"^{re.escape(k)}:\s*(.*)$", raw, flags=re.M)
        if not m:
            return {}, f"SKILL.md frontmatter missing required field: {k}"
        v_raw = (m.group(1) or "").strip()
        if not v_raw:
            return {}, f"SKILL.md frontmatter '{k}' must be a non-empty single-line value."
        if re.match(r"^[>|][0-9]*[+-]?\s*(#.*)?$", v_raw):
            return {}, f"SKILL.md frontmatter '{k}' must be a single-line value (no YAML block scalars)."
    if not raw:
        return {}, "SKILL.md YAML frontmatter is empty."

    if yaml is None:
        return {}, "PyYAML is required to parse SKILL.md frontmatter (install 'PyYAML')."

    try:
        data = yaml.safe_load(raw) or {}
    except Exception as e:
        return {}, f"SKILL.md has invalid YAML frontmatter: {type(e).__name__}: {e}"

    if not isinstance(data, dict):
        return {}, f"SKILL.md frontmatter must be a mapping, got: {type(data).__name__}"

    # Enforce Codex validation constraints (name <= 100 chars, description <= 500 chars)
    name = data.get("name", "")
    desc = data.get("description", "")
    if isinstance(name, str):
        if len(name.strip()) > CODEX_NAME_MAX:
            return {}, f"SKILL.md frontmatter 'name' exceeds {CODEX_NAME_MAX} characters."
        if "\n" in name or "\r" in name:
            return {}, "SKILL.md frontmatter 'name' must be single-line (no newlines)."
    if isinstance(desc, str):
        if len(desc.strip()) > CODEX_DESCRIPTION_MAX:
            return {}, f"SKILL.md frontmatter 'description' exceeds {CODEX_DESCRIPTION_MAX} characters."
        if "\n" in desc or "\r" in desc:
            return {}, "SKILL.md frontmatter 'description' must be single-line (no newlines)."

    return data, None

def read_skillpack_metadata(path: Path) -> tuple[dict, str | None]:
    if not path.exists():
        return {}, f"Missing skillpack.json at {path}"

    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        data = json.loads(raw)
    except Exception as e:
        return {}, f"skillpack.json is invalid JSON: {type(e).__name__}: {e}"

    if not isinstance(data, dict):
        return {}, f"skillpack.json must be a JSON object, got: {type(data).__name__}"

    # Keep `name`/`description` constraints aligned with Codex if these fields are present.
    name = data.get("name")
    desc = data.get("description")
    if isinstance(name, str):
        if len(name.strip()) > CODEX_NAME_MAX:
            return {}, f"skillpack.json field 'name' exceeds {CODEX_NAME_MAX} characters."
        if "\n" in name or "\r" in name:
            return {}, "skillpack.json field 'name' must be single-line (no newlines)."
    if isinstance(desc, str):
        if len(desc.strip()) > CODEX_DESCRIPTION_MAX:
            return {}, f"skillpack.json field 'description' exceeds {CODEX_DESCRIPTION_MAX} characters."
        if "\n" in desc or "\r" in desc:
            return {}, "skillpack.json field 'description' must be single-line (no newlines)."

    return data, None

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", help="Path to the skill directory (contains SKILL.md).")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    errors = []

    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        errors.append(f"Missing SKILL.md at {skill_md_path}")

    # references checks
    ref_dir = skill_dir / "references"
    if not ref_dir.exists():
        errors.append(f"Missing references/ directory at {ref_dir}")
    else:
        for fn in REQ_REF_FILES:
            if not (ref_dir / fn).exists():
                errors.append(f"Missing references/{fn}")

    # README check
    readme_path = skill_dir / "README.md"
    if not readme_path.exists():
        errors.append(f"Missing README.md at {readme_path}")

    # skillpack.json metadata check
    metadata_path = skill_dir / "skillpack.json"
    meta, meta_err = read_skillpack_metadata(metadata_path)
    if meta_err:
        errors.append(meta_err)
    else:
        for f in REQ_SKILLPACK_METADATA:
            if f not in meta:
                errors.append(f"skillpack.json missing required field: {f}")

        schema_version = meta.get("schema_version")
        if schema_version != 1:
            errors.append("skillpack.json schema_version must be 1")

        slug = meta.get("skill_slug")
        if not isinstance(slug, str) or not slug.strip():
            errors.append("skillpack.json skill_slug must be a non-empty string")
        elif slug.strip() != skill_dir.name:
            errors.append(f"skillpack.json skill_slug '{slug}' does not match folder name '{skill_dir.name}'")

        version = meta.get("version")
        if not isinstance(version, str) or not version.strip():
            errors.append("skillpack.json version must be a non-empty string")
        elif not SEMVER_RE.match(version.strip()):
            errors.append(f"skillpack.json version is not valid SemVer: {version!r}")

        origin = meta.get("origin")
        if not isinstance(origin, str) or origin.strip() not in ALLOWED_ORIGINS:
            errors.append(f"skillpack.json origin must be one of {sorted(ALLOWED_ORIGINS)}")

        authors = meta.get("authors")
        if not isinstance(authors, list) or not authors:
            errors.append("skillpack.json authors must be a non-empty list")
        else:
            for a in authors:
                if not isinstance(a, str) or not a.strip():
                    errors.append("skillpack.json authors items must be non-empty strings")
                    break

        contributors = meta.get("contributors", [])
        if contributors is not None and not isinstance(contributors, list):
            errors.append("skillpack.json contributors must be a list (or omitted)")
        elif isinstance(contributors, list):
            for c in contributors:
                if not isinstance(c, str) or not c.strip():
                    errors.append("skillpack.json contributors items must be non-empty strings")
                    break

        if isinstance(origin, str) and origin.strip() == "refound":
            upstream = meta.get("upstream")
            if not isinstance(upstream, dict):
                errors.append("skillpack.json upstream must be an object for origin=refound")
            else:
                page_url = upstream.get("page_url")
                skill_md_url = upstream.get("skill_md_url")
                if not isinstance(page_url, str) or not page_url.strip():
                    errors.append("skillpack.json upstream.page_url must be a non-empty string for origin=refound")
                if not isinstance(skill_md_url, str) or not skill_md_url.strip():
                    errors.append("skillpack.json upstream.skill_md_url must be a non-empty string for origin=refound")

    # frontmatter checks
    if skill_md_path.exists():
        txt = skill_md_path.read_text(encoding="utf-8", errors="replace")
        fm, fm_err = read_frontmatter(txt)
        if fm_err:
            errors.append(fm_err)
        else:
            for f in REQ_FIELDS:
                v = fm.get(f, None)
                if not isinstance(v, str) or not v.strip():
                    errors.append(f"Frontmatter missing required string field: {f}")

            # name match folder
            name = (fm.get("name") or "").strip() if isinstance(fm.get("name"), str) else ""
            if name and name != skill_dir.name:
                errors.append(f"Frontmatter name '{name}' does not match folder name '{skill_dir.name}'")

    if errors:
        print("[fail] Skill pack validation failed:")
        for e in errors:
            print(f" - {e}")
        return 2

    print("[ok] Skill pack looks structurally valid.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
