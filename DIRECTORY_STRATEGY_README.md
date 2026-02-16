# Directory Strategy README

This file documents a practical consolidation plan to make the repository easier to navigate and maintain.

## Current Pain Points

- Same skill names may appear across curated folders and `system-skills/`.
- Some paths exist mainly for compatibility, not as canonical edit targets.
- It is not always obvious where changes should be made first.

## Recommended Canonical Rule

- Canonical synchronized/global skills: edit under `system-skills/`.
- Curated folders (`coding-common-skills/`, `devops-skills/`, `obsidian-skills/`, `writing-skills/`) are presentation/compatibility layers.

## Suggested Phased Cleanup

### Phase 1 (safe, no major moves)

- Keep existing directory layout.
- Add provenance and structure docs (this file + `SKILLS_SOURCES_README.md`).
- Enforce SKILL.md frontmatter validation before sync/push.

### Phase 2 (clarity improvement)

- For duplicate skills, keep one canonical copy in `system-skills/`.
- Replace curated duplicates with symlinks pointing to canonical paths where tooling allows.
- Keep a small compatibility map for case-sensitive/case-insensitive name differences.

### Phase 3 (optional, bigger refactor)

- Introduce a single `catalog/` directory as canonical source.
- Generate curated category views from metadata/manifests (instead of manual copies).
- Keep sync scripts pointed at canonical directory only.

## Practical Checklist Before Large Sync

1. Run `./sync-skills-3way.sh status`.
2. Validate changed skills (frontmatter + naming).
3. Confirm there is no embedded git repository (`git ls-files -s | awk '$1=="160000"'`).
4. Sync and verify again with `./sync-skills-3way.sh status`.
