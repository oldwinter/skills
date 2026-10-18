# Frontmatter silent skip

The failure mode this repo keeps warning about in `AGENTS.md`: a `description` containing `: ` that is not quoted is invalid YAML, and the install CLI drops that skill while still reporting a successful install. The skill simply is not there afterwards, and nothing failed.

## Sub-features

- Reproduce the skip against a throwaway copy of the repo: the skill vanishes from `--list` and from an install while exit codes stay `0`.
- Prove the repo gate catches it first: `scripts/check-skill-contracts` fails with `unquoted description with ': ' (invalid YAML, skipped by installers)`.
- The same trap applies to `>` block scalars and angle brackets in a description; both are rejected by the same checker.

## How to get to it (user POV)

`AGENTS.md` → Skill rules states the contract, and README → 装 reminds consumers that a `disable-model-invocation` skill is expected to be un-invokable. A contributor who unquotes a description sees a green install and a missing skill — this feature is how that becomes observable before shipping.

## Driving it with the skills CLI

Build a fixture copy outside the tracked tree, break one description, then compare what the installer sees with what the checker says:

```powershell
$fixture = Join-Path $repo ".scratch/verify-$stamp-fixture"
New-Item -ItemType Directory -Force $fixture | Out-Null
Copy-Item (Join-Path $repo "scripts"), (Join-Path $repo "README.md") $fixture -Recurse
Get-ChildItem $repo -Directory |
    Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } |
    ForEach-Object { Copy-Item $_.FullName $fixture -Recurse }
Copy-Item (Join-Path $repo "obsidian-skills") $fixture -Recurse

$bad = Join-Path $fixture "done/SKILL.md"
$text = Get-Content $bad -Raw
Set-Content $bad ($text -replace 'description: "(.+)"', 'description: $1') -NoNewline

Push-Location $fixture
try {
  npx --yes skills@latest add . --list -y 1> (Join-Path $ev "fixture-list.txt"); "fixture list exit=$LASTEXITCODE"
} finally { Pop-Location }

python3 (Join-Path $repo "scripts/check-skill-contracts") $fixture 1> (Join-Path $ev "fixture-contracts.txt") 2>&1
"contracts exit=$LASTEXITCODE"
```

Observable end state that proves it works:

- `fixture-list.txt` exits `0` and no longer lists `done` (count drops by one) — the silent skip, reproduced;
- `fixture-contracts.txt` exits non-zero with `unquoted description with ': ' (invalid YAML, skipped by installers): done/SKILL.md`;
- the real checkout is untouched: `git -C $repo status --short` shows no change to `done/SKILL.md`.

Cleanup: `Remove-Item -Recurse -Force $fixture`. Keep `$ev`.

## Gotchas

- The fixture must copy `obsidian-skills/` and `scripts/`, or the counts and the checker disagree for the wrong reason.
- `done` is chosen because its real description already contains `: ` inside quotes; unquoting it is a one-line, reversible break. Any skill works, but pick one whose description has `: ` so the YAML actually breaks.
- Quote only the value: a `description:` that starts with `>` or `|` is the block-scalar variant of the same bug and is rejected by name.
- The installer's exit code stays `0` on this failure. Never use install exit status as the proof; compare the listed names and the installed tree.
- If the CLI version changes, re-check that the silent skip still exists before quoting this feature as evidence.
