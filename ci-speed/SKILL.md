---
name: ci-speed
description: Make CI, PR/MR pipelines, and local verification gates fast by measuring whether wall time goes to queue, setup, or work, then fixing the largest bucket with runner and job-graph changes, cache/mirror fixes, hotspot profiling, sharding, and double fail-closed skip guards. Use when PR checks are slow, make check takes minutes, agents keep waiting on CI, or a pipeline needs a speed audit.
---

# CI Speed

CI and local check gates form the loop coding agents wait on. Treat both as one product: measure where wall time goes, fix the largest bucket, re-measure, and keep the evidence.

`<skill-dir>` is the directory containing this file.

## Route the request

- **Audit** ("why is CI slow", "where does the time go"): run Measure, report the three buckets, change nothing.
- **Optimize** ("make CI faster", "cut PR time", "make check is slow"): Measure, apply the levers the numbers name, verify with a second audit, and ship before/after numbers.
- **One known bottleneck** ("tests take 4 minutes"): measure that job and its steps first. The named step may not be the critical path.

## Measure

Run the bundled audit from the repository root using `gh` (GitHub Actions) or `glab` (GitLab CI):

```bash
python3 <skill-dir>/scripts/ci_audit.py --workflow CI --limit 30
python3 <skill-dir>/scripts/ci_audit.py --forge gitlab --repo group/project --limit 30
```

It splits every completed job into three buckets:

- **queue**: waiting for a runner (`started_at - created_at` or GitLab `queued_duration`)
- **setup**: checkout, container prep, tool/mirror installs, cache restore/upload
- **work**: test, lint, typecheck, and build execution

Rank jobs by `queue + work`, save the baseline output (use `--json`), and inspect the slowest steps. When CI invokes a monolithic local script (such as `make check`), instrument its lanes and run `--durations` or `cProfile` on one slow test/linter before adding workers.

Completion criterion: a saved baseline showing pipeline wall time, bucket breakdown, and the top critical-path bottleneck.

## Fix, in measured order

Read [references/levers.md](references/levers.md) for tactics. Apply one lever, measure, then take the next:

1. **Queue / graph dominates**: match concurrent jobs to runner slots, cancel superseded runs, eliminate duplicate feature-branch `push` + PR/MR pipelines, and move multi-seed soak/stability matrices to schedules plus manual opt-in.
2. **Setup dominates**: align cache paths with the active installer (`UV_CACHE_DIR`, `GOCACHE`, `.mypy_cache`, OS package archives), ensure self-hosted runner slots populate caches (`pull-push` rather than leaving extra slots `pull`-only), rank mirrors by runner latency, and cap mirror attempts with short timeouts.
3. **Work dominates**: pick fast linters/typecheckers, profile in-process bottlenecks (uncached reflection/schema/JSON decoding, $O(N^2)$+ AST walks, heavy plugins replaceable with stdlib checks), shard to available cores, parallelize independent lanes/builds, drop unused coverage renders, use affected-only selection, and split `<10s` `pre-commit` hooks from fingerprint-cached `pre-push` gates.
4. **Everything balanced**: split work out of the critical-path lane, or merge tiny lanes so fewer runner slots hold up the pipeline.

For any skip logic or diff selector, enforce a **double fail-closed** contract: return a dedicated sentinel exit code (for example `10`) for a verified safe skip so both `0` and any crash/tool error (`1`, `2`, `127`) run the full suite, omit full-gate pass stamps on skipped runs, and prove the guard red with a negative test before restoring.

Completion criterion: the dominant bucket shrunk measurably, skip logic passes a negative test, and no test coverage or failure signal was silently dropped.

## Verify

Re-run the audit on post-fix runs (or isolated clean/docs-only probes for local gates) and compare against the baseline:

- report primary metrics in `before -> after` form with units (pipeline wall time, cold/warm gate duration, setup seconds)
- verify test counts and coverage floors match on unaffected code
- compare medians across multiple runs rather than one lucky run (or compare fixed-state scheduler runs when runner noise varies)

## Pitfalls

- **Tests that assume a quiet machine**: parallel workers add CPU contention and trip tight fixture startup deadlines (2–5s). Widen fixture startup/poll budgets without relaxing product behavior assertions.
- **Cold per-slot caches**: self-hosted runners often store caches per worker slot; restricting `push` to one fast job leaves other slots permanently cold.
- **Mirror timeouts**: throttled package mirrors that hang instead of failing fast burn a 300s timeout before fallback triggers.
- **Green runs that tested less**: skip selectors that return `0` on parse/git failure silently report green; require a non-zero sentinel code for skips.
- **Cost visibility**: faster runners, more shards, and extra concurrency change infrastructure cost; record trade-offs explicitly.

## Finish

Report the baseline bottleneck, each trade-off and change, `before -> after` numbers, and verified negative-test/suite checks in the PR/MR description.
