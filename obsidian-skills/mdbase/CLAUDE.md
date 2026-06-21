# mdbase-skill development

This repository contains the **mdbase** Agent Skill. The skill itself is defined in `SKILL.md` with its specification in `references/spec.md`.

When making changes to this repo:

- `SKILL.md` — Agent Skills entry point; keep under 500 lines
- `references/spec.md` — Full mdbase specification; the source of truth for all rules
- `adapters/` — Self-contained files for tools without Agent Skills support; must embed both instructions and spec
- Keep adapter files in sync with `SKILL.md` + `references/spec.md` when making changes
