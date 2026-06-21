# Create Codex Dynamic Workflows Repository

## Goal

Create a public, installable `codex-dynamic-workflows` repository in `/Users/oldwinter` that faithfully adapts the fan-out/fan-in workflow ideas from `Michaelliv/pi-dynamic-workflows` into a Codex skill package.

## Success Criteria

- Root `SKILL.md` is installable by `npx skills`.
- Documentation explains Pi concept mapping and Codex runtime boundaries.
- Helper scripts scaffold, collect, and verify workflow artifacts.
- Tests pass locally.
- GitHub public repository is created with `gh` and pushed.
- The skill installs successfully on this computer from the published repository.

## Current Context

- Reference Pi repo: `Michaelliv/pi-dynamic-workflows`, main `31b2aca0f1cb195aafbfc5e3ee2b8c83ad3f21a2`.
- Reference skill repo: `DannyMac180/skills`, main `5695fa19b9d39b8270025e79633b49a8b863f9a2`.
- Codex subagent support is available in this environment and was used for read-only scouting.

## Constraints

- Do not claim a Pi-style `workflow` tool exists in Codex.
- Avoid copying Pi runtime implementation; write an original Codex skill and cite inspiration.
- Preserve external side-effect safety: create and push only because the user explicitly requested it.

## Risks

- Licensing ambiguity because Pi package metadata says MIT but no root `LICENSE` was present in the cloned repo.
- Skills CLI install behavior may differ for global versus project installs.
- Current Codex session may not reload newly installed skills until a fresh session.

## Approval Required

User explicitly requested public GitHub upload and local install attempt. No additional approval needed for those scoped external actions.

## Work Packets

- `01-discovery`: inspect references, licensing, install expectations.
- `02-execution`: create repository, skill docs, scripts, examples, tests.
- `03-verification`: run tests, install smoke, push, and verify GitHub repo visibility.

## Integration Policy

Parent agent integrates all results. Subagent scouting informs but does not replace direct verification.

## Verification

- `python3 -m unittest discover -s tests`
- `python3 scripts/verify_workflow.py .workflow/create-codex-dynamic-workflows-repo`
- `npx skills@latest add oldwinter/codex-dynamic-workflows -g -y`
- `test -f ~/.codex/skills/codex-dynamic-workflows/SKILL.md`

## Reusable Artifacts

- Root skill package.
- Workflow scaffold scripts.
- This `.workflow/create-codex-dynamic-workflows-repo/` example run.
