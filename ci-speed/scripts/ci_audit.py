#!/usr/bin/env python3
"""Split recent GitHub Actions or GitLab CI jobs into queue, setup, and run time.

The point is the number dashboards hide by default: how much of a job's wall
time was spent waiting for a machine and doing setup, versus doing the work
that produced the result. Run it before optimizing, and again after.

    python3 scripts/ci_audit.py --workflow CI --limit 20
    python3 scripts/ci_audit.py --forge gitlab --repo group/project --limit 20
    python3 scripts/ci_audit.py --repo owner/name --json > audit.json

Requires `gh` (GitHub Actions) or `glab` (GitLab CI) authenticated for the
repository. Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess  # nosec B404 - fixed gh/glab argv
import sys
from collections import defaultdict
from typing import Any, Final
from urllib.parse import quote, urlparse

DEFAULT_SETUP_PATTERN: Final = (
    r"^(set up job|set up |run actions/checkout|checkout|install|cache|"
    r"download|initialize|post |complete job|upload )"
)
GITLAB_CMD_SETUP_PATTERN: Final = (
    r"^(?:\.? ?\S*setup|\.? ?\S*ci_ap[kt]|mkdir -p |export |"
    r"(?:apk|apt|apt-get|brew|pip|pip3|uv|npm|pnpm|yarn|bundle|cargo|go|choco|winget)\s+"
    r"(?:add|update|install|sync|ci|restore|fetch|mod download))"
)
ANSI_RE: Final = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\r")
SECTION_MARKER_RE: Final = re.compile(r"section_(start|end):(\d+(?:\.\d+)?):([A-Za-z0-9_.:-]+)")
LINE_TS_RE: Final = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)\s+\S+\s+(.*)$")


def run_gh(args: list[str]) -> Any:
    result = subprocess.run(  # nosec B603 - argv is built here, not by a shell
        ["gh", *args], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def run_glab_api(path: str, *, host: str | None = None, raw: bool = False) -> Any:
    env = {**os.environ, "GITLAB_HOST": host} if host else os.environ
    result = subprocess.run(  # nosec B603 - argv is built here, not by a shell
        ["glab", "api", path], env=env, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise SystemExit(f"glab api {path} failed: {result.stderr.strip()}")
    if raw:
        return result.stdout
    return json.loads(result.stdout) if result.stdout.strip() else None


def parse_time(value: str | None) -> dt.datetime | None:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def seconds(start: dt.datetime | None, end: dt.datetime | None) -> float:
    if start is None or end is None:
        return 0.0
    return max(0.0, (end - start).total_seconds())


def git_remote_url() -> str | None:
    result = subprocess.run(  # nosec B603 - fixed git argv
        ["git", "config", "--get", "remote.origin.url"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    url = result.stdout.strip()
    return url or None


def detect_forge(
    explicit: str,
    remote_url: str | None,
    host: str | None,
    workflow: str | None,
) -> str:
    if explicit != "auto":
        return explicit
    if host:
        return "gitlab"
    if workflow:
        return "github"
    if remote_url:
        lowered = remote_url.lower()
        if "github.com" in lowered:
            return "github"
        if "gitlab" in lowered:
            return "gitlab"
    if os.environ.get("GITLAB_HOST"):
        return "gitlab"
    return "github"


def _repo_path_from_remote(remote_url: str) -> str | None:
    if "://" in remote_url:
        path = urlparse(remote_url).path
    elif ":" in remote_url:
        path = remote_url.split(":", 1)[1]
    else:
        return None
    cleaned = path.strip("/").removesuffix(".git")
    return cleaned or None


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


def resolve_gitlab_project(explicit: str | None, remote_url: str | None) -> str:
    if explicit:
        if explicit.isdigit():
            return explicit
        if "%" in explicit and "/" not in explicit:
            return explicit
        return quote(explicit.strip("/").removesuffix(".git"), safe="")
    path = _repo_path_from_remote(remote_url or "")
    if not path:
        raise SystemExit("unable to determine GitLab project; pass --repo group/project or project ID")
    return quote(path, safe="")


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


def split_gitlab_trace(
    trace_text: str,
    started_at: str | None,
    finished_at: str | None,
    setup_pattern: re.Pattern[str],
    *,
    duration_hint: float | None = None,
) -> tuple[float, float, list[tuple[str, float]]]:
    """Split a GitLab CI job trace into (setup_seconds, work_seconds, slow_steps)."""
    start_dt = parse_time(started_at)
    finish_dt = parse_time(finished_at)
    total = seconds(start_dt, finish_dt)
    if total == 0.0 and duration_hint is not None:
        total = max(0.0, float(duration_hint))

    clean = ANSI_RE.sub("", trace_text)
    cmd_setup_re = re.compile(GITLAB_CMD_SETUP_PATTERN, re.IGNORECASE)
    section_starts: dict[str, float] = {}
    section_durations: list[tuple[str, float]] = []
    in_step_script = False
    work_start: dt.datetime | None = None
    work_end: dt.datetime | None = None
    step_script_start_ts: dt.datetime | None = None
    step_script_end_ts: dt.datetime | None = None

    for raw_line in clean.splitlines():
        ts_match = LINE_TS_RE.match(raw_line)
        line_ts = parse_time(ts_match.group(1)) if ts_match else None
        body = ts_match.group(2) if ts_match else raw_line

        for sec in SECTION_MARKER_RE.finditer(body):
            kind, epoch_s, name = sec.group(1), float(sec.group(2)), sec.group(3)
            if kind == "start":
                section_starts[name] = epoch_s
                if name == "step_script":
                    in_step_script = True
                    if line_ts is not None and step_script_start_ts is None:
                        step_script_start_ts = line_ts
            elif kind == "end":
                started_epoch = section_starts.pop(name, None)
                if started_epoch is not None and epoch_s >= started_epoch:
                    section_durations.append((name, round(epoch_s - started_epoch, 1)))
                if name == "step_script":
                    in_step_script = False
                    if line_ts is not None and step_script_end_ts is None:
                        step_script_end_ts = line_ts

        if in_step_script and line_ts is not None and work_start is None and body.startswith("$ "):
            cmd = body[2:].strip()
            if not (setup_pattern.search(cmd.lower()) or cmd_setup_re.search(cmd)):
                work_start = line_ts

    if work_start is not None and start_dt is not None:
        end_dt = work_end or step_script_end_ts or finish_dt or work_start
        work_s = max(0.0, min(total, (end_dt - work_start).total_seconds())) if total > 0 else max(
            0.0, (end_dt - work_start).total_seconds()
        )
        setup_s = max(0.0, total - work_s) if total > 0 else seconds(step_script_start_ts or start_dt, work_start)
    else:
        step_total = sum(dur for name, dur in section_durations if name in ("step_script", "build_script"))
        if step_total > 0 or section_durations:
            work_s = min(total, step_total) if total > 0 else step_total
            setup_s = max(0.0, total - work_s) if total > 0 else sum(
                dur for name, dur in section_durations if name not in ("step_script", "build_script")
            )
        else:
            work_s = total
            setup_s = 0.0

    slow_steps = [(name, dur) for name, dur in section_durations if dur > 0.4]
    return round(setup_s, 1), round(work_s, 1), slow_steps


def completed_gitlab_pipelines(project: str, host: str | None, limit: int) -> list[dict[str, Any]]:
    pipelines: list[dict[str, Any]] = []
    page = 1
    while len(pipelines) < limit:
        batch = run_glab_api(f"projects/{project}/pipelines?per_page=100&page={page}", host=host) or []
        if not batch:
            break
        for pipe in batch:
            if pipe.get("status") in ("success", "failed"):
                pipelines.append(pipe)
                if len(pipelines) >= limit:
                    break
        if len(batch) < 100:
            break
        page += 1
    return pipelines


def collate_gitlab(
    project: str,
    pipelines: list[dict[str, Any]],
    setup_pattern: re.Pattern[str],
    *,
    host: str | None = None,
    trace_samples: int = 3,
) -> dict[str, Any]:
    jobs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    steps: dict[str, list[float]] = defaultdict(list)
    sampled: dict[str, int] = defaultdict(int)
    for pipe in pipelines:
        pid = pipe["id"]
        pipe_jobs = run_glab_api(f"projects/{project}/pipelines/{pid}/jobs?per_page=100", host=host) or []
        for job in pipe_jobs:
            status = job.get("status")
            duration = job.get("duration")
            if status not in ("success", "failed") or duration is None:
                continue
            name = str(job["name"])
            queue_s = round(float(job.get("queued_duration") or 0.0), 1)
            total_s = round(float(duration), 1)
            setup_s: float | None = None
            work_s: float | None = None
            slow_steps: list[tuple[str, float]] = []
            if sampled[name] < trace_samples:
                sampled[name] += 1
                trace = run_glab_api(
                    f"projects/{project}/jobs/{job['id']}/trace", host=host, raw=True
                )
                setup_s, work_s, slow_steps = split_gitlab_trace(
                    str(trace or ""),
                    job.get("started_at"),
                    job.get("finished_at"),
                    setup_pattern,
                    duration_hint=total_s,
                )
                for sec_name, sec_dur in slow_steps:
                    steps[f"section:{sec_name}"].append(sec_dur)
            jobs[name].append(
                {
                    "run": pid,
                    "conclusion": status,
                    "queue": queue_s,
                    "total": total_s,
                    "setup": setup_s,
                    "work": work_s,
                    "steps": slow_steps,
                }
            )
    return {"jobs": jobs, "steps": steps}


def average(values: list[float]) -> float:
    return round(sum(values) / len(values), 1) if values else 0.0


def summarize(collated: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for name, samples in collated["jobs"].items():
        setups = [sample["setup"] for sample in samples if sample.get("setup") is not None]
        works = [sample["work"] for sample in samples if sample.get("work") is not None]
        rows.append(
            {
                "job": name,
                "runs": len(samples),
                "queue_avg": average([sample["queue"] for sample in samples]),
                "total_avg": average([sample["total"] for sample in samples]),
                "setup_avg": average(setups),
                "work_avg": average(works),
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


def print_report(summary: dict[str, Any], repo: str, scope: str | None) -> None:
    print(f"repo {repo} · workflow {scope or 'all'} · {len(summary['jobs'])} jobs ranked by queue + run\n")
    print(f"{'job':30} {'n':>3} {'queue':>7} {'setup':>7} {'run':>7} {'wall':>7} {'max':>7}")
    for row in summary["jobs"]:
        print(
            f"{row['job'][:30]:30} {row['runs']:3} {row['queue_avg']:7.1f} "
            f"{row['setup_avg']:7.1f} {row['work_avg']:7.1f} {row['total_avg']:7.1f} "
            f"{row['total_max']:7.1f}"
        )
    if summary["slowest_steps"]:
        print("\nslowest steps (average seconds):")
        for row in summary["slowest_steps"]:
            print(f"{row['step'][:52]:52} {row['avg_seconds']:8.1f}  n={row['samples']}")

    queue_bound = [row for row in summary["jobs"] if row["queue_avg"] > row["total_avg"]]
    if queue_bound:
        names = ", ".join(row["job"] for row in queue_bound)
        print(f"\nqueue-bound jobs (waiting beats running): {names}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Split GitHub Actions or GitLab CI job time into queue, setup, and run"
    )
    parser.add_argument(
        "--forge",
        choices=("auto", "github", "gitlab"),
        default="auto",
        help="CI forge API to query (default: auto from git remote / flags)",
    )
    parser.add_argument("--repo", help="owner/name (GitHub) or group/project / numeric ID (GitLab)")
    parser.add_argument("--workflow", help="workflow name or file (GitHub Actions)")
    parser.add_argument("--host", help="GitLab base URL (e.g. https://gitlab.example.com)")
    parser.add_argument("--limit", type=int, default=30, help="completed runs/pipelines to inspect (default 30)")
    parser.add_argument(
        "--trace-samples",
        type=int,
        default=3,
        help="GitLab traces per job name to split setup vs work (default 3; 0 skips traces)",
    )
    parser.add_argument(
        "--setup-regex",
        default=DEFAULT_SETUP_PATTERN,
        help="case-insensitive step/command pattern counted as setup",
    )
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    args = parser.parse_args(argv)

    if args.limit < 1:
        parser.error("--limit must be positive")
    if args.trace_samples < 0:
        parser.error("--trace-samples must be non-negative")

    remote_url = git_remote_url() if not args.repo or args.forge == "auto" else None
    forge = detect_forge(args.forge, remote_url, args.host, args.workflow)
    setup_pattern = re.compile(args.setup_regex, re.IGNORECASE)

    if forge == "gitlab":
        repo = resolve_gitlab_project(args.repo, remote_url)
        runs = completed_gitlab_pipelines(repo, args.host, args.limit)
        if not runs:
            print("no completed pipelines found", file=sys.stderr)
            return 1
        summary = summarize(
            collate_gitlab(
                repo, runs, setup_pattern, host=args.host, trace_samples=args.trace_samples
            )
        )
        scope: str | None = "gitlab"
    else:
        repo = resolve_repo(args.repo)
        runs = completed_runs(repo, args.workflow, args.limit)
        if not runs:
            print("no completed runs found", file=sys.stderr)
            return 1
        summary = summarize(collate(repo, runs, setup_pattern))
        scope = args.workflow

    if args.json:
        print(
            json.dumps(
                {"forge": forge, "repo": repo, "workflow": scope, "runs": len(runs), **summary},
                indent=2,
            )
        )
    else:
        print_report(summary, repo, scope)
        print(f"\nfrom {len(runs)} completed runs ({forge})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
