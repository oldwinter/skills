# AGENTS.md (repo instructions for agentic coding)

This is the canonical agent instruction file for this repository. Root `CLAUDE.md` is a symlink to this file.

This repository is a **skills library** (Markdown-first). Most work is editing `SKILL.md` files and related docs/scripts.

It is also a public Canonical Source. Keep Skill implementations reusable outside cdd's private environment. Device inventory, consumer enablement/routing policy, automations, personal memory, and runtime installation evidence belong to private `oldwinter/general-tasks`; machine and harness configuration belongs to private `oldwinter/dotfiles`.

## Repository overview

Primary unit = a *skill directory* containing:
- `SKILL.md` (required, treated as the skill entrypoint)
- optional `references/`, `rules/`, `scripts/`

### Structure

Two layers. Category buckets are the classification source of truth; 41 root directories are also installable skill names. Six names exist in both layers and may diverge (`find-skills` already does). See `README.md` Standalone Skills.

```
skills/
├── AGENTS.md
├── README.md
├── <41 root skill directories>
├── base-skills/           # Foundational / cross-domain skills (6)
├── devops-skills/         # DevOps and infrastructure (13)
├── lenny-skills/          # Lenny / Refound AI skill packs (119)
│   ├── leadership-skills/
│   ├── marketing-skills/
│   ├── product-skills/
│   └── sales-skills/
├── meta-skills/           # Skills about skills (6)
├── obsidian-skills/       # Obsidian vault management (8)
└── tools-skills/          # Tooling & automation (6)
```

`just check-readme-map` verifies the handwritten README map against this tree.

## Multi-Agent Global Paths (vercel-labs/skills)

| Agent | `--agent` value | Global path |
|------|------------------|-------------|
| Claude Code | `claude-code` | `~/.claude/skills/` |
| Codex | `codex` | `~/.codex/skills/` |
| Amp | `amp` | `~/.config/agents/skills/` |
| Cursor | `cursor` | `~/.cursor/skills/` |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/` |
| OpenCode | `opencode` | `~/.config/opencode/skills/` |

Notes:
- `npx skills add ...` supports **Symlink** (recommended) and **Copy** install methods.
- Prefer **Symlink** to keep all agents aligned with one canonical skill source.
- Runtime install directory: `~/.claude/skills/` (other agents symlink into it).

Install all skills to all agents:
```bash
npx skills add . --skill '*' --global \
  --agent claude-code \
  --agent codex \
  --agent amp \
  --agent cursor \
  --agent gemini-cli \
  --agent opencode \
  --yes
```

## Build / lint / test commands

This repo does **not** have a project-wide build/test runner.

"Verification" is usually one of:
1. Validating a specific skill directory structure/frontmatter
2. Running a specific helper script (Python/shell)

### Validate a skill directory (fast)
```bash
python3 meta-skills/skill-creator/scripts/quick_validate.py <path/to/skill-dir>
```

Checks: `SKILL.md` exists, YAML frontmatter has `name:` + `description:`, name is hyphen-case.

### Validate a skill pack (stricter)
```bash
python3 meta-skills/lenny-skillpack-creator/scripts/lint_skillpack.py <path/to/skill-dir>
```

Requires `PyYAML`. Checks `references/*.md`, `README.md`, `skillpack.json`, and metadata.

## Editing guidelines

### Skill directory invariants

- `SKILL.md` is required and should remain named exactly `SKILL.md`.
- Skill directory name is the **skill identifier**.
- Prefer **hyphen-case** for skill directory names (matches validators).
- Never add credentials, private sessions, personal memory, private hostnames, or hardcoded device paths. Use placeholders or public interfaces in examples.

### `SKILL.md` frontmatter

The frontmatter is parsed by scripts; keep it simple:
- Must start with `---` and end with `---`.
- `name:` and `description:` should be **single-line scalars** (avoid YAML block scalars like `description: >`).
- Keep description free of angle brackets (`<` `>`) if a validator enforces it.

### Markdown style

- Use ATX headings (`#`, `##`, ...).
- Prefer fenced code blocks with language tags.
- Keep command blocks copy/paste safe; include placeholders like `<skill-name>`.
- Prefer explicit file paths relative to repo root.

### Shell script style (`*.sh`)

- Use `#!/bin/bash` and `set -e` near the top.
- Quote variables: prefer `"$var"` over unquoted `$var`.
- Be explicit about destructive operations.

### Python style (`*.py`)

- Target Python 3.10+ (type hints like `dict | None`).
- Prefer `pathlib.Path` for filesystem paths.
- Use `subprocess.run(..., check=True, capture_output=True, text=True)` for CLI wrappers.
- Standard library first; third-party after; local last.

## Where to look (quick index)

| Need | Location |
|------|----------|
| Root / standalone skills | repo root (`add-just-doctor`, `change-evidence`, …) |
| Name collisions | `README.md` Standalone Skills |
| Foundational skills | `base-skills/` |
| DevOps / infra skills | `devops-skills/` |
| Lenny / product skills | `lenny-skills/` |
| Skill creation & sync | `meta-skills/` |
| Obsidian vault skills | `obsidian-skills/` |
| Tooling & automation | `tools-skills/` |
| Canonical human overview | `README.md` |
