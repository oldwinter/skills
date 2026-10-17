---
name: loop-kit
description: Set up and check the maintenance-loop suite in a repository. Writes .loop/config.json, the state directory, the LESSONS.md and acceptance-rules templates, the marked block in AGENTS.md, and the tick lock, then verifies the install with doctor. Use when the user asks to set up, install, configure, or check the loops, or when a tick skill stops because the config is missing.
disable-model-invocation: true
---

# Loop kit

The front door of a four-skill maintenance-loop suite. One tick does a slice of
maintenance work and stops; a scheduler starts the next tick. This skill owns
the shared runtime the other three call: the config, the state directory, the
Reply Desk, the templates, the `AGENTS.md` block, `doctor` and the tick lock.

Nothing in the suite reaches the network without a card approved on the Reply
Desk by a human.

`<kit-dir>` below is the directory containing this file — the `loop-kit` skill
directory. It is wherever the suite was installed, for example
`<repo>/.claude/skills/loop-kit` in a Claude Code project, so every invocation
is written against `<kit-dir>` rather than a path that only works in the skills
repository.

## When to use it

- The user asks to set up, install or configure the maintenance loops.
- A tick skill stopped because `.loop/config.json` is missing.
- The user asks whether the loops are ready: run `doctor`.
- A tick reports a lock it cannot take.

## Setup

1. Confirm the working tree is the target repository and the user wants the
   suite installed there. `git rev-parse --show-toplevel` gives the root.
2. Run init:

   ```
   python3 <kit-dir>/scripts/loopkit.py --repo-root <repo> init
   ```

   Init reads `git remote get-url origin` for `repo`, defaults `project` to the
   repository name, and accepts `--repo`, `--project`, `--state-dir`,
   `--lessons`, `--rules`, `--agents`, `--default-branch` and `--force` when the
   user wants something other than the default.
3. Read the doctor rows init printed and resolve every `FAIL` before the user
   arms a scheduler.
4. Show the user the three scheduler lines init printed and the command that
   installs the sibling skills that are missing. Arming a scheduler is the
   user's call.

Init is idempotent. Re-running it rewrites `.loop/config.json` from the file
already there, so keys the user added by hand survive, and it leaves an existing
`LESSONS.md` and rules file untouched.

## Configuration

Everything project-specific lives in `.loop/config.json` in the target
repository. The file is committed; the state directory is never inside the
repository. `references/desk.md` documents the desk, `loopkit.py config` prints
the resolved file.

| Key | Meaning |
| --- | --- |
| `project` | Names the state directory, the worktree prefix and the lock. |
| `repo` | `owner/name`, resolved from the git remote when not given. |
| `defaultBranch` | Branch a tick branches from and merges into. |
| `stateDir` | State, desk cards and locks. `~` is expanded; never in the repo. |
| `lessonsPath` | `LESSONS.md`, written by the nightly review. |
| `rulesPath` | Acceptance rules the review promotes lessons into. |
| `agentsPath` | File whose marked block tells every agent the loops exist. |
| `verifyDoc` | Pointer to how this project verifies a change, or `null`. |
| `worktreeCmd` | Template over `{project}`, `{branch}`, `{slug}`, or `null`. |
| `checks` | Commands a tick must run before it drafts a PR. Empty means ask. |
| `trustedLogins` | Bot logins a tick may treat as trusted reviewers. |
| `windowDays` | The shared lookback knob, in days, for both tick loops that look back. |
| `desk` | `{"kind": "files"}` for the portable desk. |
| `loops` | Per-loop `interval` and `enabled`, plus loop-specific keys. |

`windowDays` is one number read by two skills, so they cannot drift:

- `loop-triage-github` uses it as the recent-issue window: only threads created
  within the last `windowDays` days are the loop's to triage.
- `loop-nightly-review` uses it as the seed range when it backfills a fresh
  `LESSONS.md` (one still carrying
  `<!-- reviewed-through: 0000000 (never reviewed) -->`), and as the cap on how
  far back a backfill may reach.

Both meanings are the same intent: how far back this project considers a thread
or a commit to be current. A tick with no cursor yet falls back to `windowDays`
rather than to "everything".

## One tick

Every tick skill carries the same sections in the same order, and the same
invariants. The canonical wording is in
[references/send-protocol.md](references/send-protocol.md):

1. Preconditions, then the trust boundary.
2. Send what was approved on the desk, re-reading each thread first.
3. Advance state, collect, decide, act.
4. Draft every outbound action as a card, then report and stop.

A tick never posts without an approved card, never posts a draft whose thread
moved, and never retries a card left in `sending` by a tick that died.

## The Reply Desk

Every outbound action exists first as a JSON card in the state directory, and a
static `index.html` renders the ones waiting. The maintainer opens the page,
reads each draft, and approves, edits or drops it.

```
python3 <kit-dir>/scripts/desk.py list --status pending
python3 <kit-dir>/scripts/desk.py approve pr-123 --note "shorten it"
python3 <kit-dir>/scripts/desk.py claim pr-123
python3 <kit-dir>/scripts/desk.py sent pr-123 --url <comment url>
python3 <kit-dir>/scripts/desk.py render
```

`put` refuses to overwrite a card that is `approved`, `sending` or `sent`, so a
loop cannot erase a decision the maintainer already made. `claim` is atomic and
refuses a card that is not approved. Both exit `3` when the state refuses the
operation; `2` is a usage or config error. The full surface is in
[references/desk.md](references/desk.md).

## Templates the kit installs

- [templates/LESSONS.md](templates/LESSONS.md) is the lessons file the nightly
  review maintains: one rule per lesson, then the evidence, with a `Seen Nx`
  count of distinct days.
- [templates/acceptance.md](templates/acceptance.md) is the acceptance-rules
  file, including the table lessons are promoted into after three days.
- [templates/agents-block.md](templates/agents-block.md) is the block init keeps
  in place between `<!-- loop-kit:begin -->` and `<!-- loop-kit:end -->`.

## Scheduling a tick

[references/harnesses.md](references/harnesses.md) gives the scheduler lines for
Claude Code, this harness, cron, systemd and Windows Task Scheduler, plus the
five-minute send check and how to re-arm the event watcher.

## Scripts

`scripts/loopkit.py` takes `init`, `doctor`, `status`, `config` and `lock`, all
with `--repo-root` and `--json` where it makes sense:

```
python3 <kit-dir>/scripts/loopkit.py doctor
python3 <kit-dir>/scripts/loopkit.py status --json
python3 <kit-dir>/scripts/loopkit.py lock acquire --name triage-github
```

`doctor` prints one `PASS`/`WARN`/`FAIL`/`SKIP` row per check and exits non-zero
on any `FAIL`. It looks for the sibling tick skills next to `<kit-dir>` — the
directory `<kit-dir>` lives in, which is `<repo>/.claude/skills` in an installed
project and the repository root in the skills library — never in the target
repository. Pass `--suite-root DIR` to check a different install location.
`lock acquire` exits `3` while another tick holds the lock, and takes over a lock
older than `--stale-seconds` after saying so.

Both scripts are Python 3 standard library only and run on Windows and POSIX.

## Porting notes

[references/porting-readest.md](references/porting-readest.md) records what the
suite took from the original maintenance-loop pull request and what it changed
on purpose, including why the Reply Desk is files rather than a hosted page.
