# Repo gates

The maintainer path: `just check` (README map, skill contracts, fixture tests) and `just doctor` (local toolchain). These are the gates a change to any `SKILL.md`, the README list, or `scripts/` must pass before it is publishable.

## Sub-features

- `just check` — README map (`check-readme-map`), frontmatter/link/personal-path audit (`check-skill-contracts`), and the three fixture suites that prove those checks themselves behave.
- `just doctor` — python3, resolved `bash`, git, just, and the `CLAUDE.md` → `AGENTS.md` symlink.
- Individual recipes when only one gate is relevant (`just check-readme-map`, `just test-doctor`, ...).
- The checkers accept an explicit repo path, which is how a fixture tree is audited (`python3 scripts/check-skill-contracts <tree>`).

## How to get to it (user POV)

`AGENTS.md` → Verify, and README → 校验, tell a contributor to run `just check` after any change. On Windows the README notes that the first `bash` on PATH may be WSL; `just doctor` prints the resolved path so that is visible before a fixture test fails confusingly.

## Driving it with just

```powershell
just check       1> (Join-Path $ev "check.txt")       2> (Join-Path $ev "check.err");       "check exit=$LASTEXITCODE"
just doctor      1> (Join-Path $ev "doctor.txt")      2> (Join-Path $ev "doctor.err");       "doctor exit=$LASTEXITCODE"
```

Observable end state that proves it works:

- exit `0` for both;
- `check.txt` contains `check-readme-map: README skill list matches the repo tree.`, `check-skill-contracts: audited skill contracts pass.`, and `test-check-readme-map: ok` / `test-check-skill-contracts: ok` / `test-doctor: ok`;
- `doctor.txt` ends with `doctor: 5 pass, 0 warn, 0 fail, 2 skip` (the two `SKIP` rows are the deliberately empty env-file and services checks);
- `check.err` only repeats the recipe commands.

## Gotchas

- `just check` prunes hidden directories, so `.claude/` and `.scratch/` are never audited — a verify skill there cannot break the gate, and cannot rely on it either.
- `test-*` recipes call `bash`; WSL bash does not share the Windows filesystem. If those rows fail oddly, read the `bash` row in `doctor.txt` first.
- `just doctor` exits non-zero on any `FAIL`, but `SKIP` and `WARN` still exit `0` — assert the summary line, not only the code.
- The fixture tests run the checkers against fixture trees; a failure there means the check logic regressed even when this repo's tree passes.
- `test-skills` is not part of `check`; a green `just check` says nothing about the skill unittest suites (see [skill-test-suites.md](skill-test-suites.md)).
