# Task specs

Every spec is self-contained: target, change, constraints, evidence of done. Say whether a non-zero exit means failure or is the deliverable.

## Architecture brief

Claude writes this before any dispatch.

```markdown
# <goal>

## Acceptance criteria
- ...

## Work units

### <unit>
- Owns: <files>
- Change: ...
- Verify: <command>
- Worktree: current | new-child

## Review focus
- ...
```

## pi implementation worker

```text
You are the <unit> worker on <goal>.

Target: <worktree or path>.

Change: <exact files and behavior>. Own only <files>. Leave <other units' files> untouched.

Constraints: <style, compatibility, dependencies, scope>.

Evidence of done: <verification command> passes; <files> exist; report the command output and every file you changed. A non-zero exit from <verification command> means this task failed.
```

## codex reviewer

```text
You are the independent reviewer for <goal>. You did not write this code.

See: <diff command or review worktree path>. The acceptance criteria are in <brief path>.

Check: <review focus>. For each finding, give severity, file:line, and a concrete failure scenario. Run <verification commands> yourself.

Verdict: approve, or request changes with the findings ranked by severity. Report only; the owning pi worker makes the edits.
```

## Fix follow-up

Send this to the pi worker that owns the file.

```text
Review found these issues in <files>:
- <finding with file:line and failure scenario>

Fix only these. Re-run <verification command>. Report the diff and the command output.
```

## Collecting child-worktree changes for review

When units used `new-child`, the coordinator must give codex one place to read.

1. Ask each pi worker to commit its changes on its branch, or to write a patch file with `git diff` plus untracked files.
2. Create a review branch from the base commit and cherry-pick each unit's commit. For patch files, apply them in order.
3. Start codex in the review worktree and name the diff command, for example `git diff <base>..HEAD`.

When units used `current`, review the coordinator's worktree directly and name the same diff command.
