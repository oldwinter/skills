# Pi Dynamic Workflows To Codex

This package adapts the ideas of [`Michaelliv/pi-dynamic-workflows`](https://github.com/Michaelliv/pi-dynamic-workflows) to Codex skills and goal-oriented work. It does not embed Pi or expose a Pi extension.

## What Pi Provides

Pi's package registers a `workflow` tool. The model writes deterministic JavaScript, and the tool runs it in a sandbox with workflow globals:

- `agent(prompt, opts)`
- `parallel(thunks)`
- `pipeline(items, ...stages)`
- `phase(title)`
- `log(message)`
- `args`
- `cwd`
- `budget`

The runtime fans out to in-memory Pi subagent sessions, streams compact progress, supports abort, and can ask subagents for structured JSON output.

## Codex Adaptation

Codex workflows are coordinated by the parent agent and by whatever tools the current environment exposes:

- Goal tools hold the full objective and completion status.
- Subagent tools run bounded packets in parallel when available and authorized.
- Workflow artifact files provide persistence, reviewability, and resumption.
- Scripts scaffold, verify, and collect packet results.
- Packet expected-output contracts stand in for structured subagent schemas.

## Compatibility Boundary

Do not promise:

- a registered `workflow` tool unless one is actually available
- a JavaScript VM sandbox unless implemented in the current runtime
- automatic in-memory subagent sessions
- persisted/resumable Codex runs beyond the files this package writes

Do promise:

- explicit orchestration
- bounded packets
- approval gates
- fan-out/fan-in when subagent tools exist
- simulated packets when they do not
- auditable integration and verification

## Suggested Prompt Pattern

```text
Use $codex-dynamic-workflows.

Goal: ...
Constraints: ...
Please create a workflow artifact, split work into packets, use subagents where available, integrate results, verify, and report the final evidence.
```
