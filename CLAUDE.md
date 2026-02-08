# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A skills library for AI coding assistants (Claude Code, Cursor, Cline). Primary unit is a **skill directory** containing `SKILL.md` (required) and optional `references/`, `rules/`, `scripts/`.

## Common Commands

### 3-Way Sync (Recommended)
```bash
# Incremental sync: ~/.codex/skills <-> ~/.agents/skills + ~/.agent/skills <-> repo
./sync-skills-3way.sh sync
./sync-skills-3way.sh status
```

### Install All Skills (New Machine)
```bash
npx add-skill . --all --global
```

### Validate a Single Skill
```bash
python3 system-skills/tools-skills/skill-creator/scripts/quick_validate.py <path/to/skill-dir>
```

### Legacy Sync (Destructive)
```bash
./sync-skills.sh status
./sync-skills.sh to-claude    # repo -> Claude plugin dir
./sync-skills.sh from-claude  # Claude plugin dir -> repo
```

## Architecture

```
skills/
├── coding-common-skills/    # General coding skills
├── devops-skills/           # Infrastructure and CLI tools
├── obsidian-skills/         # Note-taking skills
├── system-skills/           # Canonical skill collection synced from ~/.agents/skills
│   ├── product-skills/
│   ├── leadership-skills/
│   ├── engineering-skills/
│   ├── tools-skills/
│   └── ...
├── writing-skills/
├── sync-skills.sh           # Legacy bidirectional sync (uses --delete)
└── sync-skills-3way.sh      # 3-way incremental sync (no delete)
```

## Skill Directory Structure

```
skill-name/
├── SKILL.md              # Required - skill entrypoint
├── references/           # Optional - reference docs
├── rules/                # Optional - rule files
└── scripts/              # Optional - helper scripts (Python/shell)
```

### SKILL.md Frontmatter
```yaml
---
name: skill-name          # hyphen-case, required
description: Single line  # required, no angle brackets
---
```

## Key Constraints

- `SKILL.md` must exist and remain named exactly `SKILL.md`
- Skill directory name = skill identifier (use hyphen-case)
- Sync tooling crawls for `SKILL.md` recursively; renames/moves break sync
- `rsync --delete` in legacy sync can remove files in destination
- Repo contains intentional duplicates across categories and `system-skills/`
