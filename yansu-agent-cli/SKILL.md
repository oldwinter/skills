---
name: yansu-agent-cli
description: Use the bundled Yansu CLI to sync project knowledge/context/skills and run Yansu workflow commands.
---

<!-- managed-by-yansu-wails:yansu-agent-cli -->

# Yansu Agent CLI

## Trigger
Need to sync Yansu knowledge/context/skills, check Yansu project status, update project knowledge after changes, or manage cron automation jobs.

## How To Use
Use the bundled Yansu CLI first, then fallback to PATH:
- Preferred: "C:\Users\Administrator\.yansu-agent\bin\yansu.exe"
- Fallback: yansu

## Common Commands
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" status
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" pull
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" push
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" sync
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" analyze

## Cron Automation Commands
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" cron list                          — list all cron jobs
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" cron show <job-id>                 — show job details
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" cron add --name "X" --schedule "every 5m" --prompt "do Y" [--project /path] [--model sonnet] — create a job
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" cron update <job-id> [--name X] [--schedule X] [--prompt X] [--enabled true|false] — update a job
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" cron delete <job-id>               — delete a job
- "C:\Users\Administrator\.yansu-agent\bin\yansu.exe" cron run <job-id>                  — trigger immediate execution

## Notes
- Run commands from the target project root (the directory containing .something/project.json).
- If the bundled binary is unavailable, use the fallback yansu command from PATH.
- Cron commands connect to the desktop app's local API. The app must be running.
