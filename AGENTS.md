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
- `SKILL.md` frontmatter is parsed by scripts: `---` delimited, `name:` and `description:` as single-line scalars (no `>` block scalars), no angle brackets in `description`.
- `agents/openai.yaml`, when present, advertises the display name, default prompt, and implicit-invocation policy to harnesses that read it; `disable-model-invocation: true` marks a skill explicit-only. Both are harness-advisory metadata, not behavior.

## Verify

- `just check` after any change: the README list and statistics match the tree, frontmatter name/description/resource links are valid, no personal machine paths appear, and the check scripts' fixture tests pass. On Windows run shell checks through `just` or Git Bash; the `bash` first on PATH may be WSL, which does not share the filesystem.
- `just doctor` checks the local toolchain (python3, bash, git, just) and the `CLAUDE.md` symlink; `PASS`/`WARN`/`FAIL`/`SKIP` rows, nonzero exit on any `FAIL`. No env file or services exist in this repo, so the doctor's service inventory is intentionally empty.
