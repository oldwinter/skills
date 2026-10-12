# Harnesses, relay, and long runs

The method is harness-neutral because every harness offers the two things it needs: a shell tool to call the controller, and files to resume from. This page covers what differs between harnesses.

## Install and invoke

The skill is a plain Agent Skills directory, so any harness that reads `SKILL.md` folders can load it. Install it with `npx skills add oldwinter/skills --skill agent-autoresearch -g`, or link or copy the folder into a skills directory:

| Harness | User skills directory | Project directory | Explicit invocation |
|---|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | `/agent-autoresearch <request>` |
| Codex | `~/.agents/skills/` (also `~/.codex/skills/`) | `.agents/skills/` | `$agent-autoresearch <request>` |
| pi | `~/.pi/agent/skills/` or `~/.agents/skills/` | `.pi/skills/`, `.agents/skills/` | `/skill:agent-autoresearch <request>`, or `pi --skill <dir>` |
| Others (Gemini CLI, OpenCode, Cursor, Amp, Droid) | their skills directory | their project directory | name the skill in the request |

Codex specifics: `agents/openai.yaml` disables implicit invocation, so Codex leaves the skill out of its automatic list and loads it only on an explicit `$agent-autoresearch`. Codex reads a project's `.agents/skills/` only when the project is trusted (`[projects."<path>"] trust_level = "trusted"` in `~/.codex/config.toml`, or `-c 'projects."<path>".trust_level="trusted"'` for one run). When a harness lists many skills, it may show this one by name only; an explicit invocation still loads it in full.

## Headless one-shot runs

Start an inline session without an interactive terminal (run from the target repository):

```bash
claude -p --dangerously-skip-permissions "/agent-autoresearch <request with limits>"
codex exec --dangerously-bypass-approvals-and-sandbox '$agent-autoresearch <request with limits>'
pi -p --skill <skill-dir> "/skill:agent-autoresearch <request with limits>"
```

A headless run ends when the model replies without a tool call, which some models do long before the controller says stop. When that happens the session is intact: continue it with a relay (below), or open an interactive session and ask it to resume.

## Shell tool timeouts

A trial blocks until measuring finishes, and each harness bounds a tool call differently:

- **Claude Code**: Bash calls default to 2 minutes and can be raised to 10 minutes per call. Pass a timeout above the measure time.
- **Codex**: long commands keep running and are polled; a trial can block for as long as it needs.
- **pi**: the bash tool has no default timeout.

When a measurement can outlast the tool limit, use `ar trial ... --detach`, then `ar wait --timeout 500` until the verdict prints. A detached trial still holds the session lock, so no second trial can start.

## Permissions

The loop runs the measure command and git writes for hours without a human to approve each call. Work on the session branch in a dedicated checkout or worktree, and treat the measure, checks, and hooks commands as code you have reviewed. Interactive sessions need approval to run shell commands and write files in that repository, either granted up front or through the harness's auto-approve mode. Headless runs need an explicit flag, listed below. Sandboxes that make `.git` read-only break keep commits; give the controller write access to the repository's git directory.

## Relay: fresh agents in a loop

`ar relay` makes the controller the driver. Each round it:

1. stops if the session is stopped or complete;
2. writes a worker prompt to `.autoresearch/relay/worker-NNN.prompt.md`: goal, metric, best so far, the controller path, and the loop steps;
3. runs one headless agent with that prompt (stdin by default) and logs its output to `worker-NNN.log`;
4. evaluates any edits the worker left without a trial, so the next worker starts clean;
5. stops after two workers in a row run no trial (inspect their logs).

Every worker starts with a fresh context, orients from `status` and `program.md`, runs up to `--trials-per-worker` trials (default 5), records what it learned in `program.md`, and exits. The loop therefore survives context limits, stalled sessions, and model hand-offs, and can mix harnesses: run a few rounds with one agent, then continue with another.

| `--agent` | Command run per worker (prompt on stdin) |
|---|---|
| `claude` | `claude -p --dangerously-skip-permissions` |
| `codex` | `codex exec --dangerously-bypass-approvals-and-sandbox -` |
| `pi` | `pi -p` |

`--model M` adds the preset's model flag. For any other CLI, pass a shell template with `--agent-cmd`. The prompt goes to stdin unless the template contains `{prompt}` (the prompt as one quoted argument) or `{prompt_file}` (its path). Check the CLI's own `--help` for its non-interactive and auto-approve flags, for example `--agent-cmd 'gemini --yolo -p {prompt}'`.

Run a relay in the background and stop it cleanly:

```bash
nohup .autoresearch/ar relay --agent codex > .autoresearch/relay.out 2>&1 &
.autoresearch/ar status            # progress at any time
.autoresearch/ar stop --reason "enough for today"    # or: touch .autoresearch/STOP
```

The current worker finishes its trial; the relay then exits. `--worker-timeout` (default 3600 s) bounds a hung worker.

## Inline continuation aids

An inline session (the agent loops in its own context) works everywhere. Harness features that keep it going longer are optional:

- **Codex**: when Goal tools are available, a Goal whose objective names the session (metric, branch, stop rule) keeps Codex working across turns until the controller reports stop.
- **Claude Code and pi**: automatic compaction summarizes old turns. The session files carry the state, so after compaction re-read `ar status` and `program.md`.
- Any harness: when a session ends early, resume with `.autoresearch/ar status` and continue, or switch to a relay.

## Parallel sessions

One session owns one working tree. To explore in parallel, give each agent its own worktree and branch:

```bash
git worktree add ../repo-ar2 -b autoresearch-base-2
```

Each worktree gets its own `.autoresearch/`. Compare their best results, then carry the winner forward. Timing metrics suffer when sessions share CPUs.

## Hooks

Executables named `after` or `before` (any extension, such as `after.sh`) in `.autoresearch/hooks/` run after every trial with a JSON payload on stdin. `after` gets the trial entry; `before` gets the next run number and the last entry; both get a session summary (goal, metric, direction, baseline, best, run count). Their stdout, up to 4 KB, is printed under the trial verdict, so it reaches the agent in any harness. Uses include notifications on a new best, tagging winning commits, external search for the next idea, or a nudge after repeated failures. Hooks time out after 30 seconds.
