# AGENTS.md (repo instructions for agentic coding)

This repository is a **skills library** (Markdown-first). Most work is editing `SKILL.md` files and related docs/scripts.

## Repository overview

Primary unit = a *skill directory* containing:
- `SKILL.md` (required, treated as the skill entrypoint)
- optional `references/`, `rules/`, `scripts/`

Repo is designed to sync between:
- this git working tree
- local Claude/Cline/Cursor skill locations (see sync tooling)

### Structure (high level)
```
skills/
├── README.md
├── SYNC_README.md
├── AGENTS.md
├── sync-skills.sh
├── coding-common-skills/
├── devops-skills/
├── obsidian-skills/
├── system-skills/
└── writing-skills/
```

## Cursor / Copilot rules

- No `.cursor/rules/` or `.cursorrules` found in this repo at time of writing.
- No `.github/copilot-instructions.md` found in this repo at time of writing.

If those files get added later, treat them as **higher priority** than this document.

## Build / lint / test commands

This repo does **not** have a single project-wide build/test runner (no root `package.json`, `pyproject.toml`, CI workflows, etc.).

Instead, “verification” is usually one of:
1) validating a specific skill directory structure/frontmatter
2) running a specific helper script (Python/shell)
3) running sync tooling

### Common commands (repo root)

#### Sync repo ↔ Claude plugin directory
```bash
./sync-skills.sh status
./sync-skills.sh to-claude
./sync-skills.sh from-claude
./sync-skills.sh both
```

Notes:
- `sync-skills.sh` uses `rsync --delete` when syncing a skill directory → **can delete files in destination**.

#### Sync system skills (`~/.agents/skills`) ↔ `./system-skills`
```bash
./system-skills/sync-skills-manager/sync-skills.sh diff
./system-skills/sync-skills-manager/sync-skills.sh pull     # alias: auto
./system-skills/sync-skills-manager/sync-skills.sh push
./system-skills/sync-skills-manager/sync-skills.sh status
```

Notes:
- `push` runs `npx add-skill .. --all --global` and can overwrite your system skills install.

#### Install all skills (repo → system)
```bash
npx add-skill . --all --global
```

### “Run a single test” equivalents

There is no uniform test suite. Use these targeted checks:

#### Validate ONE skill directory (fast)
```bash
python3 system-skills/tools-skills/skill-creator/scripts/quick_validate.py <path/to/skill-dir>
```

What it checks:
- `SKILL.md` exists
- YAML frontmatter exists and has `name:` + `description:`
- `name` is **hyphen-case** (lowercase letters/digits/hyphens)

#### Validate ONE “skill pack” structure (stricter)
```bash
python3 system-skills/tools-skills/lenny-skillpack-creator/scripts/lint_skillpack.py <path/to/skill-dir>
```

Notes:
- Requires `PyYAML` installed for frontmatter parsing.
- Checks presence of `references/*.md`, `README.md`, `skillpack.json`, and stricter metadata constraints.

#### Run a single helper script
Many skills include scripts (Python/shell). Run the specific script directly, e.g.:
```bash
python3 devops-skills/aws-cost-explorer/scripts/cost_query.py --days-ago 1 --min-cost 5
```

## Editing guidelines (most important)

### Skill directory invariants

- `SKILL.md` is required and should remain named exactly `SKILL.md`.
- Skill directory name is the **skill identifier**.
- Prefer **hyphen-case** for skill directory names (matches validators).
- Assume sync tooling crawls for `SKILL.md` recursively; renames/moves can break sync.

### `SKILL.md` frontmatter

The frontmatter is parsed by scripts; keep it simple:
- Must start with `---` and end with `---`.
- `name:` and `description:` should be **single-line scalars** (avoid YAML block scalars like `description: >`).
- Keep description free of angle brackets (`<` `>`) if a validator enforces it.

### Markdown style

- Use ATX headings (`#`, `##`, ...).
- Prefer fenced code blocks with language tags (```bash, ```python).
- Keep command blocks copy/paste safe; include placeholders like `<skill-name>`.
- Prefer explicit file paths relative to repo root.

### Shell script style (`*.sh`)

Observed patterns in this repo:
- Use `#!/bin/bash` and `set -e` near the top.
- Quote variables unless intentionally word-splitting.
- Prefer `"$var"` over unquoted `$var`.
- Be explicit about destructive operations (`rsync --delete`).

### Python style (`*.py`)

Observed patterns in this repo:
- Target modern Python (type hints like `dict | None` appear → Python 3.10+).
- Prefer `pathlib.Path` for filesystem paths.
- Use `subprocess.run(..., check=True, capture_output=True, text=True)` for CLI wrappers.
- On failures: print a clear message to `stderr` and exit non-zero.

Imports:
- Standard library first; third-party imports after; local imports last.

Typing:
- Use precise types for public functions; avoid `Any` unless unavoidable.

### TypeScript/TSX snippets

This repo contains TS/TSX primarily as *reference assets* inside skill docs/rules.
- Keep snippets minimal and idiomatic.
- Don’t introduce build tooling assumptions at repo root.

## Safety / operations

- Treat sync commands as potentially destructive (they overwrite/delete in destinations).
- Don’t edit generated/duplicated skill copies unless you know which is canonical.
  - This repo intentionally contains duplicates across top-level categories and `system-skills/`.

## Where to look (quick index)

| Need | Location |
|------|----------|
| Repo ↔ Claude plugin sync | `SYNC_README.md`, `./sync-skills.sh` |
| System skills sync tooling | `system-skills/sync-skills-manager/` |
| Curated categories | `coding-common-skills/`, `devops-skills/`, `obsidian-skills/`, `writing-skills/` |
| Canonical human overview | `README.md` |
