#!/usr/bin/env python3
"""Split recent GitHub Actions jobs into queue, setup, and run time.

The point is the number no dashboard shows by default: how much of a job's
wall time was spent waiting for a machine and doing setup, versus doing the
work that produced the result. Run it before optimizing, and again after.

    python3 scripts/ci_audit.py --limit 20
    python3 scripts/ci_audit.py --repo owner/name --workflow CI --limit 40
    python3 scripts/ci_audit.py --json > audit.json

Requires the GitHub CLI (`gh`) authenticated for the repository. Standard
library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess  # nosec B404 - fixed gh argv
import sys
from collections import defaultdict
from typing import Any, Final

DEFAULT_SETUP_PATTERN: Final = (
    r"^(set up job|set up |run actions/checkout|checkout|install|cache|"
    r"download|initialize|post |complete job|upload )"
)


def run_gh(args: list[str]) -> Any:
    result = subprocess.run(  # nosec B603 - argv is built here, not by a shell
        ["gh", *args], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def parse_time(value: str | None) -> dt.datetime | None:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def seconds(start: dt.datetime | None, end: dt.datetime | None) -> float:
    if start is None or end is None:
        return 0.0
    return max(0.0, (end - start).total_seconds())


def resolve_repo(explicit: str | None) -> str:
    if explicit:
        return explicit
    result = subprocess.run(  # nosec B603 - fixed gh argv
        ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"gh repo view failed: {result.stderr.strip()}")
    return result.stdout.strip()


def completed_runs(repo: str, workflow: str | None, limit: int) -> list[dict[str, Any]]:
    args = [
        "run",
        "list",
        "--repo",
        repo,
        "--limit",
        str(limit),
        "--json",
        "databaseId,conclusion,createdAt,updatedAt,workflowName,displayTitle,headBranch,event",
    ]
    if workflow:
        args += ["--workflow", workflow]
    runs = run_gh(args) or []
    return [run for run in runs if run.get("conclusion")]


def collate(
    repo: str, runs: list[dict[str, Any]], setup_pattern: re.Pattern[str]
) -> dict[str, Any]:
    jobs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    steps: dict[str, list[float]] = defaultdict(list)
    for run in runs:
        payload = run_gh(["api", f"repos/{repo}/actions/runs/{run['databaseId']}/jobs"])
        for job in (payload or {}).get("jobs", []):
            started = parse_time(job.get("started_at"))
            completed = parse_time(job.get("completed_at"))
            created = parse_time(job.get("created_at")) or parse_time(run.get("createdAt"))
            if started is None or completed is None:
                continue
            setup = 0.0
            work = 0.0
            slow_steps: list[tuple[str, float]] = []
            for step in job.get("steps") or []:
                duration = seconds(
                    parse_time(step.get("started_at")), parse_time(step.get("completed_at"))
                )
                name = str(step.get("name", ""))
                if setup_pattern.search(name.lower()):
                    setup += duration
                else:
                    work += duration
                steps[name].append(round(duration, 1))
                if duration > 0.4:
                    slow_steps.append((name, round(duration, 1)))
            jobs[job["name"]].append(
                {
                    "run": run["databaseId"],
                    "conclusion": job.get("conclusion"),
                    "queue": round(seconds(created, started), 1),
                    "total": round(seconds(started, completed), 1),
                    "setup": round(setup, 1),
                    "work": round(work, 1),
                    "steps": slow_steps,
                }
            )
    return {"jobs": jobs, "steps": steps}


def average(values: list[float]) -> float:
    return round(sum(values) / len(values), 1) if values else 0.0


def summarize(collated: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for name, samples in collated["jobs"].items():
        rows.append(
            {
                "job": name,
                "runs": len(samples),
                "queue_avg": average([sample["queue"] for sample in samples]),
                "total_avg": average([sample["total"] for sample in samples]),
                "setup_avg": average([sample["setup"] for sample in samples]),
                "work_avg": average([sample["work"] for sample in samples]),
                "total_max": max(sample["total"] for sample in samples),
                "queue_max": max(sample["queue"] for sample in samples),
                "slowest_sample": max(samples, key=lambda sample: sample["total"]),
            }
        )
    rows.sort(key=lambda row: (row["total_avg"] + row["queue_avg"]), reverse=True)
    slow_steps = [
        {"step": name, "avg_seconds": average(values), "samples": len(values)}
        for name, values in collated["steps"].items()
    ]
    slow_steps.sort(key=lambda row: row["avg_seconds"], reverse=True)
    return {"jobs": rows, "slowest_steps": slow_steps[:15]}


def print_report(summary: dict[str, Any], repo: str, workflow: str | None) -> None:
    print(f"repo {repo} · workflow {workflow or 'all'} · {len(summary['jobs'])} jobs ranked by queue + run\n")
    print(f"{'job':30} {'n':>3} {'queue':>7} {'setup':>7} {'run':>7} {'wall':>7} {'max':>7}")
    for row in summary["jobs"]:
        print(
            f"{row['job'][:30]:30} {row['runs']:3} {row['queue_avg']:7.1f} "
            f"{row['setup_avg']:7.1f} {row['work_avg']:7.1f} {row['total_avg']:7.1f} "
            f"{row['total_max']:7.1f}"
        )
    print("\nslowest steps (average seconds):")
    for row in summary["slowest_steps"]:
        print(f"{row['step'][:52]:52} {row['avg_seconds']:8.1f}  n={row['samples']}")

    queue_bound = [row for row in summary["jobs"] if row["queue_avg"] > row["total_avg"]]
    if queue_bound:
        names = ", ".join(row["job"] for row in queue_bound)
        print(f"\nqueue-bound jobs (waiting beats running): {names}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Split Actions job time into queue, setup, and run")
    parser.add_argument("--repo", help="owner/name; defaults to the current repository")
    parser.add_argument("--workflow", help="workflow name or file")
    parser.add_argument("--limit", type=int, default=30, help="completed runs to inspect (default 30)")
    parser.add_argument(
        "--setup-regex",
        default=DEFAULT_SETUP_PATTERN,
        help="case-insensitive step-name pattern counted as setup",
    )
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    args = parser.parse_args(argv)

    if args.limit < 1:
        parser.error("--limit must be positive")
    repo = resolve_repo(args.repo)
    runs = completed_runs(repo, args.workflow, args.limit)
    if not runs:
        print("no completed runs found", file=sys.stderr)
        return 1
    summary = summarize(collate(repo, runs, re.compile(args.setup_regex, re.IGNORECASE)))
    if args.json:
        print(json.dumps({"repo": repo, "workflow": args.workflow, "runs": len(runs), **summary}, indent=2))
    else:
        print_report(summary, repo, args.workflow)
        print(f"\nfrom {len(runs)} completed runs")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
