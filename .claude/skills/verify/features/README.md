# Feature map

The repo has two user-facing surfaces: the **consumer** path (`npx skills add`, documented in `README.md` → 装) and the **maintainer** gates (`just check`, `just doctor`, `just test-skills`). One file per feature, each grounded in commands that run against this working tree.

| Feature | What a proof shows | File |
|---|---|---|
| Install one skill | A named skill installs from this checkout into an agent skills dir, with a lock entry and no global writes. | [install-one-skill.md](install-one-skill.md) |
| Discover skills | `--list` surfaces the documented set, and `--full-depth` surfaces the nested Obsidian ones. | [list-skills.md](list-skills.md) |
| Repo gates | `just check` and `just doctor` pass on the changed tree. | [repo-gates.md](repo-gates.md) |
| Skill test suites | The five unittest suites still pass. | [skill-test-suites.md](skill-test-suites.md) |
| Frontmatter silent skip | A malformed `description` disappears from the installer without an error, and `just check` catches it first. | [frontmatter-silent-skip.md](frontmatter-silent-skip.md) |

## Adding a feature

A feature is a user-visible path, not a script: add it when the repo grows a surface (a new installer flag, a new agent target, a new gate). Every file keeps the four H2s — `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas` — and every command in it must still work from a clean checkout.

A proof that drives only one convenient entry point is incomplete when the map lists others: name in `notes.md` which mapped features a run covered and which it skipped.
