---
name: agent-autoresearch
description: Autoresearch loop for any coding agent harness (Claude Code, Codex, pi, others with a shell) - repeatedly edit, measure, keep or revert, and log experiments that push one numeric metric (speed, size, score, loss, error count) toward a goal, unattended for hours if needed. Use to start an autoresearch or overnight optimization run, or to check, resume, or report an existing one.
---

# Agent Autoresearch

Karpathy-style autoresearch that runs the same way in every harness. You are the **researcher**: you choose hypotheses and edit code. The bundled **controller** (`scripts/autoresearch.py`, Python 3 standard library) owns everything that must be trustworthy: measurement, the keep-or-revert decision, git commits, and the experiment log. The best result is a **ratchet**: a trial is kept only when the metric improves and the checks pass; every other trial is reverted with its patch saved.

```text
hypothesis -> edit -> trial (measure, gate, keep or revert, log) -> learn -> repeat
```

`<skill-dir>` is the directory containing this file. Before `init`, call the controller as `python3 <skill-dir>/scripts/autoresearch.py <command>` from inside the target repository. `init` writes a launcher, so afterwards call `.autoresearch/ar <command>` from the repository root (or by its absolute path from anywhere); it also works for a fresh context that never saw this skill. `<command> --help` lists every flag.

## Route the request

- **Status or results** of an existing session (`.autoresearch/` exists): run `.autoresearch/ar status`, `log`, or `report` and answer. Start no experiments.
- **Resume**: `.autoresearch/ar status`, then `.autoresearch/ar resume` (add `--more N` or `--budget-minutes M` when a limit stopped it), then go to **Experiment loop**.
- **New session**: **Set up**, then **Experiment loop**.

## Set up

1. **Define the experiment.** Settle the goal, the primary metric and its direction, the measure command, the correctness checks, the editable scope, the protected paths (the evaluator, its data, the tests), and the stopping rule (target, trial limit, time budget, or run until stopped). Infer what the repository and request already answer; ask only for decisions that change the experiment. Unless the user said to just go, show one confirmation:

   ```text
   Goal:    ...
   Metric:  <name> (<lower|higher> is better), measured by `<command>`
   Checks:  `<command>` | none
   Scope:   <paths>        Protected: <paths>
   Stop:    <target | N trials | M minutes | until stopped>
   ```

   Done when every line has a value.

2. **Make the measurement trustworthy.** The measure command prints `METRIC <name>=<number>` lines (a final numeric line also works), exits 0 when it measured, holds the workload and compute budget fixed, and leaves the working tree untouched. When nothing suitable exists, write a measure script outside the scope and protect it. Read [references/measurement.md](references/measurement.md) when you write a measure or checks script, when the metric is noisy (timings), or when the experiments could overfit the benchmark. Done when one manual run prints the metric.

3. **Initialize.** Commit or stash unrelated work, then:

   ```bash
   python3 <skill-dir>/scripts/autoresearch.py init --goal "..." --metric NAME --direction lower \
     --measure "CMD" --checks "CMD" --scope PATH --protect PATH \
     --max-iterations N --budget-minutes M --target X
   ```

   Drop the flags that do not apply. The time budget starts at `init`; once any limit is hit the controller refuses new trials and prints `next: STOP`. `init` creates the branch `autoresearch/<tag>-<date>`, measures the baseline (probing noise on fast benchmarks), and writes the git-ignored `.autoresearch/`: `log.jsonl` (source of truth), `program.md` (the brief), `ideas.md` (the backlog), and `ar`. If it reports a noisy metric, apply its rebaseline suggestion. Done when it prints the baseline.

4. **Write the brief.** Fill in Constraints and Strategy notes in `.autoresearch/program.md`: what produces the metric, where the cost or error comes from (profile it or read the measure output), and the first hypotheses ranked by expected gain. A fresh context resumes from this file. Done when a stranger could start the loop from it.

## Experiment loop

Keep looping without asking whether to continue; the human may be asleep. The loop ends only when the controller prints `next: STOP` (or refuses a trial because the session is stopped or complete) or the user interrupts. In a headless run (`claude -p`, `codex exec`, `pi -p`) a reply without a tool call ends the run, so keep acting until STOP, and get the first trial on the board early. After a context reset, re-orient with `.autoresearch/ar status` and `program.md` before the next trial.

1. **Choose one hypothesis** from evidence: the measure output, profiles, the code, `ideas.md`, earlier verdicts and notes. One coherent idea per trial keeps its effect attributable. When the latest keep removes the reason an earlier discard failed, that discard is a candidate again.
2. **Edit inside the scope.** When a mistake would waste a long measurement, sanity-check cheaply first (compile, one unit test). Screening several variants on a fast private probe is fine, but only `trial` adopts a change, and what the screening ruled out goes into `program.md` or `ar note` so the notebook keeps the dead ends.
3. **Run the trial:**

   ```bash
   .autoresearch/ar trial --description "what changed" --hypothesis "why it should help"
   ```

   Add `--simplification` when the change removes complexity and deserves a keep at equal metric, and `--revisits N` when it retries discard #N because an assumption changed. The verdict belongs to the controller: KEEP commits; DISCARD, CRASH, TIMEOUT, and CHECKS_FAILED revert. The controller owns git, so commits, resets, stashes, and branch switches go through it.
4. **Learn from the verdict.** Write down why a trial lost or surprised you: `.autoresearch/ar note "..."`. When a crashed idea still has merit, `ar restore N`, fix it, and trial again. Park good ideas for later in `ideas.md`. Every few trials, and after each keep, update "What's been tried" in `program.md` with wins and with dead ends plus the reason they failed.
5. Go to 1.

Research judgment:

- **Simplicity criterion.** Weigh complexity against gain. A tiny gain that adds hacky code is not worth keeping (`ar undo --reason "..."` drops the last keep); equal metric with less code is a win.
- **When stuck** (the controller warns after three trials without a keep): re-read the measure output and the code to find where the metric really comes from, combine near-misses, try a structurally different approach, or take a bold swing. Variations of a failed idea are the slowest path.
- **Noise.** When a keep's gain is within about twice the noise floor, run `ar recheck` before building on it.
- **Integrity.** Gains come from the system under test; the measurement, its data, and protected files stay as they are. When the benchmark itself looks wrong, stop and tell the user. Changing the measurement needs the user's agreement and starts a new segment: `ar init --rebaseline ...`.
- **Context hygiene.** Work from the controller's summaries; open full logs in `.autoresearch/logs/` only to diagnose.
- **Long measurements.** When a trial would outlast your shell tool's timeout, run `ar trial ... --detach`, then `ar wait` until the verdict prints.

## Finish

When the session stops or completes, or the user asks for results:

1. Run `.autoresearch/ar report` to write `report.html` and `summary.md`.
2. Tell the user: baseline to best (with percent), trial and keep counts, the top wins, notable dead ends, open ideas, the branch name, and how to land it (commands are in `summary.md`). Merging and branch cleanup stay with the user unless asked.

## Unattended runs

Over many hours a single session can stall, end its turn early, or exhaust its context. The controller can **relay** instead: it launches a fresh headless agent for each batch of trials until the session stops. Prefer it for unattended headless runs, especially with models that tend to end their turn early; it resumes any existing session.

```bash
.autoresearch/ar relay --agent claude    # or codex, pi; --model M; --trials-per-worker 5
.autoresearch/ar relay --agent-cmd 'your-agent-cli -p {prompt_file}'
```

Read [references/harnesses.md](references/harnesses.md) before launching a relay, when running under a harness you have not used with this skill, or when tuning permissions, tool timeouts, hooks, or parallel sessions.
