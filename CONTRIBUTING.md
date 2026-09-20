# Contributing

This repository is a Markdown-first skills library. Canonical agent notes are in [AGENTS.md](AGENTS.md).

## Checks

```bash
just test-sync
just audit-readme
python3 -m unittest obsidian-skills/canvas-atlas/tests/test_check_canvas.py
```

`just validate-skill <dir>` and `just validate-skillpack <dir>` need PyYAML (`python3 -m pip install pyyaml`).

Obsidian sidecar recipes (`just obsidian-sync` and friends) are not implemented yet. They exit 2 and print `try: docs/plans/2026-03-08-obsidian-skill-state-sync.md`.

Do not run `python3 meta-skills/skills-readme-updater/scripts/update_readme.py --write`. That flag is rejected so it cannot replace the handwritten two-layer README with a `~/.claude/skills` dump.

## Scope

Keep skill directories hyphen-case. Do not add credentials, private hostnames, or device paths. Do not unify root vs `*-skills/` name collisions unless a ticket asks.
