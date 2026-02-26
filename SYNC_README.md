# Skills Repository Sync

This repository treats all repo `*-skills` directories as canonical source, then syncs to runtime locations like `~/.claude/skills`.

## Overview

Recommended sync path:
- **Canonical source**: `~/Code/skills/` (this repository)
- **Runtime registry**: `~/.claude/skills/`
- **Other agents**: symlinked from runtime registry via `link-all`

Legacy `sync-skills.sh` (plugin marketplace flow) is still available for compatibility.

## Features

- ✅ **Bidirectional Sync**: Sync from repository to Claude and vice versa
- ✅ **Incremental Updates**: Only syncs changed files
- ✅ **Nested Structure Support**: Handles multi-level skill hierarchies
- ✅ **Automatic Plugin Creation**: Creates user plugin structure if it doesn't exist
- ✅ **Status Reporting**: Shows sync statistics and skill counts

## Usage

### Basic Commands

```bash
# Bidirectional sync (default - recommended)
./sync-skills.sh both

# Sync from repository to Claude only
./sync-skills.sh to-claude

# Sync from Claude to repository only
./sync-skills.sh from-claude

# Show sync status
./sync-skills.sh status
```

### Typical Workflow

1. **After cloning this repository**:
   ```bash
   ./sync-skills.sh to-claude
   ```
   This will install all skills from the repository into Claude Code.

2. **After modifying skills in the repository**:
   ```bash
   ./sync-skills.sh to-claude
   ```
   This will update Claude Code with your changes.

3. **After modifying skills in Claude Code**:
   ```bash
   ./sync-skills.sh from-claude
   ```
   This will sync changes back to the repository.

4. **Regular maintenance**:
   ```bash
   ./sync-skills.sh both
   ```
   This performs a full bidirectional sync to ensure everything is in sync.

## Directory Structure

### Repository Structure
```
skills/
├── ai-skills/
├── career-skills/
├── communication-skills/
├── devops-skills/
├── engineering-skills/
├── leadership-skills/
├── marketing-skills/
├── obsidian-skills/
├── product-skills/
├── sales-skills/
├── tools-skills/
├── system-skills/          # sync tooling container
└── writing-skills/
```

### Claude Plugin Structure
```
~/.claude/plugins/marketplaces/user-skills/
├── .claude-plugin/
│   └── plugin.json
└── plugins/
    ├── devops-skills/
    │   └── skills/
    │       └── <skill-name>/
    ├── tools-skills/
    │   └── skills/
    │       └── <skill-name>/
    └── ...
```

## How It Works

1. **Repository → Claude**:
   - Finds all `SKILL.md` files recursively in each category
   - Preserves the directory hierarchy
   - Uses `rsync` to efficiently copy only changed files
   - Creates the user plugin structure if needed

2. **Claude → Repository**:
   - Scans the user plugin directory for skills
   - Syncs back any changes to the repository
   - Preserves the directory hierarchy

3. **Incremental Sync**:
   - Compares file contents using `cmp`
   - Only syncs files that have changed
   - Reports statistics on new, updated, and unchanged files

## Skill Categories

The canonical source is all root-level `*-skills` directories
(for example: `ai-skills`, `devops-skills`, `engineering-skills`, `tools-skills`, `writing-skills`).

## Current Status

Run `./sync-skills.sh status` to see:
```
Repository Skills:
  <category>: <count> skills
  ...

Claude Plugin Skills:
  <category>: <count> skills
  ...
```

## Troubleshooting

### Skills not appearing in Claude Code

1. Make sure the sync completed successfully:
   ```bash
   ./sync-skills.sh status
   ```

2. Restart Claude Code to reload plugins

3. Check that the plugin directory exists:
   ```bash
   ls -la ~/.claude/plugins/marketplaces/user-skills/
   ```

### Sync conflicts

If you've modified the same skill in both locations:
1. The sync will overwrite based on the direction you choose
2. Consider backing up important changes before syncing
3. Use `git` to track changes in the repository

### Permission issues

Make sure the script is executable:
```bash
chmod +x sync-skills.sh
```

## Git Integration

It's recommended to commit changes after syncing from Claude:

```bash
./sync-skills.sh from-claude
git status
git add .
git commit -m "Sync skills from Claude Code"
git push
```

## Automation

You can automate the sync process using:

### Git Hooks
Add to `.git/hooks/post-commit`:
```bash
#!/bin/bash
./sync-skills.sh to-claude
```

### Cron Job
```bash
# Sync every hour
0 * * * * cd ~/Code/skills && ./sync-skills.sh both
```

### Watch Script
```bash
# Install fswatch
brew install fswatch

# Watch for changes and auto-sync
fswatch -o . | xargs -n1 -I{} ./sync-skills.sh to-claude
```

## Notes

- The script uses `rsync` with `--delete` flag, which removes files in the destination that don't exist in the source
- Nested skill structures are supported, but canonical source remains repo-root category directories
- The script preserves all files in skill directories (SKILL.md, references/, scripts/, etc.)
- Changes are detected by comparing file contents, not timestamps

## Contributing

When adding new skills:
1. Add them to the appropriate category in the repository
2. Run `./sync-skills.sh to-claude` to install them
3. Commit and push to the repository

## License

Same as the skills repository.
