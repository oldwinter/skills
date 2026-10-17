---
name: agent-harness-repair
description: "Diagnose and repair a local coding-agent CLI or harness install (Claude Code, Codex, DeepSeek Harness/DSH, Cursor, Droid, pi, Grok and similar) when the harness itself breaks: a self-update that never reaches the latest version, a failed global npm or pnpm install or expired auth, a hook that errors on every tool call, a command not found because PATH or shims point at a stale install, a config or JSON settings file that no longer parses, an MCP server that fails to start, or a sandbox or permission step that blocks entry. Use for the harness executable, installer, version, config, hooks, credentials, and launch path. Repository environment and service checks belong to add-just-doctor; application bugs belong to diagnosing-bugs."
---

# Agent Harness Repair

Restore one local coding-agent CLI or harness to its last known-good state with the smallest reversible change. The command that fails today is the acceptance test: the repair is done only when that exact command passes again.

Start read-only. Diagnose before changing anything, change one layer per round, and back up every file before rewriting it.

## 1. Map The Harness And Install Topology

Identify which harness is broken and how it got installed before touching it.

```bash
command -v <harness>; which -a <harness> 2>/dev/null   # macOS / Linux
where <harness>                                        # Windows cmd
Get-Command <harness> -All                             # Windows PowerShell
<harness> --version
```

Record in one table:

- harness name and executable path;
- install method: native installer, package manager (npm, pnpm, yarn, brew, winget, apt), app-managed updater, or plugin/bundle runtime;
- package owner and install prefix (`npm ls -g --depth=0`, `pnpm list -g`, `brew list --versions <formula>`);
- current version and last known-good version;
- config/home dir `<harness-home>`, log dir, and credential store path (path only, never contents);
- PATH order, shims, the shell rc or profile that adds the harness, and any alias or function that shadows it.

Flag every duplicate: more than one executable on PATH, a shim next to a native binary, a second copy under another prefix, an alias or function override.

Completion criterion: the table is filled, duplicates are flagged, and the exact failing command with its before-version is recorded for the after-comparison.

## 2. Capture The Failure

Reproduce with the smallest real invocation: `<harness> --version`, the self-update command, a session start, or one tool call that triggers the hook.

For each reproduction record:

- exact command, working directory, shell/terminal, and one-shot vs interactive;
- exit code and the first error line copied verbatim;
- relevant log path and timestamp (check `<harness-home>` logs and OS app log dirs);
- whether the failure persists in a clean shell, another working directory, and another terminal.

Completion criterion: a command that fails on demand, its verbatim output, and a log path. If it is not reproducible, state what changes it and which environmental condition (shell init, cwd, IDE, proxy) differs.

## 3. Classify The Failure

Pick one class before fixing: install/update, package-manager/auth, hooks, PATH/shim, config parse, MCP, auth/session, sandbox/permission, connectivity. Mixed symptoms mean several checkpointed rounds, not one reinstall.

