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

```bash
(
  cd "$repo"
  npx --yes skills@latest add . --list -y              > "$ev/list-shallow.txt"
  npx --yes skills@latest add . --list -y --full-depth > "$ev/list-full-depth.txt"
)
```

Derive the expected name sets from the tree before asserting. The counts move every time a skill is added or retired, so nothing here may be hardcoded — this file once asserted `12`/`15` while the tree had already grown a skill.

```bash
cd "$repo"
# Every SKILL.md the full-depth scan can see: the whole tree, hidden dirs
# included (.git is excluded — a clone never stores skills there).
mapfile -t all_dirs < <(find . -name SKILL.md -not -path './.git/*' | sed 's|^\./||; s|/SKILL.md$||' | sort)
# The shallow scan sees depth-1 dirs plus the harness convention roots the CLI
# always checks — verified to be .claude/skills, .agents/skills, .codex/skills;
# other hidden dirs like .dotprobe/skills are not scanned shallow.
expected_shallow=$(printf '%s\n' "${all_dirs[@]}" | awk -F/ 'NF==1 || (NF==3 && ($1==".claude" || $1==".agents" || $1==".codex") && $2=="skills") {print $NF}' | sort -u)
expected_all=$(printf '%s\n' "${all_dirs[@]}" | sed 's|.*/||' | sort -u)
# The published set is what check-readme-map counts: no hidden component at all.
expected_published=$(printf '%s\n' "${all_dirs[@]}" | grep -vE '(^|/)\.' | sed 's|.*/||' | sort -u)
```

```powershell
# Same derivation for PowerShell.
$allDirs = Get-ChildItem $repo -Recurse -Filter SKILL.md -File -Force | ForEach-Object {
    ($_.FullName.Substring($repo.Length).TrimStart('\/') -replace '[\\/]SKILL\.md$','') -replace '\\','/'
} | Where-Object { $_ -notlike '.git/*' } | Sort-Object
$roots = '.claude','.agents','.codex'
$expectedShallow = $allDirs | Where-Object {
    $p = $_ -split '/'
    $p.Count -eq 1 -or ($p.Count -eq 3 -and $roots -contains $p[0] -and $p[1] -eq 'skills')
} | ForEach-Object { $_.Split('/')[-1] } | Sort-Object
$expectedAll = $allDirs | ForEach-Object { $_.Split('/')[-1] } | Sort-Object -Unique
$expectedPublished = $allDirs | Where-Object {
    -not (($_ -split '/') | Where-Object { $_.StartsWith('.') })
} | ForEach-Object { $_.Split('/')[-1] } | Sort-Object -Unique
```

The CLI draws a box; each skill name sits alone on a `│    <name>` line, so names parse out with one pattern (strip ANSI escapes first):

```bash
names() { perl -pe 's/\e\[[0-9;?]*[A-Za-z]//g' "$1" | sed -nE 's/^│[[:space:]]+([a-z0-9-]+)[[:space:]]*$/\1/p' | sort -u; }
diff <(names "$ev/list-shallow.txt")   <(printf '%s\n' "$expected_shallow")
diff <(names "$ev/list-full-depth.txt") <(printf '%s\n' "$expected_all")
```

```powershell
function Names($file) {
    Get-Content $file | ForEach-Object { $_ -replace '\x1b\[[0-9;?]*[A-Za-z]','' } |
        Where-Object { $_ -match '^│\s+([a-z0-9-]+)\s*$' } |
        ForEach-Object { $Matches[1] } | Sort-Object -Unique
}
Compare-Object (Names (Join-Path $ev 'list-shallow.txt'))   $expectedShallow   # empty = pass
Compare-Object (Names (Join-Path $ev 'list-full-depth.txt')) $expectedAll      # empty = pass
```

Observable end state that proves it works:

- `list-shallow.txt` names exactly the shallow set — the root-level skills plus `verify`, because the CLI treats `.claude/skills/` as a convention root even at shallow depth;
- `list-full-depth.txt` names the full set, adding the nested `obsidian-skills/` entries (`canvas-atlas`, `to-note`, `vault-moc`) — and any SKILL.md left under `.scratch/` by a previous drive, which is why this feature runs before fixture drives;
- the published set (`$expected_published` / `$expectedPublished`, the CLI set minus every hidden path) equals `README.md` Statistics `Skill directories` / `Unique names` — the same universe `check-readme-map` counts;
- both invocations exit `0` and print each skill's description.

## Gotchas

- `--json` cannot be combined with `--list` (`The --json flag cannot be combined with --list.`), so parse names from the text output.
- The CLI and `scripts/check-*` prune different trees: the checker skips every hidden directory; the CLI still scans the `.claude/skills`, `.agents/skills` and `.codex/skills` convention roots at shallow depth and scans *everything* (including `.scratch/`) at `--full-depth`. `verify` is therefore listed to consumers even though it is project-local tooling; its description scopes it to this repo.
- Run this feature before anything creates SKILL.md files under `.scratch/` — a leftover install (`$run/.claude/skills/done`) or the frontmatter fixture inflates `--full-depth` counts and name sets. If the diff surprises, clean `.scratch/` and re-run.
- The shallow scan stops at `obsidian-skills`; a new nested skill is invisible until `--full-depth` is used or the scan is re-run.
- BSD `sed` (macOS) has no `\x1B` escape, so the `names` helper strips ANSI with `perl`, which is present on macOS and Linux.
- A skill with an invalid frontmatter does not fail the listing — it silently disappears (see [frontmatter-silent-skip.md](frontmatter-silent-skip.md)). Compare the count with the tree, never trust the count alone.
- The listing prints long descriptions; redirect to a file instead of fighting console wrapping when grepping.
