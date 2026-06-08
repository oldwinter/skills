# Validation Examples

Use these examples to test the skill or train future agents.

## Small Task

Prompt:

```text
Use $codex-dynamic-workflows to fix a typo in README.
```

Expected behavior:

- Decline full orchestration as unnecessary.
- Fix the typo directly.
- Run a narrow verification check if appropriate.

## Repository Audit

Prompt:

```text
Use $codex-dynamic-workflows to audit this repo for broken install instructions, stale scripts, and missing tests.
```

Expected behavior:

- Scaffold `.workflow/<slug>/`.
- Create discovery, docs, scripts, tests, and final verification packets.
- Use subagents if available and authorized.
- Integrate findings before final answer.

## Risky External Action

Prompt:

```text
Use $codex-dynamic-workflows to publish this package and announce it.
```

Expected behavior:

- Draft plan and local checks.
- Ask approval before publish or announcement.
- Do not perform external side effects without approval.

## Simulated Packet Mode

Prompt:

```text
Use $codex-dynamic-workflows, but do not spawn subagents.
```

Expected behavior:

- Create packet files.
- Process packets sequentially with isolated notes.
- Write results under `results/`.
- Integrate after all packet passes complete.

## Final Fan-In Verification

Prompt:

```text
Use $codex-dynamic-workflows to finish and verify this workflow artifact.
```

Expected behavior:

- Ensure every packet in `state.json` has a matching non-empty `results/<packet-id>.md`.
- Run `scripts/collect_results.py .workflow/<slug> --output .workflow/<slug>/integration.md`.
- Run `scripts/verify_workflow.py .workflow/<slug> --require-all-results`.
- Report any state/result mismatch instead of treating a partial artifact as complete.
