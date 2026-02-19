# Obsidian CLI Automation Recipes

Use this playbook to convert repeated Obsidian work into deterministic shell workflows.

## Preconditions

1. Confirm CLI availability:
   ```bash
   command -v obsidian
   ```
2. List available vaults:
   ```bash
   obsidian vaults
   ```
3. Pin a vault for repeatable automation:
   ```bash
   VAULT='My Vault'
   ```

## Recipe 1: Daily Note Capture + Planning Block

```bash
VAULT='My Vault'
obsidian vault="$VAULT" daily:append content=$'## Plan\n- [ ] Top 1\n- [ ] Top 2\n- [ ] Top 3\n'
obsidian vault="$VAULT" daily:read
```

## Recipe 2: Quick Inbox Capture

```bash
VAULT='My Vault'
STAMP="$(date '+%Y-%m-%d %H:%M')"
obsidian vault="$VAULT" create path="Inbox/${STAMP}.md" content=$'# Quick Capture\n\n- Context:\n- Next action:\n'
```

## Recipe 3: Weekly Note Bootstrap

```bash
VAULT='My Vault'
WEEK="$(date '+%G-W%V')"
obsidian vault="$VAULT" create \
  path="Weekly/${WEEK}.md" \
  content=$"# Weekly ${WEEK}\n\n## Goals\n- [ ]\n\n## Wins\n- \n\n## Risks\n- \n" \
  overwrite
```

## Recipe 4: Batch Set Frontmatter Property

Set a property for every Markdown note in a folder.

```bash
VAULT='My Vault'
obsidian vault="$VAULT" files folder="Projects" ext=md | while IFS= read -r path; do
  [ -z "$path" ] && continue
  obsidian vault="$VAULT" property:set path="$path" name=reviewed value=false type=checkbox
  echo "updated: $path"
done
```

## Recipe 5: Task Triage in Daily Note

```bash
VAULT='My Vault'
obsidian vault="$VAULT" tasks daily todo
obsidian vault="$VAULT" daily:append content=$'- [ ] Follow up on blockers'
obsidian vault="$VAULT" tasks daily todo
```

## Recipe 6: Vault Hygiene Report

```bash
VAULT='My Vault'
obsidian vault="$VAULT" unresolved total
obsidian vault="$VAULT" orphans total
obsidian vault="$VAULT" deadends total
obsidian vault="$VAULT" recents total
```

## Recipe 7: Search + Context Export

```bash
VAULT='My Vault'
QUERY='incident'
obsidian vault="$VAULT" search:context query="$QUERY" format=json > incident-context.json
obsidian vault="$VAULT" search query="$QUERY" total
```

## Recipe 8: Plugin Baseline Audit

```bash
VAULT='My Vault'
obsidian vault="$VAULT" plugins versions format=json > plugins.json
obsidian vault="$VAULT" plugins:enabled versions format=json > plugins-enabled.json
```

## Recipe 9: Safe Sync/History Inspection Before Restore

```bash
VAULT='My Vault'
TARGET='Projects/Example.md'

obsidian vault="$VAULT" sync:status
obsidian vault="$VAULT" sync:history path="$TARGET"
obsidian vault="$VAULT" sync:read path="$TARGET" version=1
```

Run restore only after reviewing the preview:

```bash
obsidian vault="$VAULT" sync:restore path="$TARGET" version=1
```

## Recipe 10: Command Discovery Snapshot

Capture command capabilities before writing automation:

```bash
obsidian --help > obsidian-top-help.txt
obsidian commands > obsidian-command-ids.txt
```

## Guardrails

- Prefer `path=` over `file=` when file names are ambiguous.
- Prefer read/inspect commands before mutation commands.
- Avoid `delete permanent` unless explicit user confirmation is present.
- Verify post-write state with `read`, `file`, `tasks`, `properties`, or `search`.
- Use `vault=<name>` for every non-trivial automation run.
