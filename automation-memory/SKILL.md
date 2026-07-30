---
name: automation-memory
description: "Resolve and maintain recurring Codex automation memory safely. MUST use whenever prompts include Automation:, Automation ID:, or Automation memory:, especially before any raw $CODEX_HOME path is read or created."
---

# Automation Memory

## Overview

Automation runs have one extra startup job: resolve the automation memory path correctly before any generic repo checks. The common failure mode is treating an empty `CODEX_HOME` as valid and probing `/automations/...`.

## Rules

1. Handle automation memory before any repo startup sweep that touches `SOUL.md`, `USER.md`, `AGENTS.md`, or repo memory files.
2. If the prompt includes `Automation memory:`, use that explicit path template first after normalizing `$CODEX_HOME` with a fallback. Do not replace it with a guessed default such as `/automations/automation/memory.md`.
3. Expand `$CODEX_HOME` with a fallback: `${CODEX_HOME:-$HOME/.codex}`.
4. If no explicit memory path is provided, derive it as `${CODEX_HOME:-$HOME/.codex}/automations/<automation_id>/memory.md`.
5. The first command that touches automation memory must be a standalone bootstrap/read command that only resolves `AUTO_HOME` / `AUTO_MEM` and reads that file.
6. The first command must not include `pwd`, `ls`, `echo "$CODEX_HOME"`, banner `printf`, repo files, loops, or directory probes.
7. Reading this skill file is not the memory bootstrap. After reading the skill, the next command that touches automation memory must still be the normalized standalone bootstrap, not a raw `$CODEX_HOME/automations/...` probe.
8. Missing memory is not an error. Read if present; otherwise continue and create the file only when you are ready to write the run summary.
9. If you already drifted and ran the wrong first command, stop and rerun the clean bootstrap command before continuing with repo checks.
10. If the bootstrap command fails before execution with a shell-specific process creation error such as `CreateProcess ... No such file or directory` for `/bin/zsh` or `/bin/bash`, rerun the same standalone bootstrap command with `shell="/bin/sh"` and a minimal safe workdir such as `/`. Do not treat that as a missing memory file.
11. Before the final response, write a concise summary of what changed or why nothing changed, plus the current run time.

## Startup Checklist

Before any generic startup sweep, do exactly this in order:

1. Resolve `AUTO_MEM` with `${CODEX_HOME:-$HOME/.codex}`.
2. Run one standalone read command that touches only `AUTO_MEM`.
3. Only after that, read `SOUL.md`, `USER.md`, `AGENTS.md`, repo memory, or `.omx/` state.

If you are about to add `pwd`, `ls`, `mkdir`, `printf`, `echo "$CODEX_HOME"`, `for f in ...`, or repo files into the same first command, stop and split it up.

If you just opened this `SKILL.md`, do not then run:

```bash
if [ -f "$CODEX_HOME/automations/<id>/memory.md" ]; then ...
```

Run the normalized bootstrap below instead.

## Bootstrap Pattern

Use a standalone command like this before other startup reads:

```bash
AUTO_HOME="${CODEX_HOME:-$HOME/.codex}"
AUTO_MEM="$AUTO_HOME/automations/<automation_id>/memory.md"
[ -f "$AUTO_MEM" ] && sed -n '1,220p' "$AUTO_MEM" || true
```

If the prompt provides `Automation memory:` with `$CODEX_HOME`, expand that variable with the same fallback instead of trusting the raw string.

For prompts that already include `Automation memory: $CODEX_HOME/automations/<id>/memory.md`, do not reuse that raw string directly. Normalize it first:

```bash
AUTO_HOME="${CODEX_HOME:-$HOME/.codex}"
AUTO_MEM="$AUTO_HOME/automations/<automation_id>/memory.md"
[ -f "$AUTO_MEM" ] && sed -n '1,220p' "$AUTO_MEM" || true
```

Do not decorate this command. No banner text, no `pwd`, no `ls`, no repo files.

## Write Pattern

When the run is done, create the parent directory only if needed and append a short note:

```bash
AUTO_MEM="${CODEX_HOME:-$HOME/.codex}/automations/<automation_id>/memory.md"
mkdir -p "$(dirname "$AUTO_MEM")"
printf '%s\n' "<timestamp> run (~<duration>): <summary>" >> "$AUTO_MEM"
```

## Common Mistakes

- `printenv CODEX_HOME` exits non-zero, then the run still probes `/automations/...`.
- Reading this skill file first, then immediately probing `$CODEX_HOME/automations/<id>/memory.md` without the fallback.
- Memory read is bundled into a large startup loop, so the failure is easy to miss.
- The run reports completion without writing the summary back to automation memory.
- The first command does `pwd && printf ... "$CODEX_HOME/automations/..."`, so the run silently checks the wrong path before the skill is loaded.
- The run does `mkdir -p "$(dirname "$AUTO_MEM")"` before the first read, which can create or probe `/automations/...` when `CODEX_HOME` is empty.
- The run mixes automation memory with `SOUL.md`, `USER.md`, `MEMORY.md`, `.omx/`, or skill-file reads in one batch instead of doing the standalone bootstrap first.
- The first command does `echo "$CODEX_HOME" && ls -la "$CODEX_HOME/automations/<id>" && ...`; this still violates the standalone bootstrap rule even if the final path is correct.
- The run starts with `pwd && ls SOUL.md USER.md MEMORY.md >/dev/null`, then reads automation memory second. That means the automation-memory guardrail was skipped.
- The prompt already provides `Automation memory: .../<real-id>/memory.md`, but the run falls back to a vague or generic id such as `automation`.
- A failed `/bin/zsh` or `/bin/bash` process launch is misread as "memory missing" or "skill path missing" instead of retrying the same bootstrap command with `/bin/sh`.

## Wrong vs Right

Wrong:

```bash
pwd && printf '\n---AUTOMATION MEMORY---\n' && [ -f "$CODEX_HOME/automations/foo/memory.md" ] && cat "$CODEX_HOME/automations/foo/memory.md"
```

Wrong:

```bash
for f in SOUL.md USER.md MEMORY.md "$CODEX_HOME/automations/foo/memory.md"; do ...
```

Wrong:

```bash
AUTO_MEM="$CODEX_HOME/automations/foo/memory.md"
mkdir -p "$(dirname "$AUTO_MEM")"
```

Wrong:

```bash
echo "$CODEX_HOME" && ls -la "$CODEX_HOME/automations/foo" && [ -f "$CODEX_HOME/automations/foo/memory.md" ] && sed -n '1,220p' "$CODEX_HOME/automations/foo/memory.md"
```

Wrong:

```bash
pwd && ls SOUL.md USER.md MEMORY.md >/dev/null && printf 'ok'
```

Right:

```bash
AUTO_HOME="${CODEX_HOME:-$HOME/.codex}"
AUTO_MEM="$AUTO_HOME/automations/foo/memory.md"
[ -f "$AUTO_MEM" ] && sed -n '1,220p' "$AUTO_MEM" || true
```

Then, in a separate command, read repo context files.
