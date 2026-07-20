---
name: codex-dynamic-workflows
description: Plan and run Codex-native dynamic workflows for complex tasks that benefit from explicit orchestration, goal mode, subagents or simulated work packets, approval gates, integration, verification, and reusable workflow artifacts. Use when the user invokes this skill, asks for dynamic workflows, subagents, parallel agents, swarm-like work, Goal Maker orchestration, large audits, migrations, multi-track research plus implementation, or Claude Code-style fan-out/fan-in workflows.
---

# Codex Dynamic Workflows

Use this skill to turn a large task into a supervised Codex workflow: define a success contract, scaffold a durable workflow artifact, use goal mode when sustained execution is requested, fan out disjoint packets to Codex subagents when available, integrate results, verify the outcome, and save reusable recipes when the pattern is worth keeping.

This skill is inspired by `pi-dynamic-workflows`, but it is Codex-native. Do not claim a Pi-style `workflow` tool exists unless the current environment exposes one. When Codex subagent tools are unavailable, simulate the fan-out with isolated packet notes under `.workflow/<slug>/results/`.

## Decision Rule

Use dynamic orchestration when at least two are true:

- The task has independent research, coding, review, migration, QA, docs, or design tracks.
- An explicit success contract would reduce drift.
- The task has risk: destructive edits, external writes, deploys, secrets, production data, billing, user accounts, many agents, or broad repo changes.
- Verification benefits from a separate pass from implementation.
- The workflow could become a reusable recipe.
- The user explicitly asks for a workflow, subagents, parallel agents, a swarm, Goal Maker, or Claude Code-style dynamic workflows.

For a small one-shot task, do the task directly and mention that workflow orchestration was unnecessary.

## Operating Contract

When using this skill:

1. Restate the goal and verifiable success criteria.
2. Create or update a workflow artifact before delegating.
3. Ask approval before risky, expensive, external, or destructive steps.
4. Enter goal mode when the user explicitly requests a sustained goal and goal tools are available.
5. Split work into disjoint packets with clear ownership.
6. Spawn subagents only when the environment exposes a subagent runner and the user has authorized delegated or parallel agent work.
7. Keep immediate blocking work local; delegate bounded sidecar work.
8. Integrate results explicitly; never paste raw subagent dumps as the final answer.
9. Verify with checks matched to the blast radius.
10. Save durable recipes only when they will help future work.

## Pi Concept Mapping

`pi-dynamic-workflows` uses deterministic JavaScript with globals such as `agent`, `parallel`, `pipeline`, `phase`, `log`, `args`, `cwd`, and `budget`. In Codex, map those ideas like this:

| Pi concept | Codex-native equivalent |
| --- | --- |
| `export const meta` | `plan.md` goal, criteria, constraints, risks |
| `phase(title)` | plan checklist section and progress updates |
| `agent(prompt, opts)` | bounded subagent task or packet note |
| `parallel(thunks)` | multiple independent subagent tasks, or isolated packet passes |
| `pipeline(items, ...stages)` | staged packet sequence with fan-out per item |
| structured output schema | packet expected output contract |
| live progress display | `state.json`, plan updates, concise user updates |
| abort/cancel | stop spawning, mark running packets skipped, preserve partial results |
| token budget | max agent count, time/compute budget, approval gate |

For teams that already draft Pi-style workflow scripts, use the static adapter:

```bash
python3 /path/to/codex-dynamic-workflows/scripts/codex_workflow.py workflow.js --root .workflow
```

It validates literal `meta`, `phase()`, and `agent()` calls, rejects obvious nondeterminism, and converts agent calls into Codex packet files. It does not execute JavaScript.
Existing artifact directories are protected by default; pass `--force` only when intentionally regenerating a recognized workflow artifact.

## Workflow Artifacts

Prefer creating a local run directory:

