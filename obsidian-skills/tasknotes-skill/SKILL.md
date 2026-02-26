---
name: tasknotes
description: |
  Task management with TaskNotes CLI (tn) for Obsidian. Use when:
  - User mentions tasks, todos, task management
  - Working with Obsidian and task tracking
  - Creating, updating, searching, or completing tasks
  - Managing task priorities, due dates, tags, contexts, projects
  - Tracking time on tasks with pomodoro or timer
  - Any conversation about Obsidian task workflow
---

# TaskNotes Integration

TaskNotes is an Obsidian plugin that syncs tasks to a local API. The `tn` CLI communicates with this API.

## Core Workflow

### Finding Existing Tasks

```bash
# Search for tasks by query
tn search "<query>"

# List tasks with filters
tn list --filter "title:contains:'<keyword>'"

# List today's tasks
tn list --today

# List overdue tasks
tn list --overdue

# List completed tasks
tn list --completed
```

### Creating Tasks

```bash
# Natural language creation
tn "Fix bug in login flow tomorrow high priority @work"

# Creates task with parsed elements:
# - title: "Fix bug in login flow"
# - due: tomorrow's date
# - priority: high
# - context: @work
```

**NLP parsing recognizes:**
- Dates: `tomorrow`, `friday`, `next week`, `2024-12-25`
- Priority: `high priority`, `urgent`, `!!!`
- Tags: `#work`, `#project`
- Contexts: `@home`, `@office`
- Projects: `+website`
- Estimates: `2h`, `30min`

### Updating Tasks

```bash
tn update <taskId> --status in-progress
tn update <taskId> --priority high --due 2025-01-20
tn update <taskId> --add-tags urgent,bug
tn update <taskId> --title "New title"
```

### Completing Tasks

```bash
tn complete <taskId>    # Mark complete
tn toggle <taskId>      # Toggle status
tn archive <taskId>     # Archive task
tn delete <taskId> --force
```

## Filtering Syntax

```bash
# Property conditions
tn list --filter "priority:high"
tn list --filter "status:in-progress AND tags:urgent"
tn list --filter "due:after:2025-01-01 AND due:before:2025-01-31"

# Operators: is, is-not, contains, does-not-contain, before, after, empty, not-empty
# Logical: AND, OR
# Grouping: (condition1 OR condition2) AND condition3
```

## Time Tracking

```bash
tn timer start --task <taskId>
tn timer status
tn timer stop
tn timer log --period week
```

## Pomodoro Timer

```bash
tn pomodoro start --task <taskId> --duration 25
tn pomodoro status
tn pomodoro pause
tn pomodoro resume
tn pomodoro stop
```

## Task Lifecycle in Agent Workflow

When executing multi-step tasks:

1. **Create task** at start with `tn create "<title> @agent-work"`
2. **Update progress** with `tn update <taskId> --status in-progress`
3. **Mark complete** with summary:
   ```bash
   # Update title with what was accomplished
   tn update <taskId> --title "<original title> ✓ done: <concise summary>"
   tn complete <taskId>
   ```

## Configuration

```bash
tn config --list              # Show config
tn config --set host=localhost # Set host
```

Config stored at `~/.tasknotes-cli/config.json`.

## Important Notes

- Task IDs are required for update/complete/archive/delete commands
- Use `tn list --json` for programmatic access to task IDs
- Filter syntax is powerful - use it to find existing tasks before creating new ones

## Completing Tasks with Summary

When marking a task as done, **always update the task title** to include a concise summary of what was accomplished.

```bash
# WRONG - just mark complete without context
tn complete <taskId>

# CORRECT - update title with summary, then complete
tn update <taskId> --title "Original title ✓ done: fixed X, verified Y"
tn complete <taskId>
```

**Summary format**: `✓ done: <what was accomplished>`

**Examples**:
```
# Before: "configmap 更新镜像不更新的问题解决"
# After:  "configmap 更新镜像不更新的问题解决 ✓ done: 发现kube-proxy缓存问题, 重启pod生效"

# Before:  "opensearch 搜索性能测试"
# After:   "opensearch 搜索性能测试 ✓ done: qps从50提升到200, 优化了分词配置"

# Before:  "litellm 路由策略测试"
# After:   "litellm 路由策略测试 ✓ done: 验证fallback生效, novita故障时自动切换openrouter"
```

**Why this matters**:
- Task title becomes self-documenting
- Future回顾时一目了然
- No need to search for context in other places

## Common Pitfalls & Solutions

### 1. `create` command does NOT support `--priority` flag
```bash
# WRONG - will error: unknown option '--priority'
tn create "task name" --priority high

# CORRECT - use natural language
tn "task name high priority"
```

