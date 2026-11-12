# Orchestration paradigms

Each paradigm is a shape for a Run. Pick by the work's dependency structure, not by harness.

## Fan-out / fan-in (map-reduce)

One coordinator, N workers on independent shards, one aggregation.

Use when units are independent and each has a checkable output.

Orca: `worker-start` × N; `current` for disjoint files, `new-child` for overlap.

Failure: a shard that is not independent — workers collide or duplicate work.

## Pipeline / DAG

Tasks with `--deps`; a stage starts when its dependencies settle.

Use when stages have real ordering: design → implement → test → review.

Orca: `task-create --deps`, `task-list --ready`.

Failure: fake dependencies serialize work that could run in parallel.

## Supervisor / nested workers

A worker starts its own sub-workers and aggregates their reports.

Use when a sub-task is itself decomposable, or needs a different harness.

Orca: the worker preamble's SUB-DISPATCH; `worker-start --from`; depth cap (default 4).

Failure: nesting past the cap; a parent that reports before its helpers settle.

## Maker-checker / review gate

Producer workers plus an independent reviewer; the reviewer's verdict gates acceptance.

Use when correctness matters and the producer should not self-approve.

Orca: a separate reviewer worker with the diff and acceptance criteria; `gate-create` for human decisions.

Failure: the reviewer sees a summary instead of the diff.

## Arena / best-of-N

N candidates on the same task in isolated worktrees; a judge picks or grafts.

Use when the design space is open and one attempt would lock in the wrong shape.

Orca: N `new-child` workers plus a judge worker; compare diffs.

Failure: candidates share a worktree and contaminate each other.

## Specialist routing

Assign harness or model by role: Claude architect, pi implementers, codex reviewer.

Use when harness strengths differ or the user names the roles.

Orca: `--agent` per worker; `--model` and `--effort` when the user names them.

Failure: routing by habit instead of by a checkable strength.

## Blackboard

Workers write to a shared plan or ledger; the coordinator synthesizes.

Use when work is long-running or asynchronous and workers need a common record.

Orca: `current` worktree plus a plan file; one writer per file.

Failure: concurrent writes to the same ledger.

## Sentinel / monitor

A long-running worker watches external state (CI, PR, logs) and reports on change.

Use when the coordinator must react to an external event.

Orca: a worker with a bounded watch task; external polling is fine, Orca mail polling is not.

Failure: polling Orca mail instead of ending the turn.

## Human gate

`gate-create` blocks a task until a human resolves a decision.

Use when the decision is irreversible, ambiguous, or outside the agent's authority.

Orca: `gate-create --task <id> --question "<decision>" --options <json_array>`; `gate-resolve`.

Failure: gating work the agent can decide from the brief.

## Remote / federated

Workers on another Orca server.

Use when the work needs a different machine or environment.

Orca: `--on <saved-environment>`; `new-child` or `new-top-level` with a remote repo.

Failure: assuming local paths or terminals exist on the remote host.
