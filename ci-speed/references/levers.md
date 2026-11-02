# CI speed levers

Derived from a published before/after account of cutting a PR pipeline from 40 minutes to 2. The numbers below are that account's, not universal. Use them to pick a lever, then measure your own repository.

## 1. Runners and the job graph

**Signal.** Queue is a large share of each job's wall time, or jobs wait for a runner while another job in the same run holds it.

**Do.**
- Move every job to a faster or self-hosted runner class. Include the small jobs; a short job that waits for a machine is a long job.
- Count concurrent jobs and registered runners. Keep concurrent jobs at or below the runner count. Extra jobs queue behind each other and starve the short lanes.
- If the pool is fixed, merge short lanes into a longer lane so the run needs fewer slots, or delete jobs that duplicate work.
- Cancel superseded runs with a concurrency group keyed by branch or PR.

**Verify.** The audit's `queue` column drops. A run with two long lanes and two runners should show near-zero queue for both.

**Pitfall.** Merging lanes couples failure domains. A security scan failure now fails the test lane. Keep independent evidence paths visible in step names and artifacts.

## 2. Lint with the fastest tool

**Signal.** Lint is a visible slice of setup or work, or a lint failure bounces an agent through a full CI cycle.

**Do.** Replace the slow linter with the fast one for the ecosystem: Oxlint for JavaScript and TypeScript, Ruff for Python. Turn on as many rules as the codebase tolerates; agents do not tire of fixing them.

**Verify.** Lint duration and the number of rules enabled.

## 3. Switch typecheckers when a faster one ships

**Signal.** Typecheck is a visible slice of work.

**Do.** Benchmark the alternatives on your repository, not on the announcement. TypeScript 7 and Bun's checker are faster than `tsc`; `tsgo` and similar projects change quickly. Keep a benchmark command in the repository so the next switch is cheap.

**Pitfall.** A faster checker with different semantics can hide or invent errors. Compare the error set on a known-bad commit before adopting it.

## 4. Shard tests onto machines with cores

**Signal.** One test job dominates the run and its CPU is saturated.

**Do.**
- Split the suite into independent shards and run them concurrently.
- Size shards to available cores. Loading modules and starting interpreters costs CPU too, so measure whether more shards helps. On an 8-core box with subprocess-heavy tests, four shards often beat eight.
- Keep the same test discovery entry point. A shard runner that filters the discovered set preserves the test contract; a second runner does not.

**Verify.** Wall time drops roughly with shard count until contention wins. The test count across shards equals the single-process count.

**Pitfall.** Shared fixtures, fixed ports, fixed temp paths, and once-per-process setup collide. Make state per-shard before raising the count.

## 5. Stop reloading the app per test file

**Signal.** Each test file pays a large fixed import or setup cost, and the actual assertions are a small fraction.

**Do.** Reuse the process across files (`isolate: false` in Vitest and similar settings). Add a per-file reset hook so state does not leak. Write down what each test must clean up.

**Pitfall.** Leaks show up as order-dependent failures. Run the suite in a different order or in shards to surface them.

## 6. Fix setup before optimizing tests

**Signal.** Setup is the largest bucket, or a job takes far longer than its test step.

**Do.**
- Audit every job's steps. The bundled `scripts/ci_audit.py` does this from the Actions API.
- Fix caches that never hit. Hosted caches are scoped per branch; seed the default branch and let PRs restore from it. Prefer caching the dependency directory over reinstalling.
- Use a blobless clone (`filter: blob:none`, full history) instead of a shallow clone when anything reads history. Shallow breaks tools that inspect commits.
- Match parallel tasks to cores. Running eight tasks on a four-vCPU job is slower and flakier than four.

**Verify.** Setup seconds per job, and cache hit rate.

## 7. Run independent stages in parallel

**Signal.** Lint, typecheck, build, and tests run one after another in one job.

**Do.** Run them as parallel jobs or parallel steps. A PR takes as long as its slowest lane. Then inspect the slowest lane: if it also carries migrations, smoke tests, or another app's tests, split those out.

**Verify.** The run wall time approaches the slowest lane plus the gate.

## 8. Only run what the change touches

**Signal.** Full suites run on documentation-only or single-package changes.

**Do.**
- Select affected projects or tests from the diff (Nx affected, a test-dependency map, or a path-to-test mapping).
- Run the full suite on the default branch and on a schedule.
- **Test the skip logic itself.** Make a change that the selector should catch, hide it from the selector, and confirm the run goes red. Add that as a permanent test.

**Pitfall.** A selector that silently returns an empty set reports green while testing nothing. Fail closed on an empty selection for code changes.

## 9. Put fast checks before the push

**Signal.** Agents push changes that fail lint or typecheck, then wait a full CI cycle for the answer.

**Do.** Add a pre-push or pre-commit hook that runs format, lint, and typecheck on changed files. Keep it under about ten seconds. Put it in a hook, not in AGENTS.md: agents skip prose steps.

**Verify.** Time the hook on a typical change. A slow hook gets bypassed with `--no-verify`, which is worse than no hook.

## What the account cost

The source pipeline's bill rose from about $230 to $4,300 per month. Faster runners, more shards, and more concurrent jobs cost money. Report the delta when you recommend a lever.

## Source

Owen Gretzinger, "How I made our CI 20x faster (steal this)", October 2026: <https://x.com/owengretzinger/status/2116291924219060319>
