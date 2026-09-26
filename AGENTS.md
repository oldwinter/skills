# AGENTS.md

Public, Markdown-first skills library. `CLAUDE.md` is a symlink to this file.

This repo owns reusable Skill implementations only. Device inventory, consumer enablement and routing, automations, personal memory, and install evidence belong to private `oldwinter/general-tasks`; machine and harness config belongs to private `oldwinter/dotfiles`.

## Layout

- A skill is a directory named by its identifier (hyphen-case) with a required `SKILL.md` and optional `references/`, `rules/`, `scripts/`.
- Two layers: category buckets (`base-skills/`, `devops-skills/`, `lenny-skills/`, `meta-skills/`, `obsidian-skills/`, `tools-skills/`) are the classification source of truth; root directories are also installable skill names. A few names exist in both layers and may diverge; README → Standalone Skills lists them.
- Adding, removing, or renaming a root skill means updating the README map; `just check-readme-map` enforces it.

## Skill rules

- Keep every skill usable outside this owner's machines: no credentials, private sessions, personal memory, private hostnames, or hardcoded device paths; use placeholders or public interfaces in examples.
- `SKILL.md` frontmatter is parsed by scripts: `---` delimited, `name:` and `description:` as single-line scalars (no `>` block scalars), no angle brackets in `description`.

## Verify

- `just validate-skill <dir>` for any changed skill; `just validate-skillpack <dir>` for Lenny-style packs (`skillpack.json`, `references/`). Both need PyYAML.
- `just check-readme-map` after structural changes; `just test-sync` when touching `meta-skills/sync-skills-manager` or `scripts/`.
