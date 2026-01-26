# Sync Skills Manager

Manage synchronization between repository skills and system-wide skills.

## Usage

### Incremental Update: System → Repository
```bash
# Pull only new/changed skills from system to repo
npx add-skill ~/.agents/skills --sync --merge

# Or use the helper script
./sync-skills.sh pull
```

### Full Sync: Repository → System
```bash
# Install all repo skills to system globally
npx add-skill . --all --global

# Or use the helper script
./sync-skills.sh push
```

### Dry Run (Preview Changes)
```bash
./sync-skills.sh diff
```

## Scripts

### `sync-skills.sh`

| Command | Description |
|---------|-------------|
| `./sync-skills.sh diff` | Preview changes without applying |
| `./sync-skills.sh pull` | Sync system → repository (add new skills) |
| `./sync-skills.sh push` | Sync repository → system (install all) |
| `./sync-skills.sh status` | Show current sync status |

## Sync Strategy

- **Pull**: Only adds new skills, never overwrites existing repo skills
- **Push**: Installs all skills from repo to system (overwrites if exists)
- **Diff**: Shows which skills exist in system but not in repo

## Configuration

Edit `sync-config.json` to customize sync behavior:

```json
{
  "system_skills_path": "~/.agents/skills",
  "repo_skills_path": "./system-skills",
  "exclude_patterns": [".git", "node_modules"],
  "sync_mode": "incremental"
}
```

## Examples

### Daily Workflow
```bash
# Check what's new in system
./sync-skills.sh diff

# Pull new skills to repo
./sync-skills.sh pull

# Commit changes
git add -A && git commit -m "sync: add new skills from system"
```

### After Adding New Skill to Repo
```bash
# Install to system for all agents
./sync-skills.sh push

# Or manually
npx add-skill . --all --global
```
