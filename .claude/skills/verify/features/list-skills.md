# Discover skills

What a consumer sees before installing anything: the skill list the CLI extracts from the checkout. This is also the fastest proof that a new or renamed skill is actually publishable.

## Sub-features

- List root skills (the default, shallow scan).
- List nested skills with `--full-depth` (the Obsidian bundle).
- Agree with the README's list and statistics, which `just check` also enforces.

## How to get to it (user POV)

The README's install examples assume discovery: a consumer runs `skills add oldwinter/skills --list`, sees the names and descriptions, then picks with `--skill`. `--full-depth` is the documented flag for `obsidian-skills/` in README → 装.

## Driving it with the skills CLI

```powershell
Push-Location $repo
try {
  npx --yes skills@latest add . --list -y              1> (Join-Path $ev "list-shallow.txt")
  npx --yes skills@latest add . --list -y --full-depth 1> (Join-Path $ev "list-full-depth.txt")
} finally { Pop-Location }
```

Observable end state that proves it works:

- `list-shallow.txt` reports `Found 12 skills` and names the root skills;
- `list-full-depth.txt` reports `Found 15 skills` and adds `canvas-atlas`, `to-note`, `vault-moc`;
- the 15 names equal the directories containing `SKILL.md` under the repo, and `README.md` Statistics read `Skill directories: 15` / `Unique names: 15`;
- both invocations exit `0` and print each skill's description.

## Gotchas

- `--json` cannot be combined with `--list` (`The --json flag cannot be combined with --list.`), so parse names from the text output.
- The shallow scan stops at `obsidian-skills`; a new nested skill is invisible until `--full-depth` is used or the scan is re-run.
- A skill with an invalid frontmatter does not fail the listing — it silently disappears (see [frontmatter-silent-skip.md](frontmatter-silent-skip.md)). Compare the count with the tree, never trust the count alone.
- The listing prints long descriptions; redirect to a file instead of fighting console wrapping when grepping.
