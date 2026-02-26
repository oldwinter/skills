#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as _dt
import fnmatch
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def eprint(*parts: object) -> None:
    print(*parts, file=sys.stderr)


def die(message: str, exit_code: int = 1) -> None:
    eprint(f"[ERROR] {message}")
    raise SystemExit(exit_code)


def load_json(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        die(f"Config not found: {path}")
    except OSError as exc:
        die(f"Failed to read config: {path} ({exc})")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        die(f"Invalid JSON in config {path}: {exc}")

    if not isinstance(data, dict):
        die(f"Config must be a JSON object: {path}")
    return data


def load_ratings(config: dict[str, Any]) -> tuple[int, dict[str, int]]:
    default_rating_raw = config.get("default_rating", 5)
    try:
        default_rating = int(default_rating_raw)
    except (TypeError, ValueError):
        die(f"Invalid default_rating: {default_rating_raw!r}")
    if default_rating < 1 or default_rating > 7:
        die(f"default_rating must be in [1, 7], got {default_rating}")

    ratings_raw = config.get("ratings", {})
    if not isinstance(ratings_raw, dict):
        die("Config 'ratings' must be an object")

    ratings: dict[str, int] = {}
    for skill, score_raw in ratings_raw.items():
        try:
            score = int(score_raw)
        except (TypeError, ValueError):
            die(f"Invalid rating for skill '{skill}': {score_raw!r}")
        if score < 1 or score > 7:
            die(f"Rating for skill '{skill}' must be in [1, 7], got {score}")
        ratings[str(skill)] = score

    return default_rating, ratings


def rating_for_skill(skill: str, ratings: dict[str, int], default_rating: int) -> int:
    return ratings.get(skill, default_rating)


def parse_stars_arg(stars_arg: str) -> set[int]:
    parts = [p.strip() for p in stars_arg.split(",") if p.strip()]
    if not parts:
        die("Invalid --stars value: empty")

    stars: set[int] = set()
    for p in parts:
        try:
            score = int(p)
        except ValueError:
            die(f"Invalid star value: {p!r}")
        if score < 1 or score > 7:
            die(f"Star value must be in [1, 7], got {score}")
        stars.add(score)
    return stars


def skills_for_stars(
    registry_skills: set[str],
    ratings: dict[str, int],
    default_rating: int,
    stars: set[int],
) -> set[str]:
    return {
        skill
        for skill in registry_skills
        if rating_for_skill(skill, ratings, default_rating) in stars
    }


def desired_for_star_mode(
    mode: str,
    inspection: "AgentInspection",
    star_skills: set[str],
) -> set[str]:
    if mode == "only":
        return set(star_skills)
    if mode == "install":
        return set(inspection.canonical_links) | set(star_skills)
    if mode == "uninstall":
        return set(inspection.canonical_links) - set(star_skills)
    die(f"Unknown stars mode: {mode}")
    return set()


def resolve_config_path(path_str: str, base_dir: Path) -> Path:
    p = Path(path_str).expanduser()
    if p.is_absolute():
        return p
    return (base_dir / p).resolve()


def now_timestamp() -> str:
    return f"{_dt.datetime.now().strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"


def is_skill_dir(path: Path) -> bool:
    try:
        return (path / "SKILL.md").is_file()
    except OSError:
        return False


def list_registry_skills(registry_dir: Path) -> tuple[set[str], set[str]]:
    managed: set[str] = set()
    unmanaged: set[str] = set()

    if not registry_dir.exists():
        die(f"Registry directory does not exist: {registry_dir}")
    if not registry_dir.is_dir():
        die(f"Registry directory is not a directory: {registry_dir}")

    for entry in registry_dir.iterdir():
        name = entry.name
        if name in {".DS_Store"}:
            continue
        if not (entry.is_dir() or entry.is_symlink()):
            continue
        if is_skill_dir(entry):
            managed.add(name)
        else:
            unmanaged.add(name)

    return managed, unmanaged


def guess_repo_root() -> Path:
    # This script lives at: <repo>/system-skills/sync-skills-manager/scripts/skills_profiles.py
    return Path(__file__).resolve().parents[3]


def build_categories(repo_root: Path) -> dict[str, set[str]]:
    categories: dict[str, set[str]] = {}

    for cat_dir in repo_root.rglob("*-skills"):
        if not cat_dir.is_dir():
            continue
        rel = cat_dir.relative_to(repo_root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if "sync-skills-manager" in rel.parts:
            continue

        direct_skills = {
            d.name
            for d in cat_dir.iterdir()
            if d.is_dir() and is_skill_dir(d)
        }
        if not direct_skills:
            continue

        categories.setdefault(cat_dir.name, set()).update(direct_skills)

    return categories


def resolve_symlink_target(link: Path) -> Path:
    target = os.readlink(link)
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = (link.parent / target_path)
    return target_path.resolve(strict=False)


def relative_symlink_target(link_parent: Path, target: Path) -> str:
    # On macOS, some temp paths appear under /var which resolves to /private/var.
    # Normalize both ends before computing a relative target to avoid odd paths like
    # /private/private/var/... after resolution.
    start = link_parent.resolve(strict=False)
    end = target.resolve(strict=False)
    return os.path.relpath(str(end), start=str(start))


@dataclass(frozen=True)
class AgentInspection:
    agent: str
    agent_dir: Path
    reserved_names: set[str]
    present_reserved: set[str]
    canonical_links: set[str]
    copy_dirs: set[str]
    other_symlinks: dict[str, Path]
    other_files: set[str]
    unmanaged_entries: set[str]

    @property
    def present_managed(self) -> set[str]:
        return (
            set(self.canonical_links)
            | set(self.copy_dirs)
            | set(self.other_symlinks.keys())
            | set(self.other_files)
        )


def inspect_agent_dir(
    agent: str,
    agent_dir: Path,
    registry_dir: Path,
    registry_skills: set[str],
    reserved_names: set[str],
) -> AgentInspection:
    present_reserved: set[str] = set()
    canonical_links: set[str] = set()
    copy_dirs: set[str] = set()
    other_symlinks: dict[str, Path] = {}
    other_files: set[str] = set()
    unmanaged_entries: set[str] = set()

    if not agent_dir.exists():
        return AgentInspection(
            agent=agent,
            agent_dir=agent_dir,
            reserved_names=reserved_names,
            present_reserved=present_reserved,
            canonical_links=canonical_links,
            copy_dirs=copy_dirs,
            other_symlinks=other_symlinks,
            other_files=other_files,
            unmanaged_entries=unmanaged_entries,
        )

    try:
        entries = list(agent_dir.iterdir())
    except OSError as exc:
        die(f"Failed to read agent dir {agent_dir}: {exc}")

    registry_dir_resolved = registry_dir.resolve(strict=False)

    for entry in entries:
        name = entry.name
        if name in reserved_names:
            present_reserved.add(name)
            continue

        if name not in registry_skills:
            unmanaged_entries.add(name)
            continue

        if entry.is_symlink():
            try:
                target = resolve_symlink_target(entry)
            except OSError:
                target = Path("<broken-symlink>")

            expected = (registry_dir_resolved / name).resolve(strict=False)
            if target == expected:
                canonical_links.add(name)
            else:
                other_symlinks[name] = target
            continue

        if entry.is_dir():
            copy_dirs.add(name)
            continue

        other_files.add(name)

    return AgentInspection(
        agent=agent,
        agent_dir=agent_dir,
        reserved_names=reserved_names,
        present_reserved=present_reserved,
        canonical_links=canonical_links,
        copy_dirs=copy_dirs,
        other_symlinks=other_symlinks,
        other_files=other_files,
        unmanaged_entries=unmanaged_entries,
    )


@dataclass(frozen=True)
class DesiredSkills:
    desired: set[str]
    unknown: set[str]


def merge_profile_sets(
    profile_names: list[str],
    profiles: dict[str, Any],
    categories: dict[str, set[str]],
    registry_skills: set[str],
) -> DesiredSkills:
    desired: set[str] = set()
    unknown: set[str] = set()

    for prof_name in profile_names:
        prof = profiles.get(prof_name)
        if prof is None:
            unknown.add(f"<missing-profile:{prof_name}>")
            continue
        if not isinstance(prof, dict):
            unknown.add(f"<invalid-profile:{prof_name}>")
            continue

        include_skills = prof.get("include_skills", [])
        include_categories = prof.get("include_categories", [])
        include_globs = prof.get("include_globs", [])

        exclude_skills = prof.get("exclude_skills", [])
        exclude_categories = prof.get("exclude_categories", [])
        exclude_globs = prof.get("exclude_globs", [])

        if include_skills:
            if not isinstance(include_skills, list):
                unknown.add(f"<invalid-include_skills:{prof_name}>")
            else:
                desired.update(str(s) for s in include_skills)

        if include_categories:
            if not isinstance(include_categories, list):
                unknown.add(f"<invalid-include_categories:{prof_name}>")
            else:
                for cat in include_categories:
                    cat_name = str(cat)
                    if cat_name not in categories:
                        unknown.add(f"<missing-category:{cat_name}>")
                        continue
                    desired.update(categories[cat_name])

        if include_globs:
            if not isinstance(include_globs, list):
                unknown.add(f"<invalid-include_globs:{prof_name}>")
            else:
                patterns = [str(p) for p in include_globs]
                for skill in registry_skills:
                    if any(fnmatch.fnmatch(skill, pat) for pat in patterns):
                        desired.add(skill)

        # Excludes
        if exclude_skills:
            if not isinstance(exclude_skills, list):
                unknown.add(f"<invalid-exclude_skills:{prof_name}>")
            else:
                desired.difference_update(str(s) for s in exclude_skills)

        if exclude_categories:
            if not isinstance(exclude_categories, list):
                unknown.add(f"<invalid-exclude_categories:{prof_name}>")
            else:
                for cat in exclude_categories:
                    cat_name = str(cat)
                    if cat_name not in categories:
                        unknown.add(f"<missing-category:{cat_name}>")
                        continue
                    desired.difference_update(categories[cat_name])

        if exclude_globs:
            if not isinstance(exclude_globs, list):
                unknown.add(f"<invalid-exclude_globs:{prof_name}>")
            else:
                patterns = [str(p) for p in exclude_globs]
                desired = {s for s in desired if not any(fnmatch.fnmatch(s, pat) for pat in patterns)}

    unknown_skills = {s for s in desired if s not in registry_skills}
    unknown |= unknown_skills
    desired = {s for s in desired if s in registry_skills}

    return DesiredSkills(desired=desired, unknown=unknown)


@dataclass(frozen=True)
class ApplyPlan:
    to_add: list[str]
    to_remove: list[str]
    conflicts: list[str]


def plan_apply(desired: set[str], inspection: AgentInspection) -> ApplyPlan:
    present_any = set(inspection.present_managed)
    to_remove = sorted(inspection.canonical_links - desired)
    to_add = sorted(desired - present_any)
    conflicts = sorted(desired & (present_any - inspection.canonical_links))
    return ApplyPlan(to_add=to_add, to_remove=to_remove, conflicts=conflicts)


def apply_agent(
    inspection: AgentInspection,
    registry_dir: Path,
    desired: set[str],
    *,
    do_apply: bool,
) -> ApplyPlan:
    plan = plan_apply(desired, inspection)

    if not inspection.agent_dir.exists():
        if do_apply:
            inspection.agent_dir.mkdir(parents=True, exist_ok=True)

    if plan.conflicts:
        eprint(
            f"[WARN] {inspection.agent}: {len(plan.conflicts)} conflict(s) present (run normalize first): "
            + ", ".join(plan.conflicts[:10])
            + (" ..." if len(plan.conflicts) > 10 else "")
        )

    if not do_apply:
        return plan

    # Remove extra canonical links
    for name in plan.to_remove:
        link_path = inspection.agent_dir / name
        if link_path.is_symlink():
            link_path.unlink()

    # Add missing links
    for name in plan.to_add:
        link_path = inspection.agent_dir / name
        if link_path.exists() or link_path.is_symlink():
            continue
        target = (registry_dir / name).resolve(strict=False)
        rel_target = relative_symlink_target(inspection.agent_dir, target)
        os.symlink(rel_target, link_path)

    return plan


@dataclass(frozen=True)
class NormalizePlan:
    to_replace: list[str]
    skipped_reserved: list[str]


def unique_backup_dest(base: Path) -> Path:
    if not base.exists():
        return base
    for i in range(1, 1000):
        candidate = base.with_name(f"{base.name}-{i}")
        if not candidate.exists():
            return candidate
    die(f"Backup destination collision: {base}")


def normalize_agent(
    inspection: AgentInspection,
    registry_dir: Path,
    registry_skills: set[str],
    *,
    backup_root: Path,
    timestamp: str,
    do_apply: bool,
) -> NormalizePlan:
    agent_dir = inspection.agent_dir
    reserved = inspection.reserved_names

    if not agent_dir.exists():
        if do_apply:
            agent_dir.mkdir(parents=True, exist_ok=True)
        return NormalizePlan(to_replace=[], skipped_reserved=[])

    to_replace: list[str] = []
    skipped_reserved: list[str] = []

    try:
        entries = list(agent_dir.iterdir())
    except OSError as exc:
        die(f"Failed to read agent dir {agent_dir}: {exc}")

    for entry in entries:
        name = entry.name
        if name in reserved:
            skipped_reserved.append(name)
            continue
        if name not in registry_skills:
            continue
        if name in inspection.canonical_links:
            continue
        to_replace.append(name)

    to_replace = sorted(set(to_replace))
    skipped_reserved = sorted(set(skipped_reserved))

    if not do_apply:
        return NormalizePlan(to_replace=to_replace, skipped_reserved=skipped_reserved)

    backup_root.mkdir(parents=True, exist_ok=True)

    for name in to_replace:
        src = agent_dir / name
        if not (src.exists() or src.is_symlink()):
            continue

        backup_dest = unique_backup_dest(backup_root / timestamp / inspection.agent / name)
        backup_dest.parent.mkdir(parents=True, exist_ok=True)

        # Move the existing entry out of the way (never delete in place).
        try:
            if src.is_symlink():
                os.replace(src, backup_dest)
            else:
                shutil.move(str(src), str(backup_dest))
        except OSError as exc:
            die(f"Failed to backup {src} -> {backup_dest}: {exc}")

        # Replace with canonical symlink to registry.
        target = (registry_dir / name).resolve(strict=False)
        rel_target = relative_symlink_target(agent_dir, target)
        try:
            os.symlink(rel_target, src)
        except OSError as exc:
            die(f"Failed to create symlink {src} -> {rel_target}: {exc}")

    return NormalizePlan(to_replace=to_replace, skipped_reserved=skipped_reserved)


def run_sync(repo_root: Path) -> None:
    script = repo_root / "sync-skills-3way.sh"
    if not script.exists():
        die(f"Sync script not found: {script}")
    subprocess.run(["bash", str(script), "sync"], cwd=str(repo_root), check=True)


def pick_agents(config: dict[str, Any], agent: str | None) -> list[str]:
    agents_obj = config.get("agents", {})
    if not isinstance(agents_obj, dict):
        die("Config 'agents' must be an object")

    if agent:
        if agent not in agents_obj:
            die(f"Unknown agent '{agent}'. Known: {', '.join(sorted(agents_obj.keys()))}")
        return [agent]
    return sorted(agents_obj.keys())


def cmd_status(args: argparse.Namespace) -> int:
    config_path: Path = args.config
    config = load_json(config_path)
    base_dir = config_path.parent
    default_rating, ratings = load_ratings(config)

    repo_root = guess_repo_root()
    categories = build_categories(repo_root)

    registry_dir = resolve_config_path(str(config.get("registry_dir", "")), base_dir)
    registry_skills, registry_unmanaged = list_registry_skills(registry_dir)

    agents = pick_agents(config, args.agent)
    profiles = config.get("profiles", {})
    agents_cfg = config.get("agents", {})

    print("skills-profiles status")
    print("----------------------------------------")
    print(f"repo_root:      {repo_root}")
    print(f"config:         {config_path}")
    print(f"registry_dir:   {registry_dir}")
    print(f"registry skills: {len(registry_skills)} managed, {len(registry_unmanaged)} unmanaged")
    rating_counts: dict[int, int] = {score: 0 for score in range(1, 8)}
    for skill in registry_skills:
        rating_counts[rating_for_skill(skill, ratings, default_rating)] += 1
    print("ratings:        " + "  ".join(f"{score}★={rating_counts[score]}" for score in range(7, 0, -1)))
    if registry_unmanaged:
        print("registry unmanaged (example): " + ", ".join(sorted(registry_unmanaged)[:10]) + (" ..." if len(registry_unmanaged) > 10 else ""))
    rated_unknown = sorted(set(ratings.keys()) - registry_skills)
    if rated_unknown:
        print(
            "rating warnings: skills in config but missing from registry: "
            + ", ".join(rated_unknown[:10])
            + (" ..." if len(rated_unknown) > 10 else "")
        )
    print("")

    for agent in agents:
        agent_cfg = agents_cfg.get(agent, {})
        agent_dir = resolve_config_path(str(agent_cfg.get("dir", "")), base_dir)
        reserved_names = set(agent_cfg.get("reserved_names", []) or [])
        prof_names = list(agent_cfg.get("profiles", []) or [])

        desired = merge_profile_sets(prof_names, profiles, categories, registry_skills)
        inspection = inspect_agent_dir(agent, agent_dir, registry_dir, registry_skills, reserved_names)

        print(f"[{agent}] {agent_dir}")
        print(f"  profiles: {', '.join(prof_names) if prof_names else '(none)'}")
        if desired.unknown:
            print("  warnings: " + ", ".join(sorted(desired.unknown)[:10]) + (" ..." if len(desired.unknown) > 10 else ""))
        print(f"  desired managed: {len(desired.desired)}")
        print(f"  linked (canonical symlinks): {len(inspection.canonical_links)}")
        print(f"  managed copies (dirs): {len(inspection.copy_dirs)}")
        print(f"  managed non-canonical symlinks: {len(inspection.other_symlinks)}")
        print(f"  managed other files: {len(inspection.other_files)}")
        print(f"  reserved present: {len(inspection.present_reserved)}")
        print(f"  unmanaged entries: {len(inspection.unmanaged_entries)}")

        # A few actionable examples
        if inspection.other_symlinks:
            examples = list(sorted(inspection.other_symlinks.keys()))[:5]
            print("  non-canonical examples: " + ", ".join(examples) + (" ..." if len(inspection.other_symlinks) > 5 else ""))
        if inspection.copy_dirs:
            examples = list(sorted(inspection.copy_dirs))[:5]
            print("  copy-dir examples: " + ", ".join(examples) + (" ..." if len(inspection.copy_dirs) > 5 else ""))
        print("")

    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    config_path: Path = args.config
    config = load_json(config_path)
    base_dir = config_path.parent

    repo_root = guess_repo_root()
    categories = build_categories(repo_root)

    registry_dir = resolve_config_path(str(config.get("registry_dir", "")), base_dir)
    registry_skills, _registry_unmanaged = list_registry_skills(registry_dir)

    agents = pick_agents(config, args.agent)
    profiles = config.get("profiles", {})
    agents_cfg = config.get("agents", {})

    for agent in agents:
        agent_cfg = agents_cfg.get(agent, {})
        agent_dir = resolve_config_path(str(agent_cfg.get("dir", "")), base_dir)
        reserved_names = set(agent_cfg.get("reserved_names", []) or [])
        prof_names = list(agent_cfg.get("profiles", []) or [])

        desired = merge_profile_sets(prof_names, profiles, categories, registry_skills)
        inspection = inspect_agent_dir(agent, agent_dir, registry_dir, registry_skills, reserved_names)
        plan = plan_apply(desired.desired, inspection)

        print(f"[{agent}] {agent_dir}")
        print(f"  desired: {len(desired.desired)}")
        if desired.unknown:
            print("  warnings: " + ", ".join(sorted(desired.unknown)[:10]) + (" ..." if len(desired.unknown) > 10 else ""))
        print(f"  to_add: {len(plan.to_add)}")
        print(f"  to_remove (canonical links): {len(plan.to_remove)}")
        print(f"  conflicts (normalize first): {len(plan.conflicts)}")

        if plan.to_add:
            print("  add examples: " + ", ".join(plan.to_add[:10]) + (" ..." if len(plan.to_add) > 10 else ""))
        if plan.to_remove:
            print("  remove examples: " + ", ".join(plan.to_remove[:10]) + (" ..." if len(plan.to_remove) > 10 else ""))
        if plan.conflicts:
            print("  conflict examples: " + ", ".join(plan.conflicts[:10]) + (" ..." if len(plan.conflicts) > 10 else ""))
        print("")

    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    config_path: Path = args.config
    config = load_json(config_path)
    base_dir = config_path.parent

    repo_root = guess_repo_root()
    categories = build_categories(repo_root)

    registry_dir = resolve_config_path(str(config.get("registry_dir", "")), base_dir)
    registry_skills, _registry_unmanaged = list_registry_skills(registry_dir)

    agents = pick_agents(config, args.agent)
    profiles = config.get("profiles", {})
    agents_cfg = config.get("agents", {})

    do_apply = args.apply
    if args.dry_run and do_apply:
        die("Choose either --dry-run or --apply (not both)")
    if args.dry_run:
        do_apply = False

    for agent in agents:
        agent_cfg = agents_cfg.get(agent, {})
        agent_dir = resolve_config_path(str(agent_cfg.get("dir", "")), base_dir)
        reserved_names = set(agent_cfg.get("reserved_names", []) or [])
        prof_names = list(agent_cfg.get("profiles", []) or [])

        desired = merge_profile_sets(prof_names, profiles, categories, registry_skills)
        inspection = inspect_agent_dir(agent, agent_dir, registry_dir, registry_skills, reserved_names)
        plan = apply_agent(inspection, registry_dir, desired.desired, do_apply=do_apply)

        print(f"[{agent}] {agent_dir}")
        print(f"  removed: {len(plan.to_remove)}")
        print(f"  added: {len(plan.to_add)}")
        print(f"  conflicts: {len(plan.conflicts)}")
        print("")

    if not do_apply:
        print("Dry-run only. Re-run with --apply to make changes.")

    return 0


def cmd_normalize(args: argparse.Namespace) -> int:
    config_path: Path = args.config
    config = load_json(config_path)
    base_dir = config_path.parent

    registry_dir = resolve_config_path(str(config.get("registry_dir", "")), base_dir)
    registry_skills, _registry_unmanaged = list_registry_skills(registry_dir)

    agents = pick_agents(config, args.agent)
    agents_cfg = config.get("agents", {})

    do_apply = args.apply
    if args.dry_run and do_apply:
        die("Choose either --dry-run or --apply (not both)")
    if args.dry_run:
        do_apply = False

    backup_root = resolve_config_path(args.backup_root, base_dir)
    timestamp = now_timestamp()

    for agent in agents:
        agent_cfg = agents_cfg.get(agent, {})
        agent_dir = resolve_config_path(str(agent_cfg.get("dir", "")), base_dir)
        reserved_names = set(agent_cfg.get("reserved_names", []) or [])

        inspection = inspect_agent_dir(agent, agent_dir, registry_dir, registry_skills, reserved_names)
        plan = normalize_agent(
            inspection,
            registry_dir,
            registry_skills,
            backup_root=backup_root,
            timestamp=timestamp,
            do_apply=do_apply,
        )

        print(f"[{agent}] {agent_dir}")
        print(f"  replaced: {len(plan.to_replace)}")
        if plan.to_replace:
            print("  replace examples: " + ", ".join(plan.to_replace[:10]) + (" ..." if len(plan.to_replace) > 10 else ""))
        if plan.skipped_reserved:
            print("  reserved skipped: " + ", ".join(plan.skipped_reserved))
        print("")

    if not do_apply:
        print("Dry-run only. Re-run with --apply to make changes.")
        print(f"Backup root (would be used): {backup_root}")
    else:
        print(f"Backups written under: {backup_root / timestamp}")

    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    repo_root = guess_repo_root()
    run_sync(repo_root)
    return 0


def cmd_refresh(args: argparse.Namespace) -> int:
    config_path: Path = args.config
    config = load_json(config_path)
    base_dir = config_path.parent

    repo_root = guess_repo_root()

    agents = pick_agents(config, args.agent)
    profiles = config.get("profiles", {})
    agents_cfg = config.get("agents", {})

    do_apply = args.apply
    if args.dry_run and do_apply:
        die("Choose either --dry-run or --apply (not both)")
    if args.dry_run:
        do_apply = False

    backup_root = resolve_config_path(args.backup_root, base_dir)
    timestamp = now_timestamp()

    registry_dir = resolve_config_path(str(config.get("registry_dir", "")), base_dir)

    if not do_apply:
        print("[refresh] Dry-run only. Would run: sync -> normalize -> apply. Re-run with --apply to execute.")
        print("")
    else:
        print("[refresh] Running sync-skills-3way.sh sync ...")
        run_sync(repo_root)
        print("")

    # If sync ran, registry/repo state may have changed; re-snapshot inputs used below.
    categories = build_categories(repo_root)
    registry_skills, _registry_unmanaged = list_registry_skills(registry_dir)

    for agent in agents:
        agent_cfg = agents_cfg.get(agent, {})
        agent_dir = resolve_config_path(str(agent_cfg.get("dir", "")), base_dir)
        reserved_names = set(agent_cfg.get("reserved_names", []) or [])
        prof_names = list(agent_cfg.get("profiles", []) or [])

        inspection_before = inspect_agent_dir(agent, agent_dir, registry_dir, registry_skills, reserved_names)
        norm_plan = normalize_agent(
            inspection_before,
            registry_dir,
            registry_skills,
            backup_root=backup_root,
            timestamp=timestamp,
            do_apply=do_apply,
        )

        desired = merge_profile_sets(prof_names, profiles, categories, registry_skills)
        inspection_after_norm = inspect_agent_dir(agent, agent_dir, registry_dir, registry_skills, reserved_names)
        apply_plan = apply_agent(inspection_after_norm, registry_dir, desired.desired, do_apply=do_apply)

        print(f"[{agent}] {agent_dir}")
        print(f"  normalize replaced: {len(norm_plan.to_replace)}")
        print(f"  apply removed: {len(apply_plan.to_remove)}")
        print(f"  apply added: {len(apply_plan.to_add)}")
        print(f"  apply conflicts: {len(apply_plan.conflicts)}")
        print("")

    if not do_apply:
        print("Dry-run only. Re-run with --apply to make changes.")
    else:
        print(f"Backups written under: {backup_root / timestamp}")

    return 0


def cmd_stars(args: argparse.Namespace) -> int:
    config_path: Path = args.config
    config = load_json(config_path)
    base_dir = config_path.parent
    default_rating, ratings = load_ratings(config)

    registry_dir = resolve_config_path(str(config.get("registry_dir", "")), base_dir)
    registry_skills, _registry_unmanaged = list_registry_skills(registry_dir)
    registry_dir_resolved = registry_dir.resolve(strict=False)

    stars = parse_stars_arg(args.stars)
    star_skills = skills_for_stars(
        registry_skills=registry_skills,
        ratings=ratings,
        default_rating=default_rating,
        stars=stars,
    )

    agents = pick_agents(config, args.agent)
    agents_cfg = config.get("agents", {})

    do_apply = args.apply
    if args.dry_run and do_apply:
        die("Choose either --dry-run or --apply (not both)")
    if args.dry_run:
        do_apply = False

    print(
        f"stars mode={args.mode} stars={','.join(str(s) for s in sorted(stars))} "
        f"match={len(star_skills)}"
    )
    print("")

    for agent in agents:
        agent_cfg = agents_cfg.get(agent, {})
        agent_dir = resolve_config_path(str(agent_cfg.get("dir", "")), base_dir)
        reserved_names = set(agent_cfg.get("reserved_names", []) or [])

        print(f"[{agent}] {agent_dir}")
        if agent_dir.resolve(strict=False) == registry_dir_resolved:
            print("  skipped: agent dir is canonical registry; star actions are link-level only.")
            print("")
            continue

        inspection = inspect_agent_dir(agent, agent_dir, registry_dir, registry_skills, reserved_names)
        desired = desired_for_star_mode(args.mode, inspection, star_skills)
        plan = apply_agent(inspection, registry_dir, desired, do_apply=do_apply)

        print(f"  removed: {len(plan.to_remove)}")
        print(f"  added: {len(plan.to_add)}")
        print(f"  conflicts: {len(plan.conflicts)}")
        if plan.to_add:
            print("  add examples: " + ", ".join(plan.to_add[:10]) + (" ..." if len(plan.to_add) > 10 else ""))
        if plan.to_remove:
            print(
                "  remove examples: "
                + ", ".join(plan.to_remove[:10])
                + (" ..." if len(plan.to_remove) > 10 else "")
            )
        if plan.conflicts:
            print(
                "  conflict examples: "
                + ", ".join(plan.conflicts[:10])
                + (" ..." if len(plan.conflicts) > 10 else "")
            )
        print("")

    if not do_apply:
        print("Dry-run only. Re-run with --apply to make changes.")

    return 0


def build_parser(default_config: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skills_profiles.py",
        description="Manage per-agent enabled skill sets as symlinks to a canonical registry (~/.claude/skills).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help=f"Path to skills-profiles.json (default: {default_config})",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_agent_scope_flags(p: argparse.ArgumentParser) -> None:
        g = p.add_mutually_exclusive_group()
        g.add_argument("--agent", help="Operate on a single agent name from config.")
        g.add_argument("--all", action="store_true", help="Operate on all agents (default).")

    p_status = sub.add_parser("status", help="Show registry/agent status and anomalies.")
    add_agent_scope_flags(p_status)

    p_diff = sub.add_parser("diff", help="Show desired vs current operations (dry-run).")
    add_agent_scope_flags(p_diff)

    p_apply = sub.add_parser("apply", help="Enable/disable skills by (un)linking canonical symlinks.")
    add_agent_scope_flags(p_apply)
    p_apply.add_argument("--dry-run", action="store_true", help="Preview changes (default).")
    p_apply.add_argument("--apply", action="store_true", help="Make changes.")

    p_norm = sub.add_parser("normalize", help="Convert copies/non-canonical links into canonical symlinks (with backups).")
    add_agent_scope_flags(p_norm)
    p_norm.add_argument("--dry-run", action="store_true", help="Preview changes (default).")
    p_norm.add_argument("--apply", action="store_true", help="Make changes.")
    p_norm.add_argument(
        "--backup-root",
        default="~/.claude/skills-backups",
        help="Backup root directory (default: ~/.claude/skills-backups).",
    )

    sub.add_parser("sync", help="Run repo sync-skills-3way.sh sync.")

    p_refresh = sub.add_parser("refresh", help="One-shot: sync -> normalize -> apply.")
    add_agent_scope_flags(p_refresh)
    p_refresh.add_argument("--dry-run", action="store_true", help="Preview normalize/apply (default). Does not run sync.")
    p_refresh.add_argument("--apply", action="store_true", help="Run sync + normalize + apply.")
    p_refresh.add_argument(
        "--backup-root",
        default="~/.claude/skills-backups",
        help="Backup root directory (default: ~/.claude/skills-backups).",
    )

    p_stars = sub.add_parser(
        "stars",
        help="Manage skills by star rating (install / uninstall / keep-only).",
    )
    add_agent_scope_flags(p_stars)
    p_stars.add_argument(
        "--mode",
        choices=["only", "install", "uninstall"],
        default="only",
        help="only: keep selected stars only; install: add selected stars; uninstall: remove selected stars.",
    )
    p_stars.add_argument(
        "--stars",
        required=True,
        help="Comma-separated stars in [1..7], e.g. 7 or 7,6,5.",
    )
    p_stars.add_argument("--dry-run", action="store_true", help="Preview changes (default).")
    p_stars.add_argument("--apply", action="store_true", help="Make changes.")

    return parser


def main(argv: list[str]) -> int:
    default_config = Path(__file__).resolve().parents[1] / "skills-profiles.json"
    parser = build_parser(default_config)
    args = parser.parse_args(argv)

    # Normalize config path early so status prints a clean absolute path.
    args.config = args.config.expanduser().resolve()

    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "diff":
        return cmd_diff(args)
    if args.cmd == "apply":
        return cmd_apply(args)
    if args.cmd == "normalize":
        return cmd_normalize(args)
    if args.cmd == "sync":
        return cmd_sync(args)
    if args.cmd == "refresh":
        return cmd_refresh(args)
    if args.cmd == "stars":
        return cmd_stars(args)

    die(f"Unknown command: {args.cmd}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except subprocess.CalledProcessError as exc:
        die(f"Command failed: {exc.cmd} (exit={exc.returncode})", exit_code=exc.returncode or 1)
