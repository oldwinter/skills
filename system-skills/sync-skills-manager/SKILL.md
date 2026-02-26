---
name: sync-skills-manager
description: Manage synchronization workflows between repository skills and local system skill directories.
---

# Sync Skills Manager

Manage synchronization between repository skills and local/system skill directories.

## Scripts

### `sync-skills.sh` (canonical manager)

Sync between canonical `~/.claude/skills` and `./system-skills` categories.

| Command | Description |
|---------|-------------|
| `./sync-skills.sh diff` | Preview system-only skills |
| `./sync-skills.sh pull` | Sync `~/.claude/skills` -> repo (add new skills) |
| `./sync-skills.sh push` | Sync repo -> `~/.claude/skills` and refresh agent links |
| `./sync-skills.sh link-all` | Rebuild other agent dirs as symlinks to `~/.claude/skills` |
| `./sync-skills.sh dedupe` | Remove duplicate entries from `~/.gemini/skills` |
| `./sync-skills.sh status` | Show sync status |

### `sync-skills-3way.sh` (recommended)

Incremental 3-way sync across:

- `~/.codex/skills` (including `.system`)
- `~/.claude/skills` (canonical)
- repository skills tree

Key behavior:

- Incremental only (`rsync --update`), never deletes files.
- New skills missing in repo are added to `system-skills/tools-skills/`.
- For duplicate skill names in repo, the newest `SKILL.md` copy is treated as canonical for repo -> local sync.

| Command | Description |
|---------|-------------|
| `./sync-skills-3way.sh sync` | Run 3-way incremental sync (default) |
| `./sync-skills-3way.sh status` | Show counts and name-level diffs |
| `./sync-skills-3way.sh help` | Show usage |

## Usage

### Daily 3-way sync
```bash
./sync-skills-3way.sh sync
```

### Quick status check
```bash
./sync-skills-3way.sh status
```

## Configuration

`sync-skills.sh` uses `sync-config.json`:

```json
{
  "system_skills_path": "~/.claude/skills",
  "repo_skills_path": "./system-skills",
  "exclude_patterns": ["sync-skills-manager"],
  "sync_mode": "incremental",
  "default_command": "diff"
}
```
