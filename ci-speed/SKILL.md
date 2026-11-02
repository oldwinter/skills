---
name: ci-speed
description: Make CI and PR checks fast by measuring whether wall time goes to queue, setup, or work, then fixing the largest bucket with runner and job-graph changes, faster tooling, test sharding, cache seeding, and fail-closed skip guards. Use when PR checks are slow, agents keep waiting on CI, or a pipeline needs a speed audit.
---

# CI Speed

CI is the loop coding agents wait on. An agent that waits 20 minutes per push pays it dozens of times a day. Treat CI as a product: measure the wall time, fix the largest bucket, re-measure, and keep the evidence.

`<skill-dir>` is the directory containing this file.

## Route the request

- **Audit** ("why is CI slow", "where does the time go"): run Measure, report the three buckets, change nothing.
- **Optimize** ("make CI faster", "cut PR time"): Measure, apply the levers the numbers name, verify with a second audit, open a PR with before/after numbers.
- **One known bottleneck** ("tests take 4 minutes"): measure that job first. The claim may be true and still not be the critical path.

## Measure

Run the bundled audit from the repository root. It needs `gh` authenticated for the repo and nothing else:

```bash
python3 <skill-dir>/scripts/ci_audit.py --workflow CI --limit 30
```

It splits every completed job into three buckets:

- **queue**: waiting for a runner, `started_at - job.created_at`
- **setup**: checkout, tool setup, dependency install, uploads
- **work**: the steps that produce the result

Rank jobs by queue plus work. Save the table. It is the baseline the change cites.

Then find the slowest single step in the slowest job. `--json` gives the same data for scripting:

```bash
python3 <skill-dir>/scripts/ci_audit.py --repo owner/name --limit 50 --json > baseline.json
```

When queue is the largest bucket, count runners and jobs before touching test commands. A five-second job that waits ten minutes for a machine is a ten-minute job, and it also holds a slot the next run needs.

## Fix, in measured order

Read [references/levers.md](references/levers.md) for the full playbook. Apply one lever, verify it, then take the next. The buckets name the lever:

1. **Queue dominates**: change the runner supply or the job graph. Move every job, including tiny ones, to faster or self-hosted runners. With a fixed runner pool, merge or delete short jobs that spend most of their life waiting, and keep the number of concurrent jobs at or below the pool size.
2. **Setup dominates**: warm the dependency cache, seed it from the default branch, use a blobless clone, and cache the package directory rather than reinstalling. Audit which jobs actually restore a cache; a cache that is scoped per branch is cold on every PR.
3. **Work dominates**: use the fastest linter and typechecker available, shard the test suite, stop reloading the whole app per test file, run independent stages in parallel, and skip work the change does not touch.
4. **Everything is balanced but still slow**: the run length is the slowest lane. Split work out of that lane, or merge a short lane into it and delete a scheduling wave.

Before shipping, add a fail-closed guard for any skip logic. Prove it: hide a change from the selector on purpose, confirm the run goes red, then restore it.

## Verify

Run the audit again on runs from the new pipeline and compare the same table:

- report one primary number in `before -> after` form with its unit (run wall time, or the lane's duration)
- keep the raw audit output as an artifact in the PR
- check that the test count is unchanged when you only changed scheduling; a shard that silently loses tests is a regression wearing a speedup
- check that skipped and failed tests still fail the run

Do not report a speedup from one lucky run. Compare medians over at least five runs, or the same job's scheduler timing across both configurations.

## Pitfalls

- **Tests that assume a quiet machine.** Sharding adds CPU contention. Fixtures with hard 2-3 second startup deadlines start failing. Widen the fixture's startup budget, or freeze the clock for timestamp-sensitive assertions. Never widen the assertion that proves the product behavior.
- **Sharing state between shards.** Tests that write a fixed path, a shared port, or a shared temp directory collide once they run concurrently. Find the shared path and make it shard-specific before raising the shard count.
- **More shards is not more speed.** Measure. On an 8-core box with subprocess-heavy tests, four shards beat eight; the extra processes spend their time competing.
- **A green run that tested less.** Skip logic and shard filters can both drop tests. Guard them with a count check and a deliberate negative test.
- **Cost is part of the answer.** Faster runners and more shards raise the bill. State the new cost, as the original playbook does, so the trade is visible.

## Finish

Report the baseline bucket, the change, the post-fix number, and the artifact path. When the work lands in a repository, open a PR with the before/after table and the audit output attached.
