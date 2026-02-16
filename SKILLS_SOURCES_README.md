# Skills Sources README

This repository aggregates skills from multiple upstream sources and local customizations.

## Primary Sources

| Source Type | Location in This Repo | Upstream Address |
|---|---|---|
| Agent skills standard and tooling reference | repo-wide conventions (`AGENTS.md`, sync scripts) | https://agentskills.io/home |
| Global multi-agent install/distribution workflow | repo-wide conventions and install commands | https://github.com/vercel-labs/skills |
| Refound/Lenny skill content imports (many `system-skills/*`) | mostly `system-skills/` | https://refoundai.com/lenny-skills/ |
| Community/custom operational skills | mixed directories | local/custom origin (varies per skill) |

## Vendored Skills (Submodule Replaced with Files)

The following path is now vendored as regular files (not a git submodule):

- Path: `writing-skills/humanizer-zh`
- Upstream repo: https://github.com/op7418/Humanizer-zh
- Upstream commit captured during vendorization: `eb6340162fc41cf1892875fa441f453bdea0dba1`
- Vendorization date: 2026-02-16

## Maintenance Notes

- When updating a vendored skill, record:
  - upstream URL
  - upstream commit/tag
  - import date
- Keep source attribution in this file and (if needed) in the skill's local `README.md`.
- Prefer one canonical source directory for synced skills (`system-skills/`) to reduce drift.
