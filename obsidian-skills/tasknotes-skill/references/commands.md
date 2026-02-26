# TaskNotes Commands Reference

## Task Properties

| Property | Description | Example |
|----------|-------------|---------|
| title | Task description | "Fix login bug" |
| status | Task state | pending, in-progress, completed |
| priority | Urgency level | low, medium, high, urgent |
| tags | Categorization | #work, #urgent, #bug |
| contexts | Location/context | @home, @office, @computer |
| projects | Project association | +website, +mobile-app |
| due | Due date | 2025-01-20, tomorrow |
| scheduled | Scheduled date | 2025-01-15 |
| completed | Completion timestamp | 2025-01-20T10:00:00Z |
| created | Creation timestamp | 2025-01-10T08:00:00Z |
| modified | Last modified timestamp | 2025-01-15T14:30:00Z |
| archived | Archived state | true/false |
| estimate | Time estimate | 30, 60 (minutes) |

## Complete Command Reference

### create
```bash
tn create <text>
# Natural language parsing for dates, priority, tags, contexts, projects, estimates
```

### list
```bash
tn list [options]
Options:
  --today                Today's tasks
  --overdue              Overdue tasks
  --completed            Completed tasks
  --filter <expression>  Advanced filter
  --limit <number>       Limit results (default: 20)
  --json                 JSON output
```

### search
```bash
tn search <query>
# Simple text search across tasks
```

### update
```bash
tn update <taskId> [options]
Options:
  --status <status>          Update status
  --priority <priority>      Update priority
  --due <date>               Update due date
  --scheduled <date>         Update scheduled date
  --title <title>            Update title
  --estimate <minutes>       Update estimate in minutes
  --add-tags <tags>          Add tags (comma-separated)
  --remove-tags <tags>       Remove tags
  --add-contexts <contexts>  Add contexts
  --remove-contexts <contexts>
  --add-projects <projects>  Add projects
  --remove-projects <projects>
```

### complete
```bash
tn complete <taskId>
# Mark task as completed
```

### toggle
```bash
tn toggle <taskId>
# Toggle between pending and completed
```

### archive
```bash
tn archive <taskId>
# Toggle archived status
```

### delete
```bash
tn delete <taskId> [--force]
# Delete a task
```

### timer
```bash
tn timer <action> [options]
Actions: start, stop, status, log
Options:
  --task <taskId>
  --period <period>     # today, week, month, all
  --from <date>         # ISO format
  --to <date>
  --limit <number>
```

### pomodoro
```bash
tn pomodoro <action> [options]
Actions: start, stop, pause, resume, status, stats, sessions
Options:
  --task <taskId>
  --duration <minutes>  # default: 25
  --limit <number>      # for stats/sessions
```

### projects
```bash
tn projects <action> [projectName]
Actions: list, show, create, stats
Options:
  --description <desc>  # for create
  --period <period>     # for stats
```

### stats
```bash
tn stats [options]
Options:
  --json  # JSON output
```

### filter-options
```bash
tn filter-options
# Show available filter options from actual tasks
```

## Filter Operators

### Text Operators
- `contains`: property contains value
- `does-not-contain`: property does not contain value

### Comparison Operators
- `is`: exact match
- `is-not`: not equal
- `before`: date before value
- `after`: date after value
- `on-or-before`: date <= value
- `on-or-after`: date >= value

### Numeric Operators
- `greater-than`: numeric greater than value
- `less-than`: numeric less than value

### Existence Operators
- `empty`: property is empty
- `not-empty`: property has value

### Boolean Operators
- `checked`: boolean is true
- `not-checked`: boolean is false

## Filter Examples

```bash
# Priority filters
tn list --filter "priority:urgent"
tn list --filter "priority:is-not:low"

# Status filters
tn list --filter "status:in-progress"
tn list --filter "status:completed"

# Date filters
tn list --filter "due:before:2025-02-01"
tn list --filter "due:after:2025-01-01"
tn list --filter "due:empty"

# Tag filters
tn list --filter "tags:contains:work"
tn list --filter "tags:does-not-contain:archived"

# Complex filters
tn list --filter "(priority:high OR priority:urgent) AND tags:work"
tn list --filter "status:in-progress AND due:not-empty"
tn list --filter "estimate:greater-than:30 AND status:pending"
```

## Natural Language Parsing Examples

```bash
# Basic task
tn "Buy groceries"

# With due date
tn "Buy groceries tomorrow"
tn "Submit report friday"
tn "Meeting next monday at 2pm"

# With priority
tn "Fix critical bug high priority"
tn "Urgent: review PR !!!"
tn "Complete report urgent"

# With tags
tn "Review PR #github #code"
tn "Write docs #documentation #writing"

# With contexts
tn "Call mom @home"
tn "Study Spanish @library"

# With projects
tn "Design homepage +website"
tn "Add login feature +mobile-app"

# With estimates
tn "Read article 30min"
tn "Complete chapter 2h"

# Combined
tn "Fix login bugwork #urgent +website 2h"
```

## Project Matching Guide

### tomorrow high priority @ Keyword-to-Project Mapping

When creating or updating tasks, match to projects using keywords:

| Keywords | Project |
|----------|---------|
| litellm, 模型, LLM, 推理, 部署 | `∑ 拓扑灵犀 - 设计LLM服务化架构（模型部署 and 推理加速）` |
| k8s, eks, k3s, infra, aws, 集群 | `∑ 拓扑灵犀 - infra建设` |
| 落库, 大数据, opensearch, mongodb, 爬虫 | `∑ 拓扑灵犀 - 大数据处理` |
| 小红书, 社交媒体 | `∑ 2025下半年小红书探索` |
| 面试, 求职, offer | `求职与面试` |
| 成本, 权限, 账号 | `∑ 拓扑灵犀` (main) |
| configmap, 镜像, 部署 | `∑ 拓扑灵犀 - infra建设` |
| 告警, 监控, prometheus | `∑ 拓扑灵犀` |
| 性能, 压测, benchmark | `∑ 拓扑灵犀 - 大数据处理` |

### Adding Projects to Tasks

```bash
# Method 1: Natural language in create
tn "任务描述 +∑ 项目名称 @工作"

# Method 2: Update existing task
tn update <taskId> --add-projects "∑ 项目名称"
```

### Creating New Projects

```bash
tn projects create "New Project Name" --description "Project description"
```

### Viewing Project Tasks

```bash
# Show specific project details
tn projects show "∑ 拓扑灵犀 - infra建设"

# Get project statistics
tn projects stats "∑ 拓扑灵犀 - infra建设" --period month
```
