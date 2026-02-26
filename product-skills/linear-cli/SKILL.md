---
name: linear-cli
description: This skill should be used when users need to manage Linear issues, tasks, or projects via command line. Triggers on requests mentioning Linear issues, issue tracking, creating issues, updating issue status, managing Linear projects, or Linear CLI operations.
---

# Linear CLI Skill

This skill provides instructions for managing Linear issues, tasks, and projects using the linear-cli command-line tool. Linear is a modern issue tracker designed for software teams, and the CLI enables workflow management directly from the terminal.

## Installation

First, install the linear-cli tool:

```bash
# Using Homebrew
brew install schpet/tap/linear

# Or using Deno
deno install -A --reload -f -g -n linear jsr:@schpet/linear-cli
```

## Setup

1. Create an API key at https://linear.app/settings/account/security (requires member access)
2. Add the API key to shell environment:

   ```bash
   # In ~/.bashrc or ~/.zshrc:
   export LINEAR_API_KEY="lin_api_..."

   # Or in fish:
   set -Ux LINEAR_API_KEY="lin_api_..."
   ```

3. Run the configuration wizard in your project repository:

   ```bash
   cd my-project-repo
   linear config
   ```

   This creates a `.linear.toml` config file with workspace and team settings.

## Issue Management

### View Issues

View the current issue (determined from git branch name or jj commit trailer):

```bash
linear issue view          # View current issue in terminal
linear issue view ABC-123  # View specific issue
linear issue view -w       # Open issue in web browser
linear issue view -a       # Open issue in Linear.app
linear issue id            # Print issue ID from current branch
linear issue title         # Print issue title
linear issue url           # Print Linear.app URL
```

### List Issues

List issues with filtering and sorting options:

```bash
linear issue list           # List unstarted issues assigned to you
linear issue list -A        # List unstarted issues assigned to anyone
linear issue list -s "In Progress"  # Filter by state
linear issue list -w       # Open in web browser
linear issue list -a       # Open in Linear.app
```

### Start Working on an Issue

Create or switch to an issue branch and mark as started:

```bash
linear issue start          # Choose an issue interactively
linear issue start ABC-123  # Start specific issue
```

The CLI creates a git branch with the issue ID and updates the issue status.

### Create Issues

Create new issues interactively or with flags:

```bash
linear issue create                    # Interactive prompts
linear issue create -t "title" -d "description"
```

### Update Issues

Update existing issue details:

```bash
linear issue update         # Interactive prompts for current issue
```

### Delete Issues

Remove an issue from Linear:

```bash
linear issue delete
```

### Create Pull Requests

Generate a GitHub PR with issue details via `gh pr create`:

```bash
linear issue pr
```

### Issue Comments

Manage comments on issues:

```bash
linear issue comment list          # List comments
linear issue comment add           # Add comment
linear issue comment add -p <id>   # Reply to specific comment
linear issue comment update <id>   # Update comment
```

## Team Management

```bash
linear team list       # List teams
linear team id         # Print team ID
linear team members    # List team members
linear team create     # Create a new team
linear team autolinks  # Configure GitHub autolinks
```

## Project Management

```bash
linear project list    # List projects
linear project view    # View project details
```

## Milestone Management

```bash
linear milestone list --project <projectId>     # List milestones
linear m list --project <projectId>             # Alias
linear milestone view <milestoneId>             # View details
linear m view <milestoneId>                     # Alias
linear milestone create --project <projectId> --name "Q1 Goals" --target-date "2026-03-31"
linear m create --project <projectId>           # Interactive
linear milestone update <milestoneId> --name "New Name"
linear m update <milestoneId> --target-date "2026-04-15"
linear milestone delete <milestoneId>
linear m delete <milestoneId> --force
```

## Document Management

Manage Linear documents (can be attached to projects or issues):

```bash
# List documents
linear document list
linear docs list                                # Alias
linear document list --project <projectId>
linear document list --issue TC-123
linear document list --json

# View documents
linear document view <slug>
linear document view <slug> --raw
linear document view <slug> --web
linear document view <slug> --json

# Create documents
linear document create --title "My Doc" --content "# Hello"
linear document create --title "Spec" --content-file ./spec.md
linear document create --title "Doc" --project <projectId>
linear document create --title "Notes" --issue TC-123
cat spec.md | linear document create --title "Spec"

# Update documents
linear document update <slug> --title "New Title"
linear document update <slug> --content-file ./updated.md
linear document update <slug> --edit

# Delete documents
linear document delete <slug>
linear document delete <slug> --permanent
linear document delete --bulk <slug1> <slug2>
```

## Configuration Options

Configure Linear CLI via environment variables or `.linear.toml`:

| Option          | Environment Variable       | TOML Key          | Example                    |
| --------------- | ------------------------ | ----------------- | -------------------------- |
| API key         | `LINEAR_API_KEY`         | `api_key`         | `"lin_api_..."`            |
| Team ID         | `LINEAR_TEAM_ID`         | `team_id`         | `"TEAM_abc123"`            |
| Workspace       | `LINEAR_WORKSPACE`       | `workspace`       | `"mycompany"`              |
| Issue sort      | `LINEAR_ISSUE_SORT`      | `issue_sort`      | `"priority"` or `"manual"` |
| VCS             | `LINEAR_VCS`             | `vcs`             | `"git"` or `"jj"`          |
| Download images | `LINEAR_DOWNLOAD_IMAGES` | `download_images` | `true` or `false`          |

## Version Control Integration

The CLI works with both git and jj (jujutsu):

- **git**: Works best when branches include Linear issue IDs (e.g., `eng-123-my-feature`). Use `linear issue start` or copy branch names from Linear UI.
- **jj**: Detects issues from `Linear-issue` trailers in commit descriptions. Use `linear issue start` to add the trailer automatically.

## Common Workflows

### Daily Workflow

1. List assigned issues: `linear issue list`
2. Start working: `linear issue start` (choose interactively)
3. View details: `linear issue view`
4. When done: create PR with `linear issue pr`

### Creating a Task

1. Create issue: `linear issue create -t "Task title" -d "Description"`
2. Start working: `linear issue start <issue-id>`
3. Track progress in the branch

### Reviewing Issues

1. List all unstarted issues: `linear issue list -A`
2. View specific issue: `linear issue view <issue-id>`
3. Check comments: `linear issue comment list`

## Tips

- Use `linear issue view` to quickly see the current branch's issue
- Use `linear issue pr` when ready to create a pull request - it pre-fills title and description from Linear
- The CLI keeps you in the right views in Linear, avoiding context switching
- Git branches with issue IDs are automatically detected by the CLI
