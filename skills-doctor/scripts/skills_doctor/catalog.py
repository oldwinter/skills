from __future__ import annotations

import json
import os
import re
from pathlib import Path

PROBES = {
    "local", "manual", "lark-contact", "lark-send", "lark-groups",
    "gitlab-read", "gitlab-admin", "github-org", "aws-identity",
    "kube-read", "kube-write",
}
NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
SKIP_DIRS = {".git", ".local", ".scratch", ".venv", "venv", "node_modules", "__pycache__"}
KNOWN_TOOLS = {
    "python3", "python", "bash", "git", "gh", "glab", "lark-cli", "aws",
    "kubectl", "argocd", "kargo", "terraform", "docker", "ssh", "node",
    "npm", "npx", "uv", "just", "jq", "curl", "agent-browser", "orca",
}


class CatalogError(ValueError):
    pass


def discover_skills(root: Path, directories: list[str] | None = None) -> dict[str, Path]:
    if not directories:
        directories = next(
            ([d] for d in (".claude/skills", ".agents/skills", ".codex/skills") if (root / d).is_dir()),
            ["."],
        )
    found: dict[str, Path] = {}
    for directory in directories:
        base = (root / directory).resolve()
        if not base.is_relative_to(root) or not base.is_dir():
            raise CatalogError("Skill directory must exist inside the selected repository")
        for current, children, files in os.walk(base, followlinks=False):
            children[:] = sorted(d for d in children if d not in SKIP_DIRS and not (Path(current) / d).is_symlink())
            if "SKILL.md" not in files:
                continue
            entry = Path(current) / "SKILL.md"
            children[:] = []
            if entry.is_symlink():
                continue
            name = entry.parent.name
            if not NAME.fullmatch(name):
                raise CatalogError("Invalid discovered skill directory name")
            if name in found and found[name] != entry.parent:
                raise CatalogError(f"Duplicate skill name; narrow --skills-dir: {name}")
            found[name] = entry.parent
    if not found:
        raise CatalogError("No skills found in the selected directories")
    return dict(sorted(found.items()))


def unreviewed_catalog(root: Path, discovered: dict[str, Path]) -> dict:
    return {
        "version": 1,
        "capabilities": {
            "unreviewed": {
                "tools": [], "permission": "Requirements have not been curated for this skill.",
                "owner": "Skill owner / intended operator",
                "remediation": "Read the skill and its references; declare required tools, roles and runtime dependencies in a target-local catalog.",
                "probe": "manual", "approval": "Inventory authorizes no business action.", "runtime": [],
            },
        },
        "skills": {
            name: {"sources": [str((path / "SKILL.md").relative_to(root)).replace("\\", "/")],
                   "profiles": {"unreviewed": ["unreviewed"]}}
            for name, path in discovered.items()
        },
    }


def load_catalog(root: Path, path: Path, discovered: dict[str, Path]) -> dict:
    if not path.resolve().is_relative_to(root):
        raise CatalogError("Catalog must stay inside the selected repository")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if (set(data) != {"version", "capabilities", "skills"}
                or type(data["version"]) is not int or data["version"] != 1):
            raise CatalogError("Unsupported catalog schema")
        capabilities, skills = data["capabilities"], data["skills"]
        if not isinstance(capabilities, dict) or not isinstance(skills, dict):
            raise CatalogError("Capabilities and skills must be objects")
        for name, spec in capabilities.items():
            if not NAME.fullmatch(name) or set(spec) != {
                "tools", "permission", "owner", "remediation", "probe", "approval", "runtime"
            }:
                raise CatalogError(f"Invalid capability: {name}")
            if not isinstance(spec["tools"], list) or any(
                not isinstance(tool, str) or not NAME.fullmatch(tool)
                for tool in spec["tools"]
            ):
                raise CatalogError(f"Invalid tool declaration: {name}")
            if spec["probe"] not in PROBES:
                raise CatalogError(f"Unknown probe: {name}")
            if not isinstance(spec["runtime"], list) or any(
                not isinstance(item, str) or not item.strip() for item in spec["runtime"]
            ):
                raise CatalogError(f"Invalid runtime requirements: {name}")
            for field in ("permission", "owner", "remediation", "approval"):
                if not isinstance(spec[field], str) or not spec[field].strip():
                    raise CatalogError(f"Missing {field}: {name}")
        missing, stale = discovered.keys() - skills.keys(), skills.keys() - discovered.keys()
        if missing or stale:
            raise CatalogError(
                f"Catalog coverage mismatch; missing={sorted(missing)}, stale={sorted(stale)}"
            )
        for name, spec in skills.items():
            if set(spec) != {"sources", "profiles"} or not spec["profiles"]:
                raise CatalogError(f"Invalid skill declaration: {name}")
            if not isinstance(spec["sources"], list) or not spec["sources"]:
                raise CatalogError(f"Missing evidence sources: {name}")
            entrypoint = str((discovered[name] / "SKILL.md").relative_to(root)).replace("\\", "/")
            if entrypoint not in spec["sources"]:
                raise CatalogError(f"Skill entrypoint missing from evidence: {name}")
            for source in spec["sources"]:
                resolved = (root / source).resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                    raise CatalogError(f"Missing or external evidence source: {name}")
                if resolved.suffix.lower() != ".md":
                    raise CatalogError(f"Evidence must be Markdown documentation: {name}")
            for profile, requirements in spec["profiles"].items():
                if not NAME.fullmatch(profile) or not isinstance(requirements, list) or not requirements:
                    raise CatalogError(f"Invalid profile: {name}")
                for requirement in requirements:
                    alternatives = requirement if isinstance(requirement, list) else [requirement]
                    if not alternatives or any(
                        not isinstance(item, str) or item not in capabilities
                        for item in alternatives
                    ):
                        raise CatalogError(f"Unknown capability in {name}/{profile}")
        return data
    except (OSError, json.JSONDecodeError, TypeError, AttributeError, KeyError) as error:
        raise CatalogError(f"Invalid catalog ({type(error).__name__})") from None


def tool_mentions(root: Path, skill_dir: Path, tools: set[str]) -> dict[str, list[str]]:
    """Collect hints, not executable instructions or inferred permissions."""
    found: dict[str, list[str]] = {}
    patterns = {
        tool: re.compile(r"`[^`\n]*(?<![\w-])" + re.escape(tool) + r"(?![\w-])[^`\n]*`")
        for tool in tools
    }
    for source in sorted(skill_dir.rglob("*.md")):
        if source.is_symlink() or not source.resolve().is_relative_to(root.resolve()):
            continue
        if source.stat().st_size > 512_000:
            continue
        for number, line in enumerate(source.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for tool, pattern in patterns.items():
                if pattern.search(line) and len(found.setdefault(tool, [])) < 3:
                    found[tool].append(f"{source.relative_to(root)}:{number}")
    return found
