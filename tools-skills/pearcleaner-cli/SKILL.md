---
name: pearcleaner-cli
description: Use when using Pearcleaner’s macOS CLI (`pear`) to list uninstallable app files, uninstall an app, remove all related files, clean orphaned files (orphaned/残留), or manage the privileged helper (enable/disable/status).
---

# Pearcleaner CLI (`pear`)

## Overview

Use `pear` (Pearcleaner) to uninstall macOS apps and clean up leftover/orphaned files.
Prefer listing first and require explicit user confirmation before running destructive commands.

## Prerequisites (required)

- Confirm `pear` exists and is runnable:

```bash
command -v pear
pear --help
```

- Always quote app paths with spaces (paths are usually `.app` bundles).

## Safety gates (required)

1. **Preview first**: run `pear list` (for an app) or `pear list-orphaned` (for orphaned files) and summarize what will be removed.
2. **Explicit confirmation**: never run `pear uninstall-all` or `pear remove-orphaned` until the user explicitly confirms they want that destructive action.
3. **Exact path**: if the app path is ambiguous, stop and confirm the exact `.app` location before uninstalling.

## Command quick reference

List related files for an app (non-destructive):

```bash
pear list "/Applications/Some App.app"
```

Uninstall only the app bundle:

```bash
pear uninstall "/Applications/Some App.app"
```

Uninstall the app bundle and ALL related files (destructive):

```bash
pear uninstall-all "/Applications/Some App.app"
```

List orphaned files (non-destructive):

```bash
pear list-orphaned
```

Remove ALL orphaned files (destructive; exceptions list is managed in Pearcleaner settings):

```bash
pear remove-orphaned
```

Manage privileged helper tool:

```bash
pear helper
pear helper enable
pear helper disable
```

## Workflow: uninstall one app

1. Resolve the exact app bundle path (usually under `/Applications`).
2. Preview what will be removed:

```bash
pear list "/Applications/Foo.app"
```

3. Pick one action:
   - Minimal uninstall (bundle only): `pear uninstall "/Applications/Foo.app"`
   - Full cleanup (bundle + related files): `pear uninstall-all "/Applications/Foo.app"` (requires explicit confirmation)

Optional: find an app path by name:

```bash
mdfind "kMDItemFSName == 'Foo.app'"
```

## Workflow: clean orphaned files

1. Preview orphaned files:

```bash
pear list-orphaned
```

2. If the list looks safe, ask for explicit confirmation and then remove:

```bash
pear remove-orphaned
```

## Privileged helper notes

- Use `pear helper` to check status.
- `pear helper enable` may require admin credentials and is used for privileged operations.

## Limitations / gotchas

- `pear --version` is not supported; use `pear --help`.
- `pear` does not expose a dry-run flag for destructive commands beyond the listing commands (`list`, `list-orphaned`).
