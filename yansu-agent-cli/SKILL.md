---
name: yansu-agent-cli
description: Use the bundled Yansu CLI to sync project knowledge/context/skills and run Yansu workflow commands.
---

<!-- managed-by-yansu-wails:yansu-agent-cli -->

# Yansu Agent CLI

## Trigger
Need to sync Yansu knowledge/context/skills, check Yansu project status, update project knowledge after changes, or manage cron automation jobs.

## How To Use
Resolve `yansu` from `PATH` first. If it is not installed on `PATH`, use the bundled binary for the current user:
- Windows PowerShell: `$env:USERPROFILE\.yansu-agent\bin\yansu.exe`
- POSIX shells: `$HOME/.yansu-agent/bin/yansu`

The examples below use `yansu`. Replace it with the resolved bundled path when `PATH` lookup fails.

## Common Commands
- `yansu status`
- `yansu pull`
- `yansu push`
- `yansu sync`
- `yansu analyze`

## Cron Automation Commands
- `yansu cron list` — list all cron jobs
- `yansu cron show <job-id>` — show job details
- `yansu cron add --name "X" --schedule "every 5m" --prompt "do Y" [--project /path] [--model sonnet]` — create a job
- `yansu cron update <job-id> [--name X] [--schedule X] [--prompt X] [--enabled true|false]` — update a job
- `yansu cron delete <job-id>` — delete a job
- `yansu cron run <job-id>` — trigger immediate execution

## Notes
- Run commands from the target project root (the directory containing .something/project.json).
- If the bundled binary is unavailable, use the fallback yansu command from PATH.
- Cron commands connect to the desktop app's local API. The app must be running.
