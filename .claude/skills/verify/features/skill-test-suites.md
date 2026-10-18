# Skill test suites

The skills that ship code also ship unittest suites. They are slower than the gates and are deliberately not part of `just check`, so a change to a script-bearing skill needs this drive explicitly.

## Sub-features

- `just test-skills` runs all five suites: `agent-autoresearch`, `obsidian-skills/canvas-atlas`, `longform-fiction`, `loop-kit`, `loop-triage-github`.
- One suite at a time when only one skill changed: `python3 -m unittest discover -s <skill>/tests -q`.
- The suites are Python-only; `bash` is not required for them.

## How to get to it (user POV)

README → 校验 lists `just test-skills` as the suite command next to `just check`. `AGENTS.md` does not require it for a Markdown-only change, but the justfile treats it as the story for script-bearing skills (`loop-kit`'s `loopkit.py`, `agent-autoresearch`'s helpers, the Obsidian and fiction tooling).

## Driving it with unittest

```powershell
just test-skills 1> (Join-Path $ev "test-skills.txt") 2> (Join-Path $ev "test-skills.err"); "test-skills exit=$LASTEXITCODE"
```

Observable end state that proves it works:

- exit `0`;
- `test-skills.txt` carries one `Ran N tests` block per suite (five blocks) and no `FAILED`;
- the five suites named above each ran rather than being skipped as a missing directory.

A single suite, with the same evidence discipline:

```powershell
python3 -m unittest discover -s loop-kit/tests -q 1> (Join-Path $ev "loop-kit-tests.txt") 2>&1
"loop-kit exit=$LASTEXITCODE"
```

## Gotchas

- A missing `tests/` directory makes `unittest discover` pass with zero tests; count the blocks rather than trusting the exit code alone.
- The suites run from the repo root (the recipes do), so paths inside tests are relative to it; running from elsewhere can pass vacuously.
- This target is slow (unittest discovery over five trees). It is a separate drive from `just check` because `check` must stay fast.
- Python bytecode from a run lands in `__pycache__/` directories, which `.gitignore` already covers.
