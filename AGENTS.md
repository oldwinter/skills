# PROJECT KNOWLEDGE BASE (skills repo)

**Generated:** 2026-01-31
**Commit:** 6fa0dbf
**Branch:** main

## OVERVIEW
Repository of Claude/agent “skills” (Markdown-first) organized by category. Primary unit: a skill directory containing `SKILL.md` plus optional `references/`, `rules/`, `scripts/`.

This repo is designed to sync between:
- the git working tree (this repo)
- local agent/Claude skill/plugin locations (see sync scripts below)

## STRUCTURE
```
skills/
├── README.md
├── SYNC_README.md
├── sync-skills.sh                      # repo ↔ ~/.claude/plugins/... (plugin structure)
├── coding-common-skills/               # small curated set
├── devops-skills/                      # small curated set
├── obsidian-skills/                    # small curated set
├── system-skills/                      # large set synced from ~/.agents/skills
└── writing-skills/
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Understand categories / counts | `README.md` | Canonical overview for humans.
| Repo ↔ Claude plugin sync | `SYNC_README.md`, `./sync-skills.sh` | Bidirectional sync into `~/.claude/plugins/marketplaces/user-skills/`.
| System skills sync/merge workflow | `system-skills/sync-skills-manager/` | Wrapper around `npx add-skill` + categorization logic.
| A skill’s definition | `**/SKILL.md` | Primary entrypoint for each skill.
| A skill’s deeper material | `**/references/`, `**/rules/`, `**/scripts/` | Optional; varies by skill.

## CONVENTIONS (PROJECT-SPECIFIC)
- **Skill entrypoint is `SKILL.md`** (directory naming matters; scripts crawl for `SKILL.md`).
- `system-skills/` is **nested by subcategory** (`product-skills/`, `tools-skills/`, etc.).
- This repo has **two sync systems**:
  - `./sync-skills.sh` → rsync-based sync to Claude plugin directory.
  - `system-skills/sync-skills-manager/sync-skills.sh` → manages `~/.agents/skills` ↔ `./system-skills`.

## ANTI-PATTERNS (THIS REPO)
- Don’t rename or relocate `SKILL.md` without updating sync tooling assumptions.
- Be careful with sync operations that can overwrite destinations:
  - `./sync-skills.sh` uses `rsync --delete` when syncing skill directories.
  - `system-skills/sync-skills-manager/sync-skills.sh push` installs/overwrites skills into system.

## COMMANDS
```bash
# Repo ↔ Claude plugin directory
./sync-skills.sh status
./sync-skills.sh to-claude
./sync-skills.sh from-claude
./sync-skills.sh both

# System skills manager (system ↔ repo)
./system-skills/sync-skills-manager/sync-skills.sh diff
./system-skills/sync-skills-manager/sync-skills.sh pull
./system-skills/sync-skills-manager/sync-skills.sh push
./system-skills/sync-skills-manager/sync-skills.sh status

# Install all skills (repo → system)
npx add-skill . --all --global

# Incrementally merge system skills into repo (system → repo)
npx add-skill ~/.agents/skills --sync --merge
```

## NOTES / GOTCHAS
- There is **intentional duplication**: some skills exist both in top-level categories and under `system-skills/`.
- Some skill directories contain their own `AGENTS.md` used as **skill-specific instructions**; treat those as owned by the skill (don’t “standardize” them at the repo level).
