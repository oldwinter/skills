# Global Skills

Canonical repository for operating-system-level global skills.

Runtime roots on this machine:

- `~/.agents/skills`
- `~/.codex/skills`

Sync is managed from `general-tasks`:

```bash
just global-skills-sync-status
just global-skills-sync-dry-run
just global-skills-sync-apply
```

`global-skills-sync-state.json` stores the last synced content hash for each skill.
The sync uses that state as a three-way baseline:

- canonical changed, runtime unchanged: canonical updates runtime
- runtime changed, canonical unchanged: runtime updates canonical
- both changed differently: conflict, no overwrite
- one side missing: copy to the missing side

Runtime directories are copied by default. To replace matching runtime directories
with symlinks to this canonical repo, run the same command with `link_runtime=1`;
the sync script backs up replaced runtime directories first.
