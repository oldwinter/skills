---
name: verify
description: "Drive the oldwinter/skills library end to end: run the repo gates, install a named skill from this working tree with the real skills CLI into an isolated workspace, and prove the installed bundle, lock file, and discovery output. Use when a change touches a SKILL.md, the README skill list, or scripts/, or before claiming 'it parses' or 'the install works'."
---

# Verify oldwinter/skills

There is no server here: the "app" is the `skills` installer plus the `just` gates. Every proof runs against this working tree, never the GitHub remote. Start from the project root (`git rev-parse --show-toplevel`) and read `features/README.md` for the mapped features; the commands below are the recipe they reuse.

The skill is invocable as `verify`. Do not install anything with `--global` against the real home, and do not commit the `$run` directory.

## Launch

No process to start. Prepare one isolated install workspace and one evidence directory, both under `.scratch/` (gitignored, and pruned by `scripts/check-*`, so a run can never trip `just check`):

```powershell
$repo  = git rev-parse --show-toplevel
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$run   = Join-Path $repo ".scratch/verify-$stamp"           # installs land here; deleted at cleanup
$ev    = Join-Path $repo ".scratch/verify-evidence/$stamp"  # proof; survives cleanup
New-Item -ItemType Directory -Force $run, $ev | Out-Null
"$repo`n$run`n$ev"
```

The CLI installs project-scope skills into the current working directory (`<cwd>/.claude/skills/<name>`), so running it from `$run` is what keeps the repo untouched. A short-lived command needs no server: each drive is one isolated `npx` invocation in `$run`.

## Doctor

Read-only preflight. Run it first whenever a drive looks off.

```powershell
just doctor | Tee-Object (Join-Path $ev "doctor.txt")
git -C $repo rev-parse --show-toplevel | Tee-Object (Join-Path $ev "repo-root.txt")
git -C $repo rev-parse HEAD           | Tee-Object (Join-Path $ev "head.txt")
git -C $repo status --short           | Tee-Object (Join-Path $ev "git-status.txt")
npx --yes skills@latest --version     | Tee-Object (Join-Path $ev "cli-version.txt")
```

Worth driving when: the last `doctor` line reads `0 fail`, the resolved root is the repo you mean to prove, `head.txt` plus `git-status.txt` name the exact tree the evidence covers, and the CLI prints a version (`1.7.2` is the version this skill was proven against; any newer version re-checks the gotchas below). A `FAIL` row, a different root, or no CLI version means fix the instance before driving.

## Drive

Every drive writes its transcript into `$ev` and asserts on the files, not just on CLI text.

Install one skill from this checkout (consumer path):

