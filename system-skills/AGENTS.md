# system-skills

## OVERVIEW
Large skills set synced from canonical `~/.claude/skills`, organized into subcategories (AI, Product, DevOps, Tools, etc.).

## STRUCTURE
```
system-skills/
├── <subcategory>/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── references/ | rules/ | scripts/ (optional)
└── sync-skills-manager/            # system↔repo sync tooling + config
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Find a skill by name | `system-skills/**/<skill>/SKILL.md` | Directory name is the skill identifier.
| Understand subcategory boundaries | `system-skills/*-skills/AGENTS.md` | Per-subcategory notes.
| Sync system → repo | `sync-skills-manager/` | `sync-skills.sh pull/auto`.

## CONVENTIONS
- Subcategories are first-level directories ending in `-skills` (plus `sync-skills-manager`).

## ANTI-PATTERNS
- Don’t flatten `system-skills/` — `sync-skills-manager` expects this nesting.
