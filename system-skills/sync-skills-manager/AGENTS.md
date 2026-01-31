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
```

## CONVENTIONS
- The script expects `system-skills/` to contain subcategory directories ending in `-skills` plus `sync-skills-manager`.
