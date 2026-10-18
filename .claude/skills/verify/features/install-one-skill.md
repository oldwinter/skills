# Install one skill

The consumer path that `README.md` → 装 documents: pull one named skill out of this checkout and put it where an agent reads project skills.

## Sub-features

- Install a single root skill by name (`--skill done`).
- Install with the `done` skill's manual-invocation flag intact.
- Record the install in `skills-lock.json` so a later `experimental_install` can restore it.
- Keep the repo tree untouched: installs happen in an isolated working directory.

## How to get to it (user POV)

A consumer runs, from their own project:

```bash
npx --yes skills@latest add oldwinter/skills --skill done change-evidence --full-depth
```

Here the source is the local checkout instead of `oldwinter/skills`, which is the same code path without the clone. The skill lands in the project's `.claude/skills/<name>/` (Claude Code) and/or the project's `.agents/skills` store, and `skills-lock.json` appears at the project root.

## Driving it with the skills CLI

From the isolated `$run` directory prepared by the skill's Launch step:

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

Observable end state that proves it works:

- `install.json` reports `"status": "installed"` with `"mode": "copy"` and `"scope": "project"`;
- `$run/.claude/skills/done/SKILL.md` exists, is a real directory under `$run`, and its frontmatter is `name: done`;
- `$run/skills-lock.json` has `"sourceType": "local"` and a `computedHash`;
- `Test-Path ~/.agents/skills/done` is `False` and `~/.agents/.skill-lock.json` keeps its old mtime.

## Gotchas

- The lock file stores the source relative to the install directory (`"source": "../.."`), so the `add` argument must be absolute; a relative path from `.scratch/verify-*` points at the wrong tree.
- `--copy` gives an assertable real directory; without it the CLI may create links whose Windows behavior you cannot assert.
- `done` declares `disable-model-invocation: true`. It installs and lists, but the model cannot invoke it — prove it by file presence, not by calling it.
- `--agent claude-code` writes `.claude/skills/<name>`. Adding more agents multiplies the target directories; assert the one you asked for rather than `-a '*'`.
- The installer emits telemetry and the first `npx` needs the registry; a cold run is slow, a failed run exits non-zero.
