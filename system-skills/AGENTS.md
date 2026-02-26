# system-skills

## OVERVIEW
Legacy container directory. Category content has been promoted to repo-root `*-skills` directories.

## STRUCTURE
```
system-skills/
└── sync-skills-manager/   # sync tooling + config
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Find skills by category | `<repo-root>/*-skills/<skill>/SKILL.md` | Repo-root categories are canonical.
| Sync repo → runtime installs | `sync-skills-manager/` | `sync-skills.sh push/link-all`.

## CONVENTIONS
- Keep sync tooling under `system-skills/sync-skills-manager/`.
- Prefer repo-root categories for all new/moved skills.

## ANTI-PATTERNS
- Don’t reintroduce category content under `system-skills/`; it creates duplicate source-of-truth issues.
