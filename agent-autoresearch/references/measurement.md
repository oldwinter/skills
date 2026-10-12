# Measurement design

The loop is only as good as its measurement. A trial is trustworthy when the same code yields the same verdict, the number moves only when the system under test changes, and the agent cannot move it any other way.

## The measure contract

The controller runs the measure command from the repository root with `bash` (or the platform shell) and:

- reads `METRIC <name>=<number>` lines from stdout and stderr; the line naming the primary metric decides the trial, the others are recorded as secondary metrics;
- falls back to the final non-empty stdout line when no `METRIC` line exists: a bare number becomes the primary metric, and a JSON object contributes its numeric fields;
- treats a non-zero exit, a timeout (`--timeout`, default 600 s), or a missing primary metric as a crash;
- treats any change to files git can see (tracked or untracked, not ignored) as a crash, because a measurement that edits the tree measures something else next time. Write outputs to ignored paths or to `$AUTORESEARCH_DIR` (the session directory). `$AUTORESEARCH_RUN` holds the trial label.

Exit 0 whenever a number was measured, even a bad one. Reserve non-zero exits for "could not measure".

Print secondary metrics that tell the next hypothesis where to look: phase timings, memory, error counts by category, cache hit rates. They cost nothing and are shown after every trial.

```python
#!/usr/bin/env python3
"""bench/measure.py: run the fixed workload five times, print METRIC lines."""
import statistics, subprocess, sys, time

# fast pre-check, so a syntax error fails in a second instead of after the workload
subprocess.run([sys.executable, "-m", "compileall", "-q", "src"], check=True)
times = []
for _ in range(5):
    start = time.perf_counter()
    subprocess.run([sys.executable, "-m", "mypkg.workload"], check=True, stdout=subprocess.DEVNULL)
    times.append(time.perf_counter() - start)
print(f"METRIC total_s={statistics.median(times):.4f}")
print(f"METRIC spread_s={max(times) - min(times):.4f}")
```

Wrapping an existing tool is usually one line: `uv run train.py > run.log 2>&1; grep '^val_bpb:' run.log | awk '{print "METRIC val_bpb=" $2}'` (keep `run.log` git-ignored).

## Fixed budget

Comparable trials need a fixed budget. Either fix the workload (same inputs, same iteration count) and measure cost, or fix the compute (a wall-clock or step budget, as in karpathy's 5-minute training runs) and measure quality. When the agent can trade one for the other, the budget is part of the protected measurement.

## Noise

Timing metrics are noisy; counts, sizes, and scores on fixed data usually are not.

- `init` probes a fast benchmark three times and reports the spread (median absolute deviation). When it calls the metric noisy, rebaseline with `--runs 5` (the median counts) and a `--min-delta` of about twice that spread so that noise cannot pass as progress.
- Prefer quieter signals when they track the goal: CPU time over wall time, instruction or operation counts over seconds, a larger fixed workload over a tiny one.
- Every lucky keep raises the bar for later trials. `recheck` re-measures the best commit and replaces its recorded value; use it when a keep's gain is within about twice the noise floor.
- Run parallel sessions on separate machines or cores when timing matters; they compete for the same CPU otherwise.

## Checks

`--checks` is the correctness gate: tests, type checks, lint, output equivalence. The controller runs it only when a trial would be kept, so a slow suite costs little. It must pass on the baseline. Keep its output short (failures only); the controller shows the tail.

## Overfitting and integrity

An agent optimizing a number will find every shortcut the setup allows. Close them in the setup rather than relying on intent:

- Protect the evaluator, its data, and the tests with `--protect`; the controller rejects trials that touch them.
- Keep a held-out set the loop never sees, and evaluate the final best on it before claiming the gain generalizes. When overfitting is likely, make the checks score a validation split with a floor.
- Measure in a fresh process so state cannot leak between the part that produces a result and the part that checks it.
- Count what the agent can inflate: when a compressor could embed its data, add the decompressor's size to the score; when a model could grow without bound, report its size as a secondary metric or cap it.

## Metric examples

| Goal | Metric (direction) | Measure sketch |
|---|---|---|
| Faster test suite | `total_s` (lower) | run the suite 3 times, print the median |
| Smaller bundle | `bundle_kb` (lower) | build, then `du -k dist/main.js` |
| Training quality | `val_bpb` (lower) | fixed time budget, grep the eval line |
| Fewer type errors | `errors` (lower) | count lines from the type checker |
| Higher benchmark score | `score` (higher) | run the eval harness on a fixed split |
| Lighthouse | `perf` (higher) | lighthouse JSON, extract the category score |
| Compression | `total_bytes` (lower) | compressed corpus plus decompressor size |
