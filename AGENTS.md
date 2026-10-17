# AGENTS.md

Public, Markdown-first skills library. `CLAUDE.md` is a symlink to this file.

This repo owns reusable Skill implementations only. Device inventory, consumer enablement and routing, automations, personal memory, and install evidence belong to private `oldwinter/general-tasks`; machine and harness config belongs to private `oldwinter/dotfiles`.

## Layout

- A skill is a directory named by its identifier (hyphen-case) with a required `SKILL.md` and optional `references/`, `rules/`, `scripts/`.
- Skills live at the repo root, except Obsidian ones under `obsidian-skills/`. Only skills in use stay on `main`; third-party skills are installed from their upstream, not copied here.
- Retired skills are removed from `main` and listed under README → 归档. `archive/2026-10-13` is the pre-cleanup snapshot tag; anything retired later lives in git history. Restore with `git checkout <ref> -- <path>`.
- Adding, removing, or renaming a skill means updating the README list; `just check` enforces it.

## Skill rules

- Keep every skill usable outside this owner's machines: no credentials, private sessions, personal memory, private hostnames, or hardcoded device paths; use placeholders or public interfaces in examples.
- `SKILL.md` frontmatter is parsed by scripts: `---` delimited, `name:` and `description:` as single-line scalars (no `>` block scalars), no angle brackets in `description`.

## Verify

- `just check` after any change: the README list matches the tree, frontmatter names match directories, and no personal machine paths.
