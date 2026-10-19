# AGENTS.md

Public, Markdown-first skills library. `CLAUDE.md` is a symlink to this file.

This repo owns reusable Skill implementations only. Device inventory, consumer enablement and routing, automations, personal memory, and install evidence belong to private `oldwinter/general-tasks`; machine and harness config belongs to private `oldwinter/dotfiles`.

## Layout

- A skill is a directory named by its identifier (hyphen-case) with a required `SKILL.md` and optional `references/`, `rules/`, `scripts/`, `agents/` (harness metadata), `tests/`, `examples/`; forked skills also carry `LICENSE` and `NOTICE.md`.
- Skills live at the repo root, except Obsidian ones under `obsidian-skills/`. Only skills in use stay on `main`; third-party skills are installed from their upstream, not copied here.
- Retired skills are removed from `main` and listed under README → 归档. `archive/2026-10-13` is the pre-cleanup snapshot tag; anything retired later lives in git history. Restore with `git checkout <ref> -- <path>`.
- Adding, removing, or renaming a skill means updating the README list; `just check` enforces it.

## Skill rules

- Keep every skill usable outside this owner's machines: no credentials, private sessions, personal memory, private hostnames, or hardcoded device paths; use placeholders or public interfaces in examples.
- `SKILL.md` frontmatter is parsed by scripts: `---` delimited, `name:` and `description:` as single-line scalars (no `>` block scalars), no angle brackets in `description`. A description containing `: ` must be quoted: an unquoted one is invalid YAML, and the install CLI skips that skill silently, so the install looks like it worked while the skill is missing.
- `agents/openai.yaml`, when present, advertises the display name, default prompt, and implicit-invocation policy to harnesses that read it. The checker validates it when present: `interface.display_name` / `interface.short_description` / `interface.default_prompt` (which must invoke `$<skill-name>`) and a boolean `policy.allow_implicit_invocation` that must agree with the SKILL.md marker (see Skill invocation).

## Skill invocation

Every skill is exactly one of two kinds, and the split is mechanical so a new skill cannot drift:

- **自动引用 / model-invoked** — the model may fire it on its own. Omit `disable-model-invocation` from `SKILL.md` frontmatter and set `policy.allow_implicit_invocation: true` in `agents/openai.yaml`.
- **手动引用 / user-invoked** — only the human can reach it, by typing `/name` or `$name`; no other skill can call it. Set `disable-model-invocation: true` in `SKILL.md` frontmatter and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

Both markers always agree — a skill is user-invoked in every harness or in none — and `just check` enforces the pairing, including that a user-invoked skill ships an `agents/openai.yaml`. This mirrors the [mattpocock/skills](https://github.com/mattpocock/skills/blob/main/.agents/invocation.md) convention.

Decide the kind when you add or edit a skill, by one test: **could the model usefully reach for this autonomously?** If yes, it is model-invoked (the default). Mark it user-invoked only when auto-firing would be wrong or unsafe — the skill performs an irreversible or outward-facing action (commit, push, merge, post, spend), starts a long unattended run, or must be a command the human starts on purpose.

The `description` follows the kind: a model-invoked skill keeps trigger phrasing ("Use when …") so auto-invocation fires; a user-invoked skill reads human-facing — a one-line summary, with the trigger list stripped. Group both in the README under 自动引用 / 手动引用.

## Verify

- `just check` after any change: the README list and statistics match the tree, frontmatter name/description/resource links are valid, no personal machine paths appear, and the check scripts' fixture tests pass. On Windows run shell checks through `just` or Git Bash; the `bash` first on PATH may be WSL, which does not share the filesystem.
- `just doctor` checks the local toolchain (python3, bash, git, just) and the `CLAUDE.md` symlink; `PASS`/`WARN`/`FAIL`/`SKIP` rows, nonzero exit on any `FAIL`. No env file or services exist in this repo, so the doctor's service inventory is intentionally empty.
- `.claude/skills/verify/` is project-local verification tooling, not a published skill: it drives the real install path (`.scratch/` workspace, evidence under `.scratch/verify-evidence/`) and the gates above, with its feature map in `features/`. `.agents/skills/verify` is a local junction so DeepSeek Harness discovers the same bundle; it is not committed.