```text
.workflow/<slug>/
|-- plan.md
|-- state.json
|-- orchestration.md
|-- packets/
|-- results/
|-- integration.md
`-- final-report.md
```

Scaffold it with:

```bash
python3 /path/to/codex-dynamic-workflows/scripts/new_workflow.py "Task title"
```

Keep `plan.md` human-readable. Use `state.json` for packet IDs, approval state, status, and verification evidence. Use `orchestration.md` as the executable mental model: phases, branching rules, packet prompts, and stop conditions.

## Orchestration Plan

Draft a concise plan with:

```text
Goal:
Success criteria:
Current context:
Constraints:
Risks:
Approval required:
Workflow artifact path:
Work packets:
Integration policy:
Verification:
Reusable artifacts:
```

Do not over-plan obvious work. The plan should be detailed enough to guide delegation and verification, not a substitute for execution.

## Approval Gates

Ask one clear approval question before:

- deleting, overwriting, mass-renaming, force-pushing, or rewriting history
- deploying, publishing, emailing, posting, creating public resources, or mutating external systems
- running migrations, broad codemods, or dependency upgrades
- touching credentials, secrets, billing, production data, customer data, or user accounts
- spawning many agents, running expensive jobs, or consuming unusual compute
- making changes outside the requested workspace

If approval is denied or unavailable, continue only with safe read-only planning, local drafts, dry runs, or non-destructive checks.

Read `references/risk-gates.md` when risk is unclear.

## Goal Mode

If goal mode tools are available and the user has asked for sustained execution, create or continue a goal with the full objective. Keep the objective intact; do not shrink it to the next step. Update the goal only when the overall objective is complete or genuinely blocked.

Do not enter goal mode for a small one-shot task, a purely advisory discussion, or a plan-only request.

## Work Packets

Each packet must be self-contained:

```text
Packet ID:
Objective:
Context:
Files / sources:
Ownership:
Do:
Do not:
Expected output:
Verification:
Stop condition:
```

Prefer disjoint ownership:

- codebase discovery
- dependency or API research
- implementation slice
- tests and fixtures
- docs and examples
- UX or product review
- security or risk review
- final verification

For code-edit packets, assign non-overlapping files or modules. Tell workers they are not alone in the codebase, must not revert others' edits, and must adapt to concurrent changes.

## Subagents

When a Codex subagent runner is available:

- Spawn only concrete, bounded, materially useful subtasks.
- Keep immediate blocking work local.
- Delegate sidecar work that can run while the main agent makes progress.
- Avoid duplicate work across agents.
- Ask workers to edit directly only when their write scope is disjoint and clear.
- Wait for subagents only when their result is needed for the next critical-path step.
- Close agents when they are no longer needed.

When no subagent runner is available:

- Simulate the swarm with isolated packet passes.
- Read only packet-relevant files during each pass.
- Write packet notes under `results/`.
- Integrate only after packet outputs are separate.

Prefer these packet result sections when they apply:

```text
## Accepted
## Rejected
## Conflicts
## Decisions
## Risks
## Verification
```

## Integration

After packets complete, synthesize:

```text
Accepted:
Rejected:
Conflicts:
Decisions:
Final changes:
Remaining risks:
Verification evidence:
```

Resolve conflicts explicitly. If packets disagree, inspect authoritative sources before choosing.

Use:

```bash
python3 /path/to/codex-dynamic-workflows/scripts/collect_results.py .workflow/<slug> --output .workflow/<slug>/integration.md
```

`collect_results.py` groups the packet result sections above into an integration
draft and falls back to checklist-like lines for unstructured notes.

## Verification

Run the narrowest reliable checks first, then broaden as risk warrants:

- unit tests for touched code
- typecheck or lint
- build
- browser or UI smoke test
- script dry run
- source citation check
- migration dry run
- install smoke test
- manual checklist for non-code work

Use:

```bash
python3 /path/to/codex-dynamic-workflows/scripts/verify_workflow.py .workflow/<slug>
```

This verifies required files, required directories, JSON readability, known
state keys, matching workflow slug, unique packet IDs, matching packet files,
known status values, and valid relative `results/*.md` paths.

For final fan-in, prefer:

```bash
python3 /path/to/codex-dynamic-workflows/scripts/verify_workflow.py .workflow/<slug> --require-all-results
```

Report skipped checks honestly. Do not treat a workflow as complete until evidence proves the original success criteria.

## Reusable Recipes

When a run produces a useful pattern, save a concise recipe in a project-appropriate place, such as `.workflow/recipes/<name>.md` or a docs folder. Include:

- trigger
- plan shape
- packet list
- verification checklist
- known risks

Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.

## References

- Read `references/pi-comparison.md` when adapting Pi dynamic workflow ideas to Codex.
- Read `references/plan-schema.md` when a machine-readable workflow plan is useful.
- Read `references/risk-gates.md` before risky or ambiguous operations.
- Read `references/validation-examples.md` when testing or improving this skill.
