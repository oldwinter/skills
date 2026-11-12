---
name: orch-claude-pi-codex
description: Claude architects and commands, pi workers implement in parallel, codex reviews independently, Claude synthesizes. Use for /orch-claude-pi-codex, multi-file features, parallel implementation that needs a separate reviewer, or when the user asks for the Claude→pi→codex→Claude orchestration pattern.
---

# orch-claude-pi-codex

Role-specialized Orca orchestration. Claude is the architect and commander; pi workers implement in parallel; codex reviews independently; Claude synthesizes and reports.

Read `references/paradigms.md` when choosing a different shape. Read `references/task-specs.md` before writing a spec.

## Preconditions

- Orca is reachable: `orca status` reports `runtimeState: ready`.
- Agents `claude`, `pi`, and `codex` are enabled in Orca.
- You are the root coordinator. A dispatched worker must not use this skill.

## 1. Architect

Read the repo's `AGENTS.md` and every file the change touches. Write a brief to `.orca-orch/<run_id>/brief.md` with:

- Goal and acceptance criteria.
- Work units: name, owned files, verification command, worktree choice.
- Review focus: the risks codex must check.

Choose `current` when units own disjoint files. Choose `new-child` per unit when they overlap or need isolation.

Completion: every unit has owned files and a verification command; no two units own the same file unless their worktrees are isolated.

## 2. Create the Run and tasks

```sh
orca orchestration run-create --objective "<goal>" --json
orca orchestration task-create --spec "<unit spec>" --task-title "<unit>" --json
orca orchestration task-list --ready --brief
```

Use `--deps '["<task_id>"]'` only for real ordering.

Completion: every unit is a task; the first ready wave is listed.

## 3. Dispatch pi workers

```sh
orca orchestration worker-start --task <task_id> --worktree current --agent pi --task-title "<unit>" --json
```

For overlapping files: `--worktree new-child --name <unit>`. Start every independent worker, then end your turn. Orca wakes you on `worker_done`.

Completion: every ready task has a dispatch ID and `state: ready`.

## 4. Collect and verify

For each `worker_done`, read the report and check the evidence yourself: files exist, the verification command ran, no out-of-scope edits. Use `worker-read --dispatch <id>` when the report is thin.

A failed report is not a completed task. Retry the same task with `--retry-of`, or stop and report the blocker. Follow a failed start's `next` action; release reclaimable terminals.

Completion: every unit has a verified report or a recorded failure.

## 5. Codex review gate

Start one codex reviewer with a spec that names the actual diff and the acceptance criteria. The reviewer must see the changes: review in the coordinator's worktree when units used `current`; collect child-worktree changes into a review worktree when units used `new-child` (see `references/task-specs.md`).

The review returns findings ranked by severity, each with `file:line` and a concrete failure scenario, plus a verdict: `approve` or `request changes`.

Completion: codex returns a verdict with evidence.

## 6. Fix loop

On `request changes`, send each finding to the pi worker that owns the file as a follow-up task. Re-review after the fixes. Cap the loop at two rounds; at the cap, give the user the open findings.

Completion: codex approves, or the cap is reached and the user has the findings.

## 7. Synthesize

Report per task: outcome, evidence (files, commands, review verdict), open blockers. Keep the brief and the review report as the durable record. Release workers; remove child worktrees only with the user's confirmation.

Completion: the user has the final report with evidence and blockers.

## Guardrails

- One self-contained spec per worker: target, change, constraints, evidence of done.
- pi implements, codex reviews, Claude decides. The owning pi worker makes every edit the review requests.
- `current` for disjoint files, `new-child` for overlap. A child worktree costs setup and a merge.
- End your turn after dispatching; Orca wakes you on `worker_done`.
- A failed outcome stays failed: retry the same task or report the blocker.
- Cap the review loop at two rounds; at the cap, give the user the open findings.