```powershell
Push-Location $run
try {
  npx --yes skills@latest add $repo --skill done --agent claude-code --copy -y --json `
      1> (Join-Path $ev "install.json") 2> (Join-Path $ev "install.err")
  "install exit=$LASTEXITCODE" | Tee-Object (Join-Path $ev "install-exit.txt")
  Get-ChildItem -Recurse -Force $run | Select-Object FullName, Length |
      Out-File (Join-Path $ev "tree.txt")
} finally { Pop-Location }
```

Assert all four:

- exit code `0` and `install.json` carries `"status": "installed"` for the requested name;
- `$run/.claude/skills/done/SKILL.md` exists and its frontmatter says `name: done`;
- `$run/skills-lock.json` records `"sourceType": "local"` plus a `computedHash`;
- nothing appeared outside `$run` — `Test-Path ~/.agents/skills/done` is false and the global `~/.agents/.skill-lock.json` mtime is unchanged.

Discovery (what a consumer sees before choosing):

```powershell
Push-Location $repo
try {
  npx --yes skills@latest add . --list -y             1> (Join-Path $ev "list-shallow.txt")
  npx --yes skills@latest add . --list -y --full-depth 1> (Join-Path $ev "list-full-depth.txt")
} finally { Pop-Location }
```

Assert shallow finds 12 names, `--full-depth` finds 15 including `canvas-atlas`, `to-note`, and `vault-moc`, and those 15 equal the skill directories under the repo (README Statistics say 15 / 15).

Repo gates (maintainer path; run these for every content change):

```powershell
just check       1> (Join-Path $ev "check.txt")       2> (Join-Path $ev "check.err");       "check exit=$LASTEXITCODE"
just doctor      1> (Join-Path $ev "doctor.txt")      2> (Join-Path $ev "doctor.err");       "doctor exit=$LASTEXITCODE"
just test-skills 1> (Join-Path $ev "test-skills.txt") 2> (Join-Path $ev "test-skills.err"); "test-skills exit=$LASTEXITCODE"
```

`just check` covers the README map, frontmatter/link/personal-path audit, and the check scripts' fixture tests; `just test-skills` runs the five skill unittest suites (slower, not part of `check`). Assert exit `0` for each and capture the success lines.

## Evidence

Write into `$ev`; name the proof `<stamp>` and keep `$ev` after cleanup.

- `doctor.txt`, `head.txt`, `git-status.txt`, `cli-version.txt` — the instance the proof applies to.
- `install.json`, `install.err`, `install-exit.txt`, `tree.txt` — the drive and its resulting filesystem state.
- `list-shallow.txt`, `list-full-depth.txt` — discovery output.
- `check.txt`, `check.err`, `test-skills.txt` — repo gates.
- `notes.md` — the verdict, written last.

Proof standards for this repo:

- Exercise the real consumer path: the `skills` CLI reading this checkout and writing an installed bundle. Do not substitute copying files by hand, and do not treat `just check` alone as proof that install works.
- Capture the action and the resulting state together: command transcript plus the installed file tree and lock entry. A CLI line that says "installed" is not proof of what exists.
- Verify side effects, not just visible output: installed `SKILL.md`, `skills-lock.json`, and the absence of global-scope writes.
- Mocks: none are needed. The only isolation is the `$run` directory, which is the point. A "dry-run" is not a drive — this CLI has no dry-run, so an install into `$run` is the honest exercise.
- Record `head.txt` and `git-status.txt` with the proof so a reader knows the evidence covers a dirty working tree, not `main`.

`notes.md` shape:

```markdown
# Proof <stamp>

- Tree: <head sha>, dirty as captured in git-status.txt
- Feature: features/install-one-skill.md
- Commands: <the exact invocations>
- Observed: <exit codes, file paths, lock entry>
- Verdict: pass | fail — <what failed and where the evidence is>
```

## Cleanup

```powershell
Remove-Item -Recurse -Force $run
```

- Remove only `$run` (and any temp repo copy a feature created). Never `Remove-Item` `$ev`, `.scratch/verify-evidence/`, or `$repo/.claude`.
- After cleanup, confirm the proof still exists: list `$ev` and check the expected files are present. A cleanup that eats evidence fails the run.
- Never install with `--global` against the real home: it writes `<home>/.agents/skills` and the global lock. If a feature must exercise global scope, point `HOME` and `USERPROFILE` at a temp directory for that one process and capture the diff.
- No servers are started, so never kill by process name. If `npx` hangs, stop the exact PID you started, then still run this cleanup.
- If the install wrote outside `$run`, stop and report it in `notes.md`; do not delete foreign paths to make the proof clean.

## Helpers

No scripts ship with this skill; the commands above are copy-paste ready. Add a helper here only if a drive outgrows one screen — and show its invocation in the body, never leave it to be reverse-engineered.

## Gotchas

- `--json` cannot be combined with `--list` on `skills` 1.7.2 (`The --json flag cannot be combined with --list.`). Use text for listing, `--json` for install.
- PowerShell wraps native stderr as `NativeCommandError` even on success. Always redirect stderr to `install.err` and trust exit codes plus files, never red console text.
- Pass `$repo` as an absolute path: the lock file records the source relative to `$run` (`../..`), and a relative `add` path from `.scratch/verify-*` resolves to the wrong tree.
- Shallow `--list` returns 12 skills. `obsidian-skills/` is nested, so `canvas-atlas`, `to-note`, and `vault-moc` only appear with `--full-depth`; the README states 15.
- The installer sends telemetry and needs the npm registry on a cold cache. A slow first `npx` is not a failure; a non-zero exit is.
- Always pass `--copy`: without it the CLI may link into agent directories, and symlink behavior on Windows is not a stable thing to assert.
- `done` carries `disable-model-invocation: true`, so it installs and is listed but the model cannot invoke it. Verify it by file presence and frontmatter, not by running it.
- A `SKILL.md` whose unquoted `description` contains `: ` is silently skipped by the installer while the install still reports success — see `features/frontmatter-silent-skip.md`.