### 2. `update --add-projects` may silently fail
**Symptom**: Command returns success but project not actually assigned.

**Workaround**: Use natural language when creating tasks instead:
```bash
# Instead of:
tn update <taskId> --add-projects "∑ 拓扑灵犀 - infra建设"

# Do this when creating:
tn "task description +拓扑灵犀_infra建设 @工作"
```

**Note**: `∑` symbol causes parsing issues. Use underscore `_` instead:
```bash
tn "task +拓扑灵犀_infra建设 @工作"  # Works
tn "task +∑ 拓扑灵犀 - infra建设 @工作"  # May not parse correctly
```

### 3. 404 Task Not Found
**Causes:**
- Task already deleted or archived
- Task ID/path contains special characters (Chinese punctuation, etc.)
- Task was moved to a different location

**Solutions:**
- Run `tn list` first to get current task IDs
- Use `tn search "keyword"` to find tasks
- Copy the full path from `tn list --json`
- Always include `.md` extension in task ID

### 4. Task ID with special characters
Chinese punctuation (。) or symbols in task paths require exact matching.

```bash
# Get exact ID first
tn list --filter "title:contains:'keyword'" --json | jq -r '.data.tasks[0].id'

# Then use the exact ID
tn update "Calendar/Tasks/任务名。.md" --status in-progress
```

### 5. Batch operations failure
If one task fails in a batch, the remaining commands may still execute but some will fail. Always:
1. Check current state with `tn list` first
2. Process one command at a time for critical operations
3. Verify with `tn search` after each successful operation

### 6. Creating tasks from Daily Notes
Daily Notes tasks may not appear in `tn list` the same way as Task folder tasks. If needed:
1. Delete from Daily Notes
2. Recreate in proper Task folder format with natural language

### 7. Getting task ID for update
```bash
# Use JSON output to get exact task ID
tn list --json | jq -r '.data.tasks[0].id'

# Or search and filter
tn list --filter "title:contains:'keyword'" --json
```

### 8. Projects not appearing in task list
Projects are extracted from task metadata. If a task has projects but they don't show in `tn list`:
- Check `tn list --json` for the `projects` field
- Projects may need to be added during task creation, not via update

## Projects Management

### List Existing Projects

```bash
tn projects list
```

Shows all projects extracted from task data with task counts and progress.

**Current Projects:**
- `∑ 拓扑灵犀` - Main project
- `∑ 拓扑灵犀 - infra建设`
- `∑ 拓扑灵犀 - 大数据处理`
- `∑ 拓扑灵犀 - 设计LLM服务化架构（模型部署 and 推理加速）`
- `∑ 拓扑灵犀 -  misc.`
- `∑ 2025下半年小红书探索`
- `求职与面试`
- `落库占用cpu的时间和 查询或压测分开。避免互相影响。`
- `提交工单申请使用 claude 4.5 sonnet ...`

### Auto-Assign Project Workflow

When creating or managing tasks, follow this workflow:

**Step 1: Check existing projects**
```bash
tn projects list
```

**Step 2: Match task to project by keywords**

| Task Keywords | Project |
|---------------|---------|
| LLM, litellm, 模型 | `∑ 拓扑灵犀 - 设计LLM服务化架构（模型部署 and 推理加速）` |
| k8s, eks, k3s, infra | `∑ 拓扑灵犀 - infra建设` |
| 落库, 大数据, opensearch | `∑ 拓扑灵犀 - 大数据处理` |
| 小红书 | `∑ 2025下半年小红书探索` |
| 面试, 求职 | `求职与面试` |
| aws, 成本, 权限 | `∑ 拓扑灵犀` |
| 爬虫, mongodb | `∑ 拓扑灵犀 - 大数据处理` |
| configmap, k8s | `∑ 拓扑灵犀 - infra建设` |

**Step 3: Create task with project**
```bash
# Use natural language with project name
tn "configmap问题修复 +∑ 拓扑灵犀 - infra建设 @工作"
```

**Step 4: Or update existing task with project**
```bash
tn update <taskId> --add-projects "∑ 拓扑灵犀 - infra建设"
```

### No Matching Project?

If task cannot be matched to any existing project:

1. **Ask user**: "Should I create a new project for this task?"
2. **If yes**: Note the project name and suggest creating a descriptive project
3. **If no**: Create task without project association

**Project naming convention:**
- Use `∑` prefix for main project categories
- Use `-` for sub-projects: `∑ Main Project - Sub Project`
- Keep names descriptive and searchable
