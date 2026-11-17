# CI speed levers

Derived from cutting a 40-minute PR pipeline to 2 minutes and trimming self-hosted GitLab CI / `make check` loops by an order of magnitude. Measure your own repository first, then pick the matching lever.

## 1. Runners, triggers, and the job graph

**Signal.** Queue dominates wall time, redundant pipelines run on the same commit, or heavy multi-seed jobs block every PR push.

**Do.**
- Move every job, including tiny ones, onto fast or self-hosted runners when queue exceeds work.
- Keep concurrent jobs at or below registered runner capacity, or merge short lanes into longer ones to reduce slot contention.
- Cancel superseded runs keyed by branch or PR/MR.
- Eliminate duplicate pipelines on push + PR/MR: on feature branches, run workflows on `merge_request_event` / `pull_request` (and tags/schedules/`DEFAULT_BRANCH`), skipping raw feature-branch `push` triggers once an MR/PR is open.
- Move multi-seed soak/stability matrices (`--randomly-seed`, `-count=N`) to scheduled runs (default `manual` + `allow_failure` on PR/MR if engineers want on-demand runs).

**Verify.** Queue seconds drop and pipeline count per PR commit stays at 1.

**Pitfall.** Merging lanes couples failure domains. Keep step names and artifacts separated so triage stays direct.

## 2. Lint and custom policy checks

**Signal.** Linting or custom repository policy scripts spend tens of seconds scanning files or loading heavy plugin ASTs.

**Do.**
- Replace slow linters with fast native tools (Oxlint for JS/TS, Ruff for Python) and enable strict rule sets.
- Replace single-rule heavyweight tools (for example, running `pylint --enable=duplicate-code` for 60s+ when Ruff already handles lint) with focused standard-library token/AST duplicate detectors.
- Audit custom policy scripts for quadratic complexity: precompute parent maps or guarded-import sets once per AST instead of re-walking per node, prefilter large trees with fast substring checks before running compiled regexes, and provide a `--fast` changed-files mode for pre-commit.

**Verify.** Wall time of lint/policy steps and parity on known violations (check edge flags such as `ignore-signatures` when replacing duplicate-code detectors).

## 3. Switch typecheckers when a faster one ships

**Signal.** Typecheck is a large slice of work, or cold runs spend 30–60s rebuilding type graphs from scratch.

**Do.** Benchmark incremental caches (`.mypy_cache`, TypeScript project references) and faster native checkers (`tsgo` / TypeScript 7) against the existing error set on a known-bad commit before switching.

**Pitfall.** Different semantics can hide errors. Verify parity on a failing fixture commit before adopting.

## 4. Shard and balance tests across cores

**Signal.** One test job dominates the run and CPU is underutilized or skewed across workers.

**Do.**
- Shard across processes/runners using one discovery entry point; use work-stealing schedulers (`pytest --dist=worksteal`) when test durations vary widely.
- Size workers below full saturation when tests spawn subprocesses (for example, `cores / 3` capped empirically) — oversubscription triggers CPU contention timeouts.
- Drop expensive unused outputs (`--cov-report=html`, `--cov-report=json`) when CI only enforces terminal coverage floors, and parallelize independent `coverage report --include=...` floor checks.

**Verify.** Total test count matches single-process discovery and zero contention flakes appear across repeated runs.

**Pitfall.** Shared fixtures, fixed ports, or tight 2–5s subprocess startup deadlines fail once concurrency rises. Widen startup budgets without relaxing functional assertions.

## 5. Profile in-process hotspots before over-sharding

**Signal.** Pure-Python or in-memory unit tests take seconds each despite doing little I/O.

**Do.** Profile one slow test with `python -m cProfile -s cumtime` (or language equivalent):
- Cache `typing.get_type_hints` / schema introspection results (`@functools.cache` by schema class) called inside tight serialization/validation loops.
- Cache static catalog/config file parses keyed by `(resolved_path, st_mtime_ns, st_size)` with lazy per-task decoding and defensive copies (`copy.deepcopy`) so test isolation holds.
- Prewarm reusable subprocess/fixture processes where safe, with explicit per-test state resets.

