# system-skills/sync-skills-manager

## OVERVIEW
Sync tooling for repository-canonical skill categories ↔ runtime installs (`~/.claude/skills` and other agents).

## WHERE TO LOOK
| Task | Location |
|------|----------|
| User-facing usage | `SKILL.md` |
| Implementation | `sync-skills.sh` |
| Repo/system path config | `sync-config.json` |

## COMMANDS
```bash
./sync-skills.sh diff
./sync-skills.sh pull     # alias: auto
./sync-skills.sh push
./sync-skills.sh link-all
./sync-skills.sh status
./sync-skills-3way.sh sync
./sync-skills-3way.sh status
```

## CONVENTIONS
- Category discovery is recursive for directories ending in `-skills` that directly contain skills (`SKILL.md`).
- New auto-categorized skills prefer `<repo-root>/<category>/`; existing `system-skills/<category>/` remains supported for compatibility.
- `sync-skills-3way.sh` is incremental only (`rsync --update`) and does not delete destination files.
- `sync-skills.sh link-all` rebuilds other agent global paths as symlinks to `~/.claude/skills`.
