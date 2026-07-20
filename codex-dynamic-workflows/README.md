# codex-dynamic-workflows

Codex-native dynamic workflow orchestration as an installable skill.

Use it when a task is too broad for a single linear pass: codebase audits, multi-perspective reviews, large migrations, fan-out research, implementation plus verification, or any request that explicitly asks for Codex goal mode, subagents, parallel agents, or Claude Code-style dynamic workflows.

This project is inspired by [`Michaelliv/pi-dynamic-workflows`](https://github.com/Michaelliv/pi-dynamic-workflows), but it does not install a Pi extension or claim a Pi-style `workflow` tool. It maps the same fan-out/fan-in ideas to Codex skills, goal mode, subagent packets, workflow artifacts, and deterministic helper scripts.

## Install

Install as a global skill:

```bash
npx skills@latest add oldwinter/codex-dynamic-workflows -g -y
```

Or install from a local checkout:

```bash
npx skills@latest add /Users/oldwinter/codex-dynamic-workflows -g -y
```

For a project-level install, run the same command inside the target project without `-g`.

## Usage

Ask Codex to use the skill:

```text
Use $codex-dynamic-workflows to audit this repository for stale scripts, broken install instructions, and missing tests.
```

The expected flow is:

1. Restate the goal and success criteria.
2. Scaffold `.workflow/<slug>/`.
3. Split the task into disjoint packets.
4. Use Codex subagents when available and authorized.
5. Simulate packets with isolated notes when subagents are unavailable.
6. Integrate results.
7. Verify the final outcome.

## Workflow Artifact

Create one manually:

```bash
python3 scripts/new_workflow.py "Audit install docs"
```

It creates:

```text
.workflow/audit-install-docs/
|-- plan.md
|-- state.json
|-- orchestration.md
|-- packets/
|-- results/
|-- integration.md
`-- final-report.md
```

Collect packet results:

```bash
python3 scripts/collect_results.py .workflow/audit-install-docs --output .workflow/audit-install-docs/integration.md
```

For cleaner integration drafts, packet results can use second-level sections such
as `## Accepted`, `## Rejected`, `## Conflicts`, `## Decisions`, `## Risks`, and
`## Verification`. The collector groups those sections across packet results and
falls back to checklist-like lines for unstructured notes.

Verify artifact completeness:

```bash
python3 scripts/verify_workflow.py .workflow/audit-install-docs
```

For a final fan-in pass, require every packet listed in `state.json` to have a
non-empty result:

```bash
python3 scripts/verify_workflow.py .workflow/audit-install-docs --require-all-results
```

Verification also checks basic `state.json` consistency: the slug must match the
directory name, packet IDs must be unique, packet files must match state packet
IDs, result paths must live under `results/`, and status values must be known.

## Pi-Style Script Adapter

You can also validate a small Pi-style workflow script and convert its `agent()` calls into Codex packets:

```bash
python3 scripts/codex_workflow.py examples/inspect-project.workflow.js --json
python3 scripts/codex_workflow.py examples/inspect-project.workflow.js --root .workflow
```

The adapter is intentionally static. It parses `export const meta`, literal `phase(...)`, and literal `agent(..., { label })` calls, rejects obvious nondeterministic APIs such as `Date.now()`, `Math.random()`, `new Date()`, and template interpolation, then writes a Codex workflow artifact. It does not execute JavaScript. Existing artifact directories are protected by default; pass `--force` only when you intentionally want to regenerate a recognized workflow artifact.

## Pi Concept Mapping

| Pi dynamic workflows | Codex dynamic workflows |
| --- | --- |
| `export const meta` | `plan.md` and `state.json` |
| `phase(title)` | progress updates and orchestration phases |
| `agent(prompt, opts)` | Codex subagent task or packet note |
| `parallel(thunks)` | independent subagents or isolated packet passes |
| `pipeline(items, ...stages)` | staged packets with fan-out per item |
| structured output | packet expected-output contract |
| live progress display | `state.json`, user updates, final report |
| abort | stop spawning, mark skipped, preserve partial results |
| token budget | agent/time/compute budget and approval gate |

## Development

```bash
python3 -m unittest discover -s tests
python3 scripts/codex_workflow.py examples/inspect-project.workflow.js --root /tmp/codex-workflow-adapter-smoke --force
```

The tests exercise scaffold, verification, and integration helper behavior against temporary workflow directories.

## Status

This is a practical v1 skill package. It ships the Codex orchestration contract, deterministic workflow artifact helpers, and a static Pi-style workflow adapter. It does not ship a JavaScript VM runner or register a native Codex `workflow` tool.

## License

MIT. See `LICENSE` and `NOTICE.md`.