**Pitfall.** Mutable cached objects leak across tests if callers mutate returned structures in place. Deep-copy or freeze cached data.

## 6. Fix setup: caches, slots, and mirrors

**Signal.** Setup takes 20–120s per job, or cold spikes hit 300s+.

**Do.**
- Audit every job's trace (`scripts/ci_audit.py --forge gitlab` or GitHub Actions mode).
- Verify cached paths match the *actual* installer and toolchain: `UV_CACHE_DIR` (not only `PIP_CACHE_DIR`), `GOCACHE` alongside `GOMODCACHE`, `.mypy_cache`, and OS package archives (`APT_CACHE_DIR` with stamp-checked offline `dpkg -i` fallback).
- On self-hosted runners with per-slot local caches (`concurrent-0..N`), allow long/primary jobs (`pull-push`) to populate caches across slots instead of restricting `push` to one short job.
- Rank package mirrors (`apk`, `apt`, `pip`, `npm`) by latency from the runner network, and set tight per-mirror network timeouts (20–30s instead of 300s) so throttled mirrors fail over fast.
- Use blobless clones (`filter: blob:none`) when history is inspected; shallow clones break diff/commit checks.

**Verify.** Setup seconds drop cleanly across all runner slots, not only slot 0.

## 7. Run independent stages and builds in parallel

**Signal.** Independent checks, coverage reports, cross-compiled binaries, or target bootstrap kits run sequentially inside one step.

**Do.** Run independent shell subchecks (`&` + wait-all propagating non-zero exit), Go cross-compilations (`GOOS`/`GOARCH` targets), or Python artifact builders (`ThreadPoolExecutor`) concurrently inside jobs with spare cores.

**Verify.** Critical-path wall time approaches the slowest single subtask plus teardown overhead.

## 8. Only run what the change touches (double fail-closed)

**Signal.** Docs, READMEs, or localized scripts trigger 5-minute full test/build suites.

**Do.**
- Add path-based job filters (`changes:` on PR/MR events while keeping jobs unconditional on `DEFAULT_BRANCH`, tags, schedules, and web triggers) plus an allowlist diff selector inside monolithic `make check` runners.
- Implement **double fail-closed** exit semantics in the selector script: return a dedicated non-zero sentinel code (e.g., `10`) for "verified safe to skip"; treat `0` *and* every crash/git/untracked error code (`1`, `2`, `127`) as "run the full suite". Never write a full-gate pass stamp when heavy suites were skipped.
- Keep a permanent unit test proving any unknown extension, dirty index, or selector bug falls back to full execution.

**Pitfall.** Returning `0` on skip turns a crashed selector into a silent green build.

## 9. Split fast `pre-commit` from cached `pre-push`

**Signal.** Slow hooks get skipped with `--no-verify`, or agents push trivial format/lint errors to remote CI.

**Do.**
- Bind a `<10s` `pre-commit` hook to formatting, fast AST/diff policy checks (`--fast`), and lint-only native checks (`--lint-only`).
- Bind `pre-push` to the full local gate, backed by a content fingerprint over git `HEAD`, staged index, tracked/untracked worktree hashes, and tool env so `git push` right after `make check` finishes in `<0.5s`.

**Verify.** Time both a typical `pre-commit` edit (`<10s`) and an immediately-followed `pre-push` (`<1s`).

## Cost and trade-offs

Every lever trades something (compute spend, deferred multi-seed soak coverage on PRs, or narrow signature-ignoring duplicate checks). State those trade-offs explicitly in the PR/MR alongside `before -> after` measurements.

## References

- Original Actions case study (40m to 2m, $230 to $4,300/mo): Owen Gretzinger, "How I made our CI 20x faster (steal this)", October 2026: <https://x.com/owengretzinger/status/2116291924219060319>
