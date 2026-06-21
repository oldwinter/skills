# Example: Repository Audit Workflow

Use this as a compact pattern when a user asks for a multi-track repository audit.

## Prompt

```text
Use $codex-dynamic-workflows to audit this repo for broken install instructions, stale scripts, missing tests, and risky external actions.
```

## Packets

### 01-discovery

Objective: Map repository structure, entrypoints, and success criteria.

Expected output: `results/01-discovery.md` with key files, commands, and constraints.

### 02-docs

Objective: Check README and docs for install/run instructions that do not match the repo.

Expected output: `results/02-docs.md` with accepted findings and evidence.

### 03-scripts

Objective: Inspect scripts and just/npm recipes for stale paths, missing dependencies, or unsafe defaults.

Expected output: `results/03-scripts.md`.

### 04-tests

Objective: Run narrow verification and identify missing coverage.

Expected output: `results/04-tests.md` with commands and outcomes.

### 05-integration

Objective: Resolve conflicts, rank findings, and produce final recommendations.

Expected output: `integration.md` and `final-report.md`.
