# system-skills/sync-skills-manager

## OVERVIEW
Sync tooling for `~/.agents/skills` ↔ `./system-skills` (including auto-categorization heuristics).

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
./sync-skills.sh status
./sync-skills-3way.sh sync
./sync-skills-3way.sh status
```

## CONVENTIONS
- The script expects `system-skills/` to contain subcategory directories ending in `-skills` plus `sync-skills-manager`.
- `sync-skills-3way.sh` is incremental only (`rsync --update`) and does not delete destination files.
