# AGENTS.md (repo instructions for agentic coding)

This is the canonical agent instruction file for this repository. Root `CLAUDE.md` should be a symlink to this file.

This repository is a **skills library** (Markdown-first). Most work is editing `SKILL.md` files and related docs/scripts.

## Repository overview

Primary unit = a *skill directory* containing:
- `SKILL.md` (required, treated as the skill entrypoint)
- optional `references/`, `rules/`, `scripts/`

Repo is designed to sync between:
- this git working tree
- local Claude/Cline/Cursor skill locations (see sync tooling)

## Multi-Agent Global Paths (vercel-labs/skills)

Based on the upstream `skills` CLI mapping, your primary agents use these global skill directories:

| Agent | `--agent` value | Global path |
|------|------------------|-------------|
| Claude Code | `claude-code` | `~/.claude/skills/` |
| Codex | `codex` | `~/.codex/skills/` |
| Amp | `amp` | `~/.config/agents/skills/` |
| Cursor | `cursor` | `~/.cursor/skills/` |
| Antigravity | `antigravity` | `~/.gemini/antigravity/skills/` |
| Droid | `droid` | `~/.factory/skills/` |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/` |
| OpenCode | `opencode` | `~/.config/opencode/skills/` |

Notes:
- `npx skills add ...` supports two install methods: **Symlink** (recommended, single source of truth) and **Copy** (independent copies).
- In a multi-agent setup like this repo, prefer **Symlink** to keep all agents aligned with one canonical skill source.
- This repository's custom sync scripts are centered on canonical `~/.claude/skills`, then fan out symlinks to other agent global directories.

Recommended command to install to your primary agents:
```bash
npx skills add . --skill '*' --global \
  --agent claude-code \
  --agent codex \
  --agent amp \
  --agent cursor \
  --agent antigravity \
  --agent droid \
  --agent gemini-cli \
  --agent opencode \
  --yes
```

### Local Consolidation Plan (canonical `~/.claude/skills`)

Goal: keep one canonical copy in `~/.claude/skills`, and let other agents consume skills via symlink.

Recommended local workflow:
```bash
# 1) Push newest repo copy per skill name into canonical source
./system-skills/sync-skills-manager/sync-skills.sh push

# 2) Rebuild all target agent dirs as symlinks to ~/.claude/skills
./system-skills/sync-skills-manager/sync-skills.sh link-all

# 3) Verify global distribution
npx skills ls -g
```

Practical note:
- `~/.agents/skills` may still exist as a compatibility mirror, but it is no longer the canonical edit source.

### OOTB Tooling From `vercel-labs/skills`

What is supported out of the box:
- Inventory: `npx skills ls -g`
- Install/update into selected agents: `npx skills add <source> --global --agent ... --skill ...`
- Remove from selected agents: `npx skills remove --global --agent ... --skill ...`
- Install method supports **Symlink** and **Copy** (prefer Symlink for centralized management).

What is not exposed as a single dedicated command (in current `npx skills --help`):
- No explicit one-shot command like “migrate all copied dirs to symlink”.
- Practical approach is remove+re-add for target agent/skill set, and choose/keep symlink mode.

Suggested migration pass (safe order):
```bash
# 1) Check current global distribution
npx skills ls -g

# 2) Reinstall overlap skills for Amp/Gemini/OpenCode from this repo
# (use interactive mode at least once to ensure Symlink mode is selected)
npx skills add . --global \
  --agent amp \
  --agent gemini-cli \
  --agent opencode \
  --skill argocd-cli aws-cli changelog-generator eksctl github-cli gitlab-cli \
  --skill humanizer-zh justfile kargo-cli kubectl obsidian-dashboard skill-creator \
  --skill sync-to-prod vercel-react-best-practices web-design-guidelines
```

### Full No-Miss Sync Runbook

Use this sequence when you want to minimize missed skills across active agents, then sync back into this git repo.

```bash
# 1) Consolidate Codex/Repo updates into canonical source and repository
./sync-skills-3way.sh sync

# 2) Ensure canonical source contains latest repo copies
./system-skills/sync-skills-manager/sync-skills.sh push

# 3) Rebuild all target agent dirs as symlinks to canonical source
./system-skills/sync-skills-manager/sync-skills.sh link-all

# 4) Verify names are aligned
./sync-skills-3way.sh status
```

Practical note:
- `./sync-skills-3way.sh` aligns by directories containing `SKILL.md` (unique skill names), not by all top-level folders.

Upstream discovery note from `vercel-labs/skills` README:
- If repo root contains `SKILL.md`, root is treated as one skill.
- Otherwise, CLI discovers skills recursively under `skills/` directory.

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

#### Sync system skills (`~/.claude/skills`) ↔ `./system-skills`
```bash
./system-skills/sync-skills-manager/sync-skills.sh diff
./system-skills/sync-skills-manager/sync-skills.sh pull     # alias: auto
./system-skills/sync-skills-manager/sync-skills.sh push
./system-skills/sync-skills-manager/sync-skills.sh link-all
./system-skills/sync-skills-manager/sync-skills.sh status
./sync-skills-3way.sh sync
./sync-skills-3way.sh status
./system-skills/sync-skills-manager/sync-skills-3way.sh sync
./system-skills/sync-skills-manager/sync-skills-3way.sh status
```

Notes:
- `push` syncs repo skills directly into canonical `~/.claude/skills`.
- `link-all` rebuilds other agent global directories as symlinks to canonical source.
- `sync-skills-3way.sh` performs incremental sync across `~/.codex/skills`, `~/.claude/skills`, and repo without deleting files.

#### Install all skills (repo → system)
```bash
./system-skills/sync-skills-manager/sync-skills.sh push
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