| Trigger condition | Evidence to collect | First fix | Fallback if still broken |
| --- | --- | --- | --- |
| Update reports success but the version is unchanged, or the updater errors midway | before/after version, update log, install method and prefix, free disk, permission error | update through the recorded install method; clear a partial download or update cache | reinstall the same version over the existing install without uninstalling; pin the last known-good version |
| Global npm/pnpm install fails with E404, EACCES, ETIMEDOUT, or token expired | error code, configured registry, scoped registry in the rc file, auth presence (never the value), proxy variables | fix registry or auth config for the recorded manager, then rerun the exact install command | use the harness native installer or a user-level prefix and rerun |
| Hook errors on tool use, for example a PreToolUse hook error | hook config file and line, hook command, stderr and exit code, whether the hook binary exists | make the config valid and neutralize only the failing hook with a backup | remove the failing hook entry after backup, or repair its script and retest |
| Settings or JSON config no longer parses | exact parse message, path and offset, newest backup | minimal syntax fix or restore the last backup | move the file aside so defaults regenerate, then re-add user entries one at a time |
| Command not found, or an old version answers | `which -a` output, PATH order, shim content, shell rc edits, every install prefix | reorder PATH or regenerate shims in the file that created them | consolidate to one install method, then repair the launcher entry |
| Auth or session rejected after update or reinstall | credential store kind (keychain, file, env), expiry metadata without secret, account identity | rerun the harness login/auth command interactively | recreate the token in the provider UI, then configure an env pointer or store entry |
| MCP server fails to start | MCP config path, server command and args, spawn error, server name | fix the command, args, and environment variable names | disable that server entry with a backup, verify the harness starts, repair later |
| Sandbox or permission denial blocks entry | exact denial text, path, platform policy, whether the denial is by design | repair only the proven permission entry using platform docs | stop and hand off to sandbox-specific tooling; keep enforcement intact |
| Companion CLI or remote endpoint probe fails | endpoint and proxy, TLS/HTTP status, auth probe result | fix proxy or network config, or restart the documented local service | run the vendor connectivity check and escalate with sanitized evidence |

Keep the original log and error text as evidence; do not paraphrase an error code.

## 4. Choose The Minimal Fix

Work from cheapest to most invasive: config syntax, then install metadata or regeneration, then package layer, then reinstall. Prefer the harness documented repair or doctor command when one exists. Change only the layer the evidence points at.

Completion criterion: a one-sentence diagnosis naming class, layer, and the single planned change, plus the evidence line it rests on.

## 5. CHECKPOINT — Approve Risky Repair

STOP before any action in this list and get explicit approval:

- uninstall or force-reinstall a harness or global package;
- rewrite, replace, or delete hook, permission, MCP, or auth config;
- change credential state (logout/login, revoke or recreate a token);
- use sudo, administrator, or OS-level elevation;
- delete plugins, chat history, session data, or user config.

Present in the approval request: the diagnosis line, exact commands, files to change, backup path, rollback line, and expected blast radius.

Back up before touching: copy each config file to `<config-file>.bak-<timestamp>` (or `<harness-home>/backups/`), record checksums, and write the exact rollback command. A repair without a written rollback line is not approved.

If approval is unavailable, stop at a dry-run report and mark the repair blocked, naming the pending action.

## 6. Safety Rules

- Print secret names and presence only. Never echo tokens, cookies, API keys, session files, or the full contents of an auth or credential file.
- Read-only evidence first; one layer per round; preserve plugins, chat history, session state, and user config unless the request explicitly includes their removal.
- No sudo or admin escalation by default: request it only when evidence proves a permission problem a user-level install cannot fix.
- No blind global uninstall or force-reinstall; repair in place, or reinstall the same version over the existing install.
- Use placeholders in every published command: `<harness>`, `<harness-home>`, `<install-prefix>`, `<config-file>`, `<log-path>`. Never hardcode a device path, username, or hostname.
- Evidence over claims: a repair is unproven until the real failing command is rerun.

## 7. Apply And Verify

Apply the planned change, then rerun the exact failing command from section 2. Prove the harness still works end to end: start one session or make one real tool call, and recheck `<harness> --version` against the intended version.

Completion criterion: the failing command passes, the version equals the intended version, the second lifecycle signal passes, and stdout/stderr contain no secrets.

If the rerun still fails, revert with the recorded rollback line, reclassify with the new evidence, and take the next round. Never stack a second unverified fix on top of the first.

## 8. Report The Repair

Hand off:

- harness, install method, and home/config dir;
- before/after version, plus the exact failing command with its verbatim first error;
- failure class and the evidence that established it;
- commands run, in order;
- changed files with backup path and exact rollback line;
- residual risks or follow-ups (pinned version, pending auth expiry, duplicate install left in place);
- if verification was impossible: the exact blocker and the evidence still missing.

Separate "repair implemented" from "harness verified": the report is complete only when the acceptance command result is stated explicitly.
