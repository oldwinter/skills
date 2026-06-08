# Integration Checklist: create-codex-dynamic-workflows-repo

## 01 Discovery

# Discovery Result
Accepted:
- Pi reference repo is a TypeScript Pi extension with parser/runtime/tool/display/subagent modules and tests.
- User-facing concepts to preserve: `agent`, `parallel`, `pipeline`, `phase`, structured output, progress display, abort, deterministic workflow boundaries.
- Codex adaptation should be a skill plus durable workflow artifacts, not a false claim of a native Pi-style tool.
Risk:
- Pi package metadata declares MIT, but no root `LICENSE` was found in the cloned reference. This repo avoids copying Pi runtime code and includes attribution in `NOTICE.md`.
Verification:
- Reference repos cloned to `/tmp/pi-dynamic-workflows-ref` and `/tmp/dannymac-skills-ref`.

## 02 Execution

# Execution Result
Accepted:
- Created root installable skill package with `SKILL.md`.
- Added Codex-specific references for risk gates, plan schema, validation examples, and Pi comparison.
- Added deterministic Python helper scripts under `scripts/`.
- Added README, NOTICE, MIT LICENSE, example workflow, type hints, and GitHub Actions unittest workflow.
- Added a static Pi-style workflow adapter (`scripts/codex_workflow.py`) and example workflow script.
Decision:
- Root directory is the skill package so `npx skills add oldwinter/codex-dynamic-workflows` can discover `SKILL.md` directly.
Verification:
- File creation completed with `apply_patch`.

## 03 Verification

# Verification Result
Accepted:
- `python3 -m unittest discover -s tests` passed: 3 tests.
- `python3 scripts/collect_results.py .workflow/create-codex-dynamic-workflows-repo --output .workflow/create-codex-dynamic-workflows-repo/integration.md` passed.
- `python3 scripts/verify_workflow.py .workflow/create-codex-dynamic-workflows-repo` passed with 3 packets and 3 results.
- `python3 scripts/codex_workflow.py examples/inspect-project.workflow.js --json` passed and extracted 2 phases plus 2 agent packets.
- `python3 scripts/codex_workflow.py examples/inspect-project.workflow.js --root /tmp/codex-workflow-adapter-smoke` passed and generated packet files.
- `python3 -m unittest discover -s tests` passed after adapter coverage was added: 5 tests.
Verification:
- `gh repo view oldwinter/codex-dynamic-workflows --json nameWithOwner,visibility,url,defaultBranchRef,pushedAt` confirmed `PUBLIC`, default branch `main`, URL `https://github.com/oldwinter/codex-dynamic-workflows`.
- `git status --short --branch` confirmed local `main...origin/main` is clean.
- `npx skills@latest add oldwinter/codex-dynamic-workflows -g -y` installed 1 skill from `https://github.com/oldwinter/codex-dynamic-workflows.git`.
- `npx skills@latest list -g --json` shows `codex-dynamic-workflows` installed globally with agents `Cline`, `Codex`, `Warp`, `Zed`.
- File checks confirmed `~/.agents/skills/codex-dynamic-workflows/SKILL.md` and `~/.codex/skills/codex-dynamic-workflows` exist.
- Installed adapter smoke passed from `~/.agents/skills/codex-dynamic-workflows/scripts/codex_workflow.py`.

## Integration Decisions

Accepted:

Rejected:

Conflicts:

Remaining risks:

Verification still needed:
