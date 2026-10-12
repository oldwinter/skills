#!/usr/bin/env python3
"""agent-autoresearch controller.

The researcher (any coding agent with a shell) chooses hypotheses and edits
code. This controller owns everything that has to be trustworthy: measurement,
the keep-or-revert decision, git history, and the append-only experiment log.

Standard library only. Python 3.8+. Run `autoresearch.py --help`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import os
import re
import shlex
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SESSION = ".autoresearch"
SCHEMA = 1
METRIC_RE = re.compile(r"^\s*METRIC\s+([A-Za-z0-9_.\-µ]+)\s*=\s*(\S+)\s*$")
FAILED = ("crash", "timeout", "checks_failed")
TAIL_LINES = 25
HOOK_TIMEOUT = 30
HOOK_OUTPUT_LIMIT = 4096
NOISE_PROBE_SECONDS = 20.0
RECENT = 8
SCRIPT = Path(__file__).resolve()
SKILL_DIR = SCRIPT.parent.parent

PRESETS: Dict[str, Dict[str, Any]] = {
    "claude": {"argv": ["claude", "-p", "--dangerously-skip-permissions"], "model": ["--model"]},
    "codex": {
        "argv": ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox"],
        "model": ["-m"],
        "tail": ["-"],
    },
    "pi": {"argv": ["pi", "-p"], "model": ["--model"]},
}


class ARError(Exception):
    """A user-facing error: printed without a traceback."""

    code = 2


class Halt(ARError):
    """The session is not active, so no experiment may run."""

    code = 3


# ---------------------------------------------------------------- formatting


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).isoformat(timespec="seconds")


def from_iso(text: str) -> dt.datetime:
    return dt.datetime.fromisoformat(text)


def fmt(value: Optional[float]) -> str:
    if value is None:
        return "-"
    if float(value).is_integer() and abs(value) < 1e15:
        return f"{int(value):,}"
    magnitude = abs(value)
    if magnitude >= 1000:
        return f"{value:,.2f}".rstrip("0").rstrip(".")
    if magnitude >= 1:
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return f"{value:.6g}"


def pct(new: Optional[float], ref: Optional[float]) -> str:
    if new is None or ref is None or ref == 0:
        return "n/a"
    return f"{(new - ref) / abs(ref) * 100:+.2f}%"


def slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value[:40].strip("-") or "run"


def short(sha: Optional[str]) -> str:
    return sha[:7] if sha else "-"


def minutes_left(deadline: Optional[str]) -> Optional[float]:
    if not deadline:
        return None
    return (from_iso(deadline) - utcnow()).total_seconds() / 60


def median(values: List[float]) -> float:
    return float(statistics.median(values))


def mad(values: List[float]) -> float:
    center = median(values)
    return median([abs(v - center) for v in values])


def tail(text: str, lines: int = TAIL_LINES) -> str:
    rows = text.rstrip().splitlines()
    return "\n".join(rows[-lines:])


# ----------------------------------------------------------------------- git


def git(
    repo: Path,
    *args: str,
    env: Optional[Dict[str, str]] = None,
    input_text: Optional[str] = None,
    check: bool = True,
) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise ARError(f"git {' '.join(args)} failed: {detail}")
    return proc


def find_repo(path: Optional[str]) -> Path:
    start = Path(path or os.getcwd()).expanduser().resolve()
    proc = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise ARError(
            f"{start} is not inside a git repository. Autoresearch keeps and reverts "
            "experiments with git: run `git init && git add -A && git commit -m baseline` first."
        )
    return Path(proc.stdout.strip()).resolve()


def git_path(repo: Path, name: str) -> Path:
    path = Path(git(repo, "rev-parse", "--git-path", name).stdout.strip())
    return path if path.is_absolute() else repo / path


def head_sha(repo: Path) -> str:
    proc = git(repo, "rev-parse", "--verify", "HEAD", check=False)
    if proc.returncode != 0:
        raise ARError("the repository has no commits yet; commit the starting state first")
    return proc.stdout.strip()


def tree_of(repo: Path, rev: str) -> str:
    return git(repo, "rev-parse", f"{rev}^{{tree}}").stdout.strip()


def branch_name(repo: Path) -> Optional[str]:
    proc = git(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def is_ancestor(repo: Path, older: str, newer: str) -> bool:
    return git(repo, "merge-base", "--is-ancestor", older, newer, check=False).returncode == 0


def snapshot(repo: Path) -> str:
    """Tree object for the whole working tree (untracked files included), index untouched."""
    index = git_path(repo, "index")
    with tempfile.TemporaryDirectory(prefix="autoresearch-") as tmp:
        tmp_index = Path(tmp) / "index"
        if index.exists():
            # copy2 keeps the index mtime, so git's racy-entry check still re-hashes fresh edits
            shutil.copy2(index, tmp_index)
        env = dict(os.environ, GIT_INDEX_FILE=str(tmp_index))
        git(repo, "add", "-A", "--", ".", env=env)
        return git(repo, "write-tree", env=env).stdout.strip()


def diff_paths(repo: Path, old: str, new: str) -> List[str]:
    out = git(repo, "diff", "--name-only", "-z", "--no-renames", old, new).stdout
    return [path for path in out.split("\0") if path]


def commit_env(repo: Path) -> Dict[str, str]:
    env = dict(os.environ)
    for var, role in (("GIT_AUTHOR_IDENT", "AUTHOR"), ("GIT_COMMITTER_IDENT", "COMMITTER")):
        if git(repo, "var", var, check=False).returncode != 0:
            env.setdefault(f"GIT_{role}_NAME", "agent-autoresearch")
            env.setdefault(f"GIT_{role}_EMAIL", "agent-autoresearch@localhost")
    return env


def commit_tree(repo: Path, tree: str, parent: str, head: str, branch: str, message: str) -> str:
    """Commit `tree` on top of `parent` and move the branch there; working tree untouched."""
    sha = git(repo, "commit-tree", tree, "-p", parent, "-F", "-", env=commit_env(repo), input_text=message).stdout.strip()
    git(repo, "update-ref", "-m", "autoresearch: keep", f"refs/heads/{branch}", sha, head)
    git(repo, "reset", "-q")
    return sha


def revert_to(repo: Path, sha: str) -> None:
    git(repo, "reset", "-q", "--hard", sha)
    git(repo, "clean", "-q", "-fd", "-e", f"/{SESSION}/")


# ------------------------------------------------------------------- session


class Session:
    def __init__(self, repo: Path):
        self.repo = repo
        self.dir = repo / SESSION
        self.log = self.dir / "log.jsonl"
        self.program = self.dir / "program.md"
        self.ideas = self.dir / "ideas.md"
        self.logs = self.dir / "logs"
        self.patches = self.dir / "patches"
        self.hooks = self.dir / "hooks"
        self.relay = self.dir / "relay"
        self.stop_file = self.dir / "STOP"
        self.launcher = self.dir / "ar"
        self.pending_out = self.dir / "pending-trial.out"
        self.pending_pid = self.dir / "pending-trial.pid"

    def rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.repo).as_posix()
        except ValueError:
            return str(path)

    def read(self) -> List[Dict[str, Any]]:
        if not self.log.exists():
            return []
        entries = []
        for number, line in enumerate(self.log.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ARError(f"{self.rel(self.log)}:{number} is not valid JSON ({exc}); repair or delete that line")
        return entries

    def append(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        entry.setdefault("time", iso(utcnow()))
        self.dir.mkdir(parents=True, exist_ok=True)
        with self.log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry


class Lock:
    """One controller command at a time per session."""

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self) -> "Lock":
        for _ in range(2):
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                if self._stale():
                    try:
                        self.path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                pid = self.path.read_text().strip() or "?"
                raise ARError(f"another controller command (pid {pid}) is running in this session; wait for it to finish")
            with os.fdopen(fd, "w") as handle:
                handle.write(str(os.getpid()))
            return self
        raise ARError(f"could not acquire {self.path}")

    def _stale(self) -> bool:
        try:
            pid = int(self.path.read_text().strip())
        except (OSError, ValueError):
            return True
        if os.name == "nt":
            return time.time() - self.path.stat().st_mtime > 6 * 3600
        return not pid_alive(pid)

    def __exit__(self, *exc: Any) -> None:
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def pid_alive(pid: int) -> bool:
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class State:
    """Replay of log.jsonl: the log is the only source of truth."""

    def __init__(self) -> None:
        self.config: Optional[Dict[str, Any]] = None
        self.baseline: Optional[Dict[str, Any]] = None
        self.stack: List[List[Any]] = []
        self.trials: List[Dict[str, Any]] = []
        self.notes: Dict[int, List[str]] = {}
        self.stop: Optional[Dict[str, Any]] = None
        self.max_iterations: Optional[int] = None
        self.deadline: Optional[str] = None
        self.target: Optional[float] = None
        self.noise: List[float] = []
        self.next_run = 1
        self.started: Optional[str] = None

    @property
    def best_commit(self) -> str:
        return self.stack[-1][0]

    @property
    def best_metric(self) -> float:
        return self.stack[-1][1]

    @property
    def direction(self) -> str:
        return self.config["metric"]["direction"] if self.config else "lower"

    def streak(self) -> int:
        count = 0
        for trial in reversed(self.trials):
            if trial["status"] == "keep":
                break
            count += 1
        return count

    def counts(self) -> Dict[str, int]:
        counts = {"keep": 0, "discard": 0, "crash": 0, "timeout": 0, "checks_failed": 0}
        for trial in self.trials:
            counts[trial["status"]] = counts.get(trial["status"], 0) + 1
        return counts

    def noise_floor(self) -> Optional[float]:
        return median(self.noise) if self.noise else None


def replay(entries: List[Dict[str, Any]]) -> State:
    state = State()
    for entry in entries:
        kind = entry.get("type")
        if kind == "config":
            state.config = entry
            state.baseline = None
            state.stack = []
            state.trials = []
            state.stop = None
            state.noise = []
            state.max_iterations = entry.get("max_iterations")
            state.deadline = entry.get("deadline")
            state.target = entry.get("target")
            state.started = entry.get("time")
        elif kind == "baseline":
            state.baseline = entry
            state.stack = [[entry["commit"], entry["metric"]]]
        elif kind == "trial":
            state.trials.append(entry)
            if entry["status"] == "keep":
                state.stack.append([entry["commit"], entry["metric"]])
        elif kind == "recheck":
            state.stack[-1][1] = entry["metric"]
        elif kind == "undo":
            if len(state.stack) > 1:
                state.stack.pop()
        elif kind == "stop":
            state.stop = entry
        elif kind == "resume":
            state.stop = None
            for key in ("max_iterations", "deadline", "target"):
                if key in entry:
                    setattr(state, key, entry[key])
        elif kind == "note":
            state.notes.setdefault(entry.get("run") or 0, []).append(entry["text"])
        if kind in ("baseline", "trial", "recheck") and entry.get("noise") is not None:
            state.noise.append(entry["noise"])
        if kind == "trial":
            state.next_run = max(state.next_run, int(entry["run"]) + 1)
    return state


def effective(state: State, session: Session) -> Tuple[str, str]:
    """(status, reason): active, stopped, complete, or none."""
    if state.config is None or state.baseline is None:
        return "none", "no session; run init"
    if state.stop:
        status = "complete" if state.stop.get("by") == "target" else "stopped"
        return status, state.stop.get("reason", "")
    if state.target is not None and reached(state.best_metric, float(state.target), state.direction):
        return "complete", f"best {fmt(state.best_metric)} meets target {fmt(state.target)}"
    if session.stop_file.exists():
        return "stopped", f"stop requested ({session.rel(session.stop_file)} exists)"
    if state.deadline and utcnow() >= from_iso(state.deadline):
        return "stopped", "time budget used up"
    if state.max_iterations is not None and len(state.trials) >= state.max_iterations:
        return "stopped", f"iteration limit {state.max_iterations} reached"
    return "active", ""


def load(args: argparse.Namespace) -> Tuple[Path, Session, State]:
    repo = find_repo(getattr(args, "repo", None))
    session = Session(repo)
    state = replay(session.read())
    if state.config is None or state.baseline is None:
        raise ARError(f"no autoresearch session in {repo}; start one with `init` (see SKILL.md)")
    ensure_excluded(repo)
    return repo, session, state


def reached(value: float, target: float, direction: str) -> bool:
    return value <= target if direction == "lower" else value >= target


def gain(value: float, best: float, direction: str) -> float:
    """Positive when `value` is better than `best`."""
    return best - value if direction == "lower" else value - best


def threshold(config: Dict[str, Any], best: float) -> float:
    limit = float(config.get("min_delta") or 0)
    if config.get("min_rel"):
        limit = max(limit, abs(best) * float(config["min_rel"]))
    return limit


# --------------------------------------------------------------- measurement


class CommandResult:
    def __init__(self, returncode: Optional[int], timed_out: bool, duration: float, stdout: str, stderr: str):
        self.returncode = returncode
        self.timed_out = timed_out
        self.duration = duration
        self.stdout = stdout
        self.stderr = stderr


def kill_tree(proc: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=5)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            pass
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


def run_command(command: str, cwd: Path, timeout: float, log_path: Path, env_extra: Dict[str, str]) -> CommandResult:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    kwargs: Dict[str, Any] = {
        "cwd": str(cwd),
        "shell": True,
        "stdin": subprocess.DEVNULL,
        "env": dict(os.environ, **env_extra),
    }
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
        bash = shutil.which("bash")
        if bash:
            kwargs["executable"] = bash
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        started = time.monotonic()
        proc = subprocess.Popen(command, stdout=out, stderr=err, **kwargs)
        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_tree(proc)
        except KeyboardInterrupt:
            kill_tree(proc)
            raise
        duration = time.monotonic() - started
        out.seek(0)
        err.seek(0)
        stdout = out.read().decode("utf-8", "replace")
        stderr = err.read().decode("utf-8", "replace")
    log_path.write_text(
        f"$ {command}\n# exit={proc.returncode} timed_out={timed_out} seconds={duration:.2f}\n"
        f"--- stdout ---\n{stdout}\n--- stderr ---\n{stderr}",
        encoding="utf-8",
    )
    return CommandResult(proc.returncode, timed_out, duration, stdout, stderr)


def to_number(text: str) -> Optional[float]:
    try:
        value = float(text)
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def parse_metrics(stdout: str, stderr: str, primary: str) -> Dict[str, float]:
    """`METRIC name=value` lines win; otherwise the final stdout line (number or JSON object)."""
    found: Dict[str, float] = {}
    for text in (stdout, stderr):
        for line in text.splitlines():
            match = METRIC_RE.match(line)
            if match:
                value = to_number(match.group(2))
                if value is not None:
                    found[match.group(1)] = value
    if found:
        return found
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if not lines:
        return {}
    last = lines[-1]
    value = to_number(last)
    if value is not None:
        return {primary: value}
    if last.startswith("{"):
        try:
            payload = json.loads(last)
        except json.JSONDecodeError:
            return {}
        if isinstance(payload, dict):
            return {
                key: float(item)
                for key, item in payload.items()
                if isinstance(item, (int, float)) and not isinstance(item, bool) and math.isfinite(item)
            }
    return {}


def measure(session: Session, config: Dict[str, Any], label: str, runs: int, probe: bool = False) -> Dict[str, Any]:
    name = config["metric"]["name"]
    samples: List[Dict[str, float]] = []
    logs: List[str] = []
    total = 0.0
    wanted = runs
    while len(samples) < wanted:
        index = len(samples) + 1
        suffix = "" if wanted == 1 and not probe else f"-{index}"
        log_path = session.logs / f"{label}-measure{suffix}.log"
        env = {"AUTORESEARCH_DIR": str(session.dir), "AUTORESEARCH_RUN": label}
        result = run_command(config["measure"], session.repo, float(config["timeout"]), log_path, env)
        logs.append(session.rel(log_path))
        total += result.duration
        failure = None
        if result.timed_out:
            failure = ("timeout", f"measure timed out after {config['timeout']}s")
        elif result.returncode != 0:
            failure = ("crash", f"measure exited {result.returncode}")
        metrics = {} if failure else parse_metrics(result.stdout, result.stderr, name)
        if failure is None and name not in metrics:
            failure = ("crash", f"measure printed no `METRIC {name}=<number>` line and no final numeric line")
        if failure:
            return {
                "ok": False,
                "status": failure[0],
                "reason": failure[1],
                "tail": tail(result.stdout + ("\n" + result.stderr if result.stderr else "")),
                "logs": logs,
                "duration": round(total, 3),
            }
        samples.append(metrics)
        if probe and len(samples) == 1 and wanted == 1 and result.duration <= NOISE_PROBE_SECONDS:
            wanted = 3
    values = [sample[name] for sample in samples]
    secondary: Dict[str, float] = {}
    for sample in samples:
        for key in sample:
            if key != name and key not in secondary:
                secondary[key] = median([s[key] for s in samples if key in s])
    return {
        "ok": True,
        "metric": median(values),
        "metrics": secondary,
        "samples": values if len(values) > 1 else None,
        "noise": mad(values) if len(values) >= 3 else None,
        "logs": logs,
        "duration": round(total, 3),
    }


def run_checks(session: Session, config: Dict[str, Any], label: str) -> Dict[str, Any]:
    log_path = session.logs / f"{label}-checks.log"
    env = {"AUTORESEARCH_DIR": str(session.dir), "AUTORESEARCH_RUN": label}
    timeout = float(config.get("checks_timeout") or config["timeout"])
    result = run_command(config["checks"], session.repo, timeout, log_path, env)
    ok = not result.timed_out and result.returncode == 0
    report: Dict[str, Any] = {"ok": ok, "seconds": round(result.duration, 2), "log": session.rel(log_path)}
    if not ok:
        report["reason"] = f"timed out after {timeout:g}s" if result.timed_out else f"exit {result.returncode}"
        report["tail"] = tail(result.stdout + ("\n" + result.stderr if result.stderr else ""))
    return report


# --------------------------------------------------------------- side files


PROGRAM_TEMPLATE = """# Autoresearch program: {goal}

Living brief for this session. A fresh agent resumes from this file plus
`.autoresearch/ar status`. Humans steer the research by editing it.

## Objective
{goal}

## Metric
- Primary: `{metric}`{unit} ({direction} is better). Baseline {baseline}. Target: {target}.
- Measure: `{measure}` ({runs} run(s) per trial, median; timeout {timeout}s)
- Checks: {checks}
- Secondary metrics: {secondary}

## Scope
- Editable: {scope}
- Protected: {protect}

## Constraints
- (fill in: rules the experiments must respect, e.g. no new dependencies, keep the public API)

## Strategy notes
- (fill in: what produces the metric, where the cost or error comes from, the first hypotheses worth testing)

## What's been tried
- (update every few trials and after each keep: wins, dead ends with the reason they failed, open questions)
"""

IDEAS_TEMPLATE = """# Ideas backlog

Deferred hypotheses worth testing later. Prune entries once tried; note why.

"""


def write_launcher(session: Session) -> None:
    script = shlex.quote(str(SCRIPT))
    python = shlex.quote(sys.executable or "python3")
    session.launcher.write_text(
        "#!/bin/sh\n"
        "# agent-autoresearch controller for this session (generated by init)\n"
        f"PY={python}\n"
        '[ -x "$PY" ] || PY=python3\n'
        'DIR=$(cd "$(dirname "$0")" && pwd)\n'
        f'exec "$PY" {script} --repo "$DIR/.." "$@"\n',
        encoding="utf-8",
    )
    session.launcher.chmod(0o755)


def ensure_excluded(repo: Path) -> None:
    exclude = git_path(repo, "info/exclude")
    line = f"/{SESSION}/"
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    if line in existing.splitlines():
        return
    exclude.parent.mkdir(parents=True, exist_ok=True)
    with exclude.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(f"# agent-autoresearch session state\n{line}\n")


def norm_path(repo: Path, raw: str) -> str:
    value = raw.strip().replace("\\", "/")
    if not value:
        raise ARError("scope and protect paths cannot be empty")
    if any(char in value for char in "*?["):
        raise ARError(f"{raw!r}: give files or directories, not globs")
    path = Path(value)
    if path.is_absolute():
        try:
            value = path.resolve().relative_to(repo).as_posix()
        except ValueError:
            raise ARError(f"{raw!r} is outside the repository {repo}")
    while value.startswith("./"):
        value = value[2:]
    value = value.rstrip("/") or "."
    if value == ".." or value.startswith("../"):
        raise ARError(f"{raw!r} is outside the repository")
    if value == SESSION or value.startswith(SESSION + "/"):
        raise ARError(f"{raw!r}: the session directory is managed by the controller")
    return value


def within(path: str, prefixes: List[str]) -> bool:
    return any(prefix == "." or path == prefix or path.startswith(prefix + "/") for prefix in prefixes)


# ------------------------------------------------------------------ commands


def cmd_init(args: argparse.Namespace) -> int:
    repo = find_repo(args.repo)
    session = Session(repo)
    previous = replay(session.read())
    has_session = previous.config is not None and previous.baseline is not None
    if has_session and not (args.rebaseline or args.fresh):
        raise ARError(
            "a session already exists here (see `status`). Use `resume` to continue it, "
            "`init --rebaseline` to change the measurement on this branch, or `init --fresh` to archive it."
        )
    if args.rebaseline and not has_session:
        raise ARError("--rebaseline needs an existing session; run init without it")
    if git(repo, "ls-files", "--", SESSION).stdout.strip():
        raise ARError(f"{SESSION}/ is tracked by git; untrack it (git rm -r --cached {SESSION}) and commit first")
    ensure_excluded(repo)
    head = head_sha(repo)
    tree = snapshot(repo)
    if tree != tree_of(repo, "HEAD"):
        dirty = diff_paths(repo, "HEAD", tree)
        listed = ", ".join(dirty[:15]) + (" ..." if len(dirty) > 15 else "")
        raise ARError(f"uncommitted changes: {listed}. Commit or stash them so the baseline is reproducible.")

    if args.rebaseline:
        base = {k: v for k, v in previous.config.items() if k not in ("type", "time", "segment")}
        if branch_name(repo) != base["branch"]:
            raise ARError(f"--rebaseline must run on the session branch {base['branch']}")
        if head != previous.best_commit:
            raise ARError(f"HEAD must be the best commit {short(previous.best_commit)} to rebaseline")
        config = dict(base)
        segment = int(previous.config["segment"]) + 1
    else:
        missing = [flag for flag, value in (("--goal", args.goal), ("--metric", args.metric), ("--measure", args.measure)) if not value]
        if missing:
            raise ARError("init needs " + ", ".join(missing))
        config = {"schema": SCHEMA, "goal": " ".join(args.goal.split()), "metric": {"name": args.metric, "unit": "", "direction": "lower"}}
        segment = int(previous.config["segment"]) + 1 if previous.config else 0

    metric = dict(config["metric"])
    if args.metric:
        metric["name"] = args.metric
    if args.unit is not None:
        metric["unit"] = args.unit
    if args.direction:
        metric["direction"] = args.direction
    elif not args.rebaseline:
        raise ARError("init needs --direction lower|higher")
    config["metric"] = metric
    if args.goal:
        config["goal"] = " ".join(args.goal.split())
    overrides = {
        "measure": args.measure,
        "checks": args.checks,
        "timeout": args.timeout,
        "checks_timeout": args.checks_timeout,
        "runs": args.runs,
        "min_delta": args.min_delta,
        "min_rel": args.min_rel,
        "target": args.target,
        "max_iterations": args.max_iterations,
        "patience": args.patience,
    }
    for key, value in overrides.items():
        if value is not None:
            config[key] = value
    if args.no_checks:
        config["checks"] = None
    if args.scope:
        config["scope"] = [norm_path(repo, p) for p in args.scope]
    if args.protect:
        config["protect"] = [norm_path(repo, p) for p in args.protect]
    config.setdefault("scope", ["."])
    config.setdefault("protect", [])
    config.setdefault("checks", None)
    config.setdefault("timeout", 600)
    config.setdefault("runs", 1)
    config.setdefault("min_delta", 0.0)
    if args.budget_minutes is not None:
        config["deadline"] = iso(utcnow() + dt.timedelta(minutes=args.budget_minutes))
        config["budget_minutes"] = args.budget_minutes
    elif args.rebaseline and config.get("deadline"):
        config["deadline"] = previous.deadline
    if int(config["runs"]) < 1:
        raise ARError("--runs must be at least 1")
    overlap = [p for p in config["scope"] if p != "." and within(p, config["protect"])]
    if overlap:
        raise ARError(f"scope paths are inside protected paths: {', '.join(overlap)}")

    if args.fresh and session.dir.exists():
        stamp = utcnow().strftime("%Y%m%dT%H%M%SZ")
        archive = session.dir / "archive" / stamp
        archive.mkdir(parents=True)
        for child in session.dir.iterdir():
            if child.name != "archive":
                shutil.move(str(child), str(archive / child.name))
        previous = State()
        segment = 0
    session.logs.mkdir(parents=True, exist_ok=True)
    session.patches.mkdir(parents=True, exist_ok=True)

    with Lock(session.dir / "lock"):
        label = f"seg{segment}-baseline"
        result = measure(session, config, label, int(config["runs"]), probe=args.runs is None and not args.rebaseline)
        if snapshot(repo) != tree:
            changed = diff_paths(repo, tree, snapshot(repo))
            revert_to(repo, head)
            raise ARError(
                "the measure command changed the working tree (" + ", ".join(changed[:10]) + "); it was reverted. "
                "Write outputs to git-ignored paths or $AUTORESEARCH_DIR, then retry."
            )
        if not result["ok"]:
            raise ARError(
                f"baseline measurement failed: {result['reason']}\n{result['tail']}\n"
                f"full log: {result['logs'][-1]}\nFix the measure command, then run init again."
            )
        checks = None
        if config.get("checks"):
            checks = run_checks(session, config, label)
            if snapshot(repo) != tree:
                revert_to(repo, head)
                raise ARError("the checks command changed the working tree; it was reverted. Make it side-effect free.")
            if not checks["ok"]:
                raise ARError(
                    f"checks fail on the unmodified baseline ({checks['reason']}):\n{checks['tail']}\n"
                    f"full log: {checks['log']}\nFix them or choose different checks before starting."
                )

        if args.rebaseline:
            branch = config["branch"]
        elif args.branch == "current":
            branch = branch_name(repo)
            if not branch:
                raise ARError("HEAD is detached; pass --branch NAME to create a session branch")
        else:
            stamp = utcnow().astimezone().strftime("%Y%m%d-%H%M")
            branch = args.branch or f"autoresearch/{slug(args.tag or metric['name'])}-{stamp}"
            if git(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}", check=False).returncode == 0:
                raise ARError(f"branch {branch} already exists; pass --branch with a new name or --branch current")
            git(repo, "checkout", "-q", "-b", branch)
        config.update(branch=branch, base_commit=config.get("base_commit") or head)

        config_entry = session.append(dict(type="config", segment=segment, **config))
        baseline = {
            "type": "baseline",
            "segment": segment,
            "commit": head,
            "metric": result["metric"],
            "metrics": result["metrics"],
            "samples": result["samples"],
            "noise": result["noise"],
            "duration": result["duration"],
            "logs": result["logs"],
        }
        if checks:
            baseline["checks"] = {"ok": True, "seconds": checks["seconds"], "log": checks["log"]}
        session.append(baseline)
        if config.get("target") is not None and reached(result["metric"], float(config["target"]), metric["direction"]):
            session.append({"type": "stop", "segment": segment, "by": "target", "reason": "baseline already meets the target"})

    write_launcher(session)
    unit = f" {metric['unit']}" if metric.get("unit") else ""
    if not session.program.exists():
        session.program.write_text(
            PROGRAM_TEMPLATE.format(
                goal=config["goal"],
                metric=metric["name"],
                unit=f" ({metric['unit']})" if metric.get("unit") else "",
                direction=metric["direction"],
                baseline=fmt(result["metric"]),
                target=fmt(config.get("target")) if config.get("target") is not None else "none",
                measure=config["measure"],
                runs=config["runs"],
                timeout=config["timeout"],
                checks=f"`{config['checks']}`" if config.get("checks") else "none",
                secondary=", ".join(result["metrics"]) or "none",
                scope=", ".join(config["scope"]),
                protect=", ".join(config["protect"]) or "none",
            ),
            encoding="utf-8",
        )
    if not session.ideas.exists():
        session.ideas.write_text(IDEAS_TEMPLATE, encoding="utf-8")

    word = "Rebaselined" if args.rebaseline else "Initialized"
    print(f"{word} autoresearch segment {segment} on branch {config['branch']} (base {short(head)}).")
    print(f"Baseline {metric['name']} = {fmt(result['metric'])}{unit}  ({metric['direction']} is better; {result['duration']:.1f}s)")
    if result["metrics"]:
        print("Secondary: " + "  ".join(f"{k}={fmt(v)}" for k, v in result["metrics"].items()))
    if result["samples"]:
        spread = result["noise"] or 0.0
        share = spread / abs(result["metric"]) * 100 if result["metric"] else 0.0
        print(f"Noise: {len(result['samples'])} runs, MAD {fmt(spread)} ({share:.2f}% of median)")
        if share > 0.5 and int(config["runs"]) == 1:
            print(
                "  The metric is noisy. Consider `.autoresearch/ar init --rebaseline --runs 5 "
                f"--min-delta {fmt(2 * spread)}` so noise cannot pass as progress."
            )
    if checks:
        print(f"Checks pass ({checks['seconds']}s).")
    print(f"Scope: {', '.join(config['scope'])}   Protected: {', '.join(config['protect']) or 'none'}")
    limits = []
    if config.get("max_iterations"):
        limits.append(f"{config['max_iterations']} trials")
    if config.get("deadline"):
        limits.append(f"{config.get('budget_minutes')} min")
    if config.get("target") is not None:
        limits.append(f"target {fmt(config['target'])}")
    if config.get("patience"):
        limits.append(f"patience {config['patience']}")
    print(f"Limits: {', '.join(limits) or 'none (runs until stopped)'}")
    print(f"Session files: {SESSION}/ (git-ignored via .git/info/exclude). Controller: {session.rel(session.launcher)}")
    status, reason = effective(replay(session.read()), session)
    if status != "active":
        print(f"Session is {status}: {reason}.")
    else:
        print(
            "Next: complete .autoresearch/program.md (Constraints, Strategy notes), then loop: "
            "edit -> `.autoresearch/ar trial --description \"...\"` -> repeat until the controller says stop."
        )
    return 0


def decide(value: float, best: float, config: Dict[str, Any], simplification: bool) -> str:
    delta = gain(value, best, config["metric"]["direction"])
    limit = threshold(config, best)
    if delta > limit:
        return "improved"
    if simplification and delta >= -limit:
        return "simplification"
    return "worse"


def trial_message(run: int, args: argparse.Namespace, result: Dict[str, Any], config: Dict[str, Any], best: float) -> str:
    title = " ".join(args.description.split())
    lines = [f"autoresearch #{run}: {title[:72]}", ""]
    if args.hypothesis:
        lines.append(f"Hypothesis: {' '.join(args.hypothesis.split())}")
    payload = {config["metric"]["name"]: result["metric"], "best_before": best}
    payload.update(result["metrics"])
    lines.append("Result: " + json.dumps(payload, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def parse_asi(pairs: Optional[List[str]]) -> Dict[str, str]:
    asi: Dict[str, str] = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise ARError(f"--asi expects key=value, got {pair!r}")
        key, value = pair.split("=", 1)
        asi[key.strip()] = value.strip()
    return asi


def detach_trial(session: Session) -> int:
    if session.pending_pid.exists():
        try:
            if pid_alive(int(session.pending_pid.read_text().strip())):
                raise ARError("a detached trial is already running; use `wait`")
        except ValueError:
            pass
    argv = [arg for arg in sys.argv[1:] if arg != "--detach"]
    if "--repo" not in argv:
        argv = ["--repo", str(session.repo)] + argv
    with session.pending_out.open("w", encoding="utf-8") as out:
        proc = subprocess.Popen(
            [sys.executable or "python3", str(SCRIPT)] + argv,
            stdout=out,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            cwd=str(session.repo),
            start_new_session=os.name != "nt",
        )
    session.pending_pid.write_text(str(proc.pid), encoding="utf-8")
    print(f"Trial running in the background (pid {proc.pid}). Collect the verdict with `.autoresearch/ar wait`.")
    return 0


def cmd_trial(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    status, reason = effective(state, session)
    if status != "active":
        raise Halt(f"session is {status}: {reason}. Stop experimenting and report (`ar report`), or `ar resume` to continue.")
    if args.detach:
        return detach_trial(session)
    config = state.config
    with Lock(session.dir / "lock"):
        branch = branch_name(repo)
        if branch != config["branch"]:
            raise ARError(
                f"the session runs on branch {config['branch']} but HEAD is on {branch or 'a detached HEAD'}; "
                f"switch back with `git switch {config['branch']}`"
            )
        best, best_metric = state.best_commit, state.best_metric
        head = head_sha(repo)
        folded = 0
        if head != best:
            if not is_ancestor(repo, best, head):
                raise ARError(
                    f"HEAD {short(head)} is not on top of the best commit {short(best)}. "
                    f"Restore it with `git reset --hard {short(best)}` (drops uncommitted edits), then retry."
                )
            folded = int(git(repo, "rev-list", "--count", f"{best}..{head}").stdout.strip())
        tree = snapshot(repo)
        changed = diff_paths(repo, best, tree)
        if not changed:
            raise ARError("no changes to evaluate: edit files in scope first (trials compare the working tree to the best commit)")
        outside = [p for p in changed if not within(p, config["scope"])]
        guarded = [p for p in changed if within(p, config["protect"])]
        if outside or guarded:
            problems = []
            if outside:
                problems.append("outside the scope " + ", ".join(config["scope"]) + ": " + ", ".join(outside))
            if guarded:
                problems.append("protected: " + ", ".join(guarded))
            raise ARError(
                "this trial touches files it may not change (" + "; ".join(problems) + "). "
                f"Restore them with `git checkout {short(best)} -- <path>` (or delete new files), then retry."
            )
        run = state.next_run
        label = f"{run:04d}"
        session.patches.mkdir(parents=True, exist_ok=True)
        patch_path = session.patches / f"{label}.patch"
        patch_path.write_text(git(repo, "diff", "--binary", best, tree).stdout, encoding="utf-8")

        result = measure(session, config, label, int(config["runs"]))
        entry: Dict[str, Any] = {
            "type": "trial",
            "segment": config["segment"],
            "run": run,
            "description": " ".join(args.description.split()),
            "hypothesis": " ".join(args.hypothesis.split()) if args.hypothesis else None,
            "asi": parse_asi(args.asi) or None,
            "files": changed,
            "patch": session.rel(patch_path),
            "parent": best,
            "best_before": best_metric,
        }
        if args.simplification:
            entry["simplification"] = True
        if args.revisits:
            entry["revisits"] = args.revisits
        if folded:
            entry["folded_commits"] = folded
        verdict = None
        if not result["ok"]:
            status = result["status"]
        elif snapshot(repo) != tree:
            status = "crash"
            result["reason"] = "the measure command changed files in the working tree; measurements must be side-effect free"
            result["tail"] = ""
        else:
            verdict = decide(result["metric"], best_metric, config, args.simplification)
            status = "discard"
            if verdict != "worse":
                status = "keep"
                if config.get("checks"):
                    checks = run_checks(session, config, label)
                    if checks["ok"] and snapshot(repo) != tree:
                        checks.update(ok=False, reason="checks changed files in the working tree", tail="")
                    entry["checks"] = {k: checks[k] for k in ("ok", "seconds", "log", "reason") if k in checks}
                    if not checks["ok"]:
                        status = "checks_failed"
                        result["reason"] = f"checks failed ({checks['reason']})"
                        result["tail"] = checks.get("tail", "")
        entry.update(
            status=status,
            metric=result.get("metric"),
            metrics=result.get("metrics") or {},
            samples=result.get("samples"),
            noise=result.get("noise"),
            duration=result["duration"],
            logs=result["logs"],
        )
        if verdict == "simplification" and status == "keep":
            entry["kept_as"] = "simplification"
        if status in FAILED:
            entry["reason"] = result.get("reason")
        if status == "keep":
            entry["commit"] = commit_tree(repo, tree, best, head_sha(repo), config["branch"], trial_message(run, args, result, config, best_metric))
        else:
            revert_to(repo, best)
            entry["commit"] = None
        session.append(entry)
        state = replay(session.read())
        stop = stop_after_trial(state, session)
        if stop:
            session.append(stop)
            state = replay(session.read())
    print_trial(session, state, entry, result)
    run_hooks(session, state, entry)
    return 0


def stop_after_trial(state: State, session: Session) -> Optional[Dict[str, Any]]:
    segment = state.config["segment"]
    if state.target is not None and reached(state.best_metric, float(state.target), state.direction):
        return {"type": "stop", "segment": segment, "by": "target", "reason": f"best {fmt(state.best_metric)} meets target {fmt(state.target)}"}
    if state.max_iterations is not None and len(state.trials) >= state.max_iterations:
        return {"type": "stop", "segment": segment, "by": "limit", "reason": f"iteration limit {state.max_iterations} reached"}
    if state.deadline and utcnow() >= from_iso(state.deadline):
        return {"type": "stop", "segment": segment, "by": "budget", "reason": "time budget used up"}
    patience = state.config.get("patience")
    if patience and state.streak() >= int(patience):
        return {"type": "stop", "segment": segment, "by": "patience", "reason": f"{state.streak()} trials in a row without a keep"}
    if session.stop_file.exists():
        return {"type": "stop", "segment": segment, "by": "user", "reason": "stop requested via STOP file"}
    return None


def progress_line(state: State, session: Session) -> str:
    counts = state.counts()
    parts = [f"{len(state.trials)}" + (f"/{state.max_iterations}" if state.max_iterations else "") + " trials"]
    tally = [f"{counts[k]} {k}" for k in ("keep", "discard", "crash", "timeout", "checks_failed") if counts.get(k)]
    if tally:
        parts.append(", ".join(tally))
    left = minutes_left(state.deadline)
    if left is not None:
        parts.append(f"{max(left, 0):.0f} min left")
    parts.append(f"best {fmt(state.best_metric)} ({pct(state.best_metric, state.baseline['metric'])} vs baseline)")
    return " | ".join(parts)


def print_trial(session: Session, state: State, entry: Dict[str, Any], result: Dict[str, Any]) -> None:
    config = state.config
    name = config["metric"]["name"]
    run = entry["run"]
    status = entry["status"]
    best_before = entry["best_before"]
    ar = session.rel(session.launcher)
    if entry.get("metric") is not None:
        head = f"#{run} {status.upper()}  {name} {fmt(entry['metric'])}  (best was {fmt(best_before)}: {pct(entry['metric'], best_before)}; baseline {pct(entry['metric'], state.baseline['metric'])})"
    else:
        head = f"#{run} {status.upper()}  {entry.get('reason', '')}"
    if entry.get("metric") is not None and status in FAILED and entry.get("reason"):
        head += f"  [{entry['reason']}]"
    print(head)
    if entry.get("kept_as") == "simplification":
        print("  kept as a simplification: metric not worse, code simpler")
    if entry.get("metrics"):
        base = state.baseline.get("metrics") or {}
        print("  secondary: " + "  ".join(f"{k} {fmt(v)}" + (f" (base {fmt(base[k])})" if k in base else "") for k, v in entry["metrics"].items()))
    if status in FAILED:
        if result.get("tail"):
            print("  output tail:")
            print("    " + result["tail"].replace("\n", "\n    "))
        log = (entry.get("checks") or {}).get("log") if status == "checks_failed" else entry["logs"][-1]
        print(f"  full log: {log}")
    details = []
    if entry.get("checks"):
        details.append(f"checks {'pass' if entry['checks']['ok'] else 'FAIL'} {entry['checks']['seconds']}s")
    details.append(f"measure {entry['duration']:.1f}s")
    if status == "keep":
        details.append(f"commit {short(entry['commit'])}")
        if entry.get("folded_commits"):
            details.append(f"{entry['folded_commits']} manual commit(s) folded in")
    else:
        details.append(f"reverted to {short(entry['parent'])}")
        details.append(f"patch {entry['patch']} (re-apply: {ar} restore {run})")
    print("  " + " | ".join(details))
    floor = state.noise_floor()
    if floor and entry.get("metric") is not None and status == "keep":
        ratio = abs(gain(entry["metric"], best_before, state.direction)) / floor if floor else 0
        print(f"  noise floor (MAD) {fmt(floor)}; this gain = {ratio:.1f}x noise" + ("  -> run `recheck` before building on it" if ratio < 2 else ""))
    print("  session: " + progress_line(state, session))
    status_now, reason = effective(state, session)
    if status_now != "active":
        print(f"next: STOP. The session is {status_now} ({reason}). Run `{ar} report`, then summarize for the user.")
        return
    hints = []
    if status == "keep":
        hints.append("build on this. Does it remove the reason an earlier discard failed? If so, revisit it: `restore N`, adapt, `trial --revisits N`.")
    elif status in FAILED:
        hints.append(f"if the idea still has merit, fix it: `{ar} restore {run}`, repair, trial again; otherwise move on.")
    else:
        hints.append(f"record why it lost (`{ar} note --run {run} \"...\"`), then try the next hypothesis.")
    streak = state.streak()
    if streak >= 3:
        hints.append(f"{streak} trials in a row without a keep: re-read program.md and the measure output, then try something structurally different.")
    if len(state.trials) % 5 == 0:
        hints.append("update the \"What's been tried\" section of .autoresearch/program.md.")
    print("next: keep going. " + " ".join(hints))


def run_hooks(session: Session, state: State, entry: Dict[str, Any]) -> None:
    if not session.hooks.is_dir():
        return
    snapshot_info = {
        "goal": state.config["goal"],
        "metric_name": state.config["metric"]["name"],
        "direction": state.direction,
        "baseline_metric": state.baseline["metric"],
        "best_metric": state.best_metric,
        "run_count": len(state.trials),
    }
    payloads = {
        "after": {"event": "after", "cwd": str(session.repo), "run_entry": entry, "session": snapshot_info},
        "before": {"event": "before", "cwd": str(session.repo), "next_run": state.next_run, "last_run": entry, "session": snapshot_info},
    }
    for stage in ("after", "before"):
        hooks = sorted(p for p in session.hooks.iterdir() if p.stem == stage and p.is_file() and os.access(p, os.X_OK))
        for hook in hooks[:1]:
            try:
                proc = subprocess.run(
                    [str(hook)],
                    input=json.dumps(payloads[stage]),
                    capture_output=True,
                    text=True,
                    timeout=HOOK_TIMEOUT,
                    cwd=str(session.repo),
                )
                text = proc.stdout.strip()[:HOOK_OUTPUT_LIMIT]
                if proc.returncode != 0:
                    text = f"(hook exited {proc.returncode}) {proc.stderr.strip()[:500]}"
            except subprocess.TimeoutExpired:
                text = f"(hook timed out after {HOOK_TIMEOUT}s)"
            if text:
                print(f"hook {stage}: {text}")


def status_payload(state: State, session: Session) -> Dict[str, Any]:
    status, reason = effective(state, session)
    config = state.config
    counts = state.counts()
    return {
        "state": status,
        "reason": reason,
        "goal": config["goal"],
        "branch": config["branch"],
        "segment": config["segment"],
        "metric": config["metric"],
        "baseline": state.baseline["metric"],
        "best": state.best_metric,
        "best_commit": state.best_commit,
        "target": state.target,
        "trials": len(state.trials),
        "counts": counts,
        "streak": state.streak(),
        "max_iterations": state.max_iterations,
        "deadline": state.deadline,
        "minutes_left": None if state.deadline is None else round(max(minutes_left(state.deadline) or 0, 0), 1),
        "next_run": state.next_run,
        "noise_floor": state.noise_floor(),
    }


def trial_row(trial: Dict[str, Any], notes: Dict[int, List[str]]) -> str:
    value = fmt(trial.get("metric")) if trial.get("metric") is not None else "-"
    change = pct(trial.get("metric"), trial.get("best_before")) if trial.get("metric") is not None else "-"
    text = trial["description"]
    if trial.get("revisits"):
        text = f"[revisits #{trial['revisits']}] {text}"
    if trial["status"] in FAILED and trial.get("reason"):
        text += f" ({trial['reason']})"
    row = f"  #{trial['run']:<4} {trial['status']:<13} {value:>14} {change:>9}  {short(trial.get('commit')):<7}  {text}"
    for note in notes.get(trial["run"], []):
        row += f"\n{'':>8}note: {note}"
    return row


def cmd_status(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    payload = status_payload(state, session)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    config = state.config
    metric = config["metric"]
    ar = session.rel(session.launcher)
    print(f"agent-autoresearch: {config['goal']}")
    print(f"state {payload['state'].upper()}" + (f" ({payload['reason']})" if payload["reason"] else "") + f" | branch {config['branch']} | segment {config['segment']}")
    target = f" | target {fmt(state.target)}" if state.target is not None else ""
    print(
        f"metric {metric['name']} ({metric['direction']} is better) | baseline {fmt(state.baseline['metric'])} | "
        f"best {fmt(state.best_metric)} ({pct(state.best_metric, state.baseline['metric'])}) @ {short(state.best_commit)}{target}"
    )
    print("progress: " + progress_line(state, session) + f" | {state.streak()} without a keep")
    floor = state.noise_floor()
    if floor is not None:
        print(f"noise floor (MAD): {fmt(floor)}" + (" (deterministic)" if floor == 0 else ""))
    checks = f"`{config['checks']}`" if config.get("checks") else "none"
    print(f"measure: `{config['measure']}` x{config['runs']} (timeout {config['timeout']}s, min delta {fmt(threshold(config, state.best_metric))}) | checks: {checks}")
    print(f"scope: {', '.join(config['scope'])} | protected: {', '.join(config['protect']) or 'none'}")
    recent = state.trials[-RECENT:]
    if recent:
        print(f"recent trials ({len(recent)} of {len(state.trials)}; full list: {ar} log):")
        for trial in recent:
            print(trial_row(trial, state.notes))
    if session.pending_pid.exists():
        print(f"a detached trial may be running; collect it with `{ar} wait`")
    print(f"files: {session.rel(session.program)} | {session.rel(session.ideas)} | {session.rel(session.log)}")
    if payload["state"] == "active":
        print(f"next: continue the loop: one hypothesis, edit in scope, `{ar} trial --description \"...\"`.")
    else:
        print(f"next: the session is {payload['state']}; report results (`{ar} report`) or `{ar} resume` to continue.")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    entries = session.read()
    trials = [e for e in entries if e.get("type") == "trial"] if args.all else state.trials
    if args.json:
        print(json.dumps(trials, indent=2, ensure_ascii=False))
        return 0
    if args.tsv:
        keys: List[str] = []
        for trial in trials:
            for key in trial.get("metrics") or {}:
                if key not in keys:
                    keys.append(key)
        name = state.config["metric"]["name"]
        print("\t".join(["run", "commit", name, "status", *keys, "description"]))
        print("\t".join(["0", short(state.baseline["commit"]), str(state.baseline["metric"]), "baseline", *[str((state.baseline.get("metrics") or {}).get(k, "")) for k in keys], "baseline"]))
        for trial in trials:
            metrics = trial.get("metrics") or {}
            print("\t".join([str(trial["run"]), short(trial.get("commit")), "" if trial.get("metric") is None else str(trial["metric"]), trial["status"], *[str(metrics.get(k, "")) for k in keys], trial["description"].replace("\t", " ")]))
        return 0
    print(f"baseline {fmt(state.baseline['metric'])} @ {short(state.baseline['commit'])}")
    for trial in trials:
        print(trial_row(trial, state.notes))
    return 0


def cmd_measure(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    config = dict(state.config)
    label = "explore-" + utcnow().strftime("%Y%m%dT%H%M%S")
    result = measure(session, config, label, args.runs or int(config["runs"]))
    name = config["metric"]["name"]
    if not result["ok"]:
        print(f"measure failed: {result['reason']}\n{result['tail']}\nfull log: {result['logs'][-1]}")
        return 1
    print(f"{name} {fmt(result['metric'])} (best {fmt(state.best_metric)}: {pct(result['metric'], state.best_metric)}) [not recorded; only `trial` records]")
    if result["metrics"]:
        print("secondary: " + "  ".join(f"{k} {fmt(v)}" for k, v in result["metrics"].items()))
    if result["samples"]:
        print("samples: " + ", ".join(fmt(v) for v in result["samples"]))
    print(f"log: {result['logs'][-1]}")
    return 0


def require_at_best(repo: Path, state: State) -> None:
    if head_sha(repo) != state.best_commit or snapshot(repo) != tree_of(repo, state.best_commit):
        raise ARError(f"the working tree must be clean at the best commit {short(state.best_commit)} for this command")


def cmd_recheck(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    with Lock(session.dir / "lock"):
        require_at_best(repo, state)
        runs = args.runs or max(int(state.config["runs"]), 3)
        label = f"recheck-{state.next_run - 1:04d}-" + utcnow().strftime("%H%M%S")
        result = measure(session, state.config, label, runs)
        if not result["ok"]:
            raise ARError(f"recheck failed: {result['reason']}\nfull log: {result['logs'][-1]}")
        previous = state.best_metric
        session.append(
            {
                "type": "recheck",
                "segment": state.config["segment"],
                "commit": state.best_commit,
                "metric": result["metric"],
                "previous": previous,
                "samples": result["samples"],
                "noise": result["noise"],
                "logs": result["logs"],
            }
        )
    name = state.config["metric"]["name"]
    print(f"recheck {name} @ {short(state.best_commit)}: {fmt(result['metric'])} over {runs} runs (recorded best was {fmt(previous)}: {pct(result['metric'], previous)})")
    if result["noise"] is not None:
        print(f"noise (MAD): {fmt(result['noise'])}")
    print("The best metric now uses the rechecked value; later trials must beat it.")
    return 0


def cmd_undo(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    with Lock(session.dir / "lock"):
        require_at_best(repo, state)
        if len(state.stack) < 2:
            raise ARError("nothing to undo: the best commit is the baseline")
        dropped, restored = state.stack[-1], state.stack[-2]
        revert_to(repo, restored[0])
        session.append({"type": "undo", "segment": state.config["segment"], "commit": dropped[0], "restored": restored[0], "reason": args.reason})
    print(f"undid keep {short(dropped[0])}; best is {short(restored[0])} again ({fmt(restored[1])}). Its patch remains in .autoresearch/patches.")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    trial = next((e for e in session.read() if e.get("type") == "trial" and int(e["run"]) == args.run), None)
    if trial is None:
        raise ARError(f"no trial #{args.run} in the log")
    patch = session.repo / trial["patch"]
    if not patch.exists():
        raise ARError(f"patch for #{args.run} is missing: {trial['patch']}")
    if not args.force and snapshot(repo) != tree_of(repo, "HEAD"):
        raise ARError("the working tree has uncommitted changes; finish or revert them first (or pass --force to apply on top)")
    applied = git(repo, "apply", "--whitespace=nowarn", str(patch), check=False)
    if applied.returncode != 0:
        applied = git(repo, "apply", "--3way", "--whitespace=nowarn", str(patch), check=False)
    if applied.returncode != 0:
        raise ARError(f"patch #{args.run} no longer applies cleanly:\n{(applied.stderr or applied.stdout).strip()}")
    print(f"applied trial #{args.run} ({trial['status']}: {trial['description']}) to the working tree: {', '.join(trial['files'])}")
    if trial["status"] == "discard":
        print(f"if you retry it because an assumption changed, pass `--revisits {args.run}` to trial and say what changed")
    return 0


def cmd_note(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    run = args.run
    if run is None and state.trials:
        run = state.trials[-1]["run"]
    session.append({"type": "note", "segment": state.config["segment"], "run": run, "text": " ".join(args.text.split())})
    print(f"noted on #{run}" if run else "noted")
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    status, reason = effective(state, session)
    if status != "active":
        print(f"session already {status} ({reason})")
        return 0
    session.append({"type": "stop", "segment": state.config["segment"], "by": "user", "reason": args.reason})
    print(f"session stopped: {args.reason}. Best {fmt(state.best_metric)} @ {short(state.best_commit)}.")
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    entry: Dict[str, Any] = {"type": "resume", "segment": state.config["segment"]}
    if args.note:
        entry["note"] = " ".join(args.note.split())
    if args.more is not None:
        entry["max_iterations"] = len(state.trials) + args.more
    if args.max_iterations is not None:
        entry["max_iterations"] = args.max_iterations
    if args.no_limit:
        entry["max_iterations"] = None
        entry["deadline"] = None
    if args.budget_minutes is not None:
        entry["deadline"] = iso(utcnow() + dt.timedelta(minutes=args.budget_minutes))
    if args.target is not None:
        entry["target"] = args.target
    if session.stop_file.exists():
        session.stop_file.unlink()
    session.append(entry)
    state = replay(session.read())
    status, reason = effective(state, session)
    if status == "active":
        print("session active again. " + progress_line(state, session))
        if args.note:
            print(f"direction: {entry['note']}")
    else:
        print(f"session is still {status}: {reason}. Raise the limit (--more N, --budget-minutes M, --target X, or --no-limit).")
    return 0


def cmd_wait(args: argparse.Namespace) -> int:
    repo = find_repo(args.repo)
    session = Session(repo)
    if not session.pending_pid.exists():
        if session.pending_out.exists():
            print(session.pending_out.read_text(encoding="utf-8").rstrip())
            return 0
        raise ARError("no detached trial to wait for")
    pid = int(session.pending_pid.read_text().strip() or 0)
    deadline = time.monotonic() + args.timeout
    while pid_alive(pid) and time.monotonic() < deadline:
        time.sleep(2)
    if pid_alive(pid):
        print(f"trial (pid {pid}) is still running; run `wait` again")
        return 0
    session.pending_pid.unlink()
    print(session.pending_out.read_text(encoding="utf-8").rstrip())
    return 0


# -------------------------------------------------------------------- report


def render_chart(state: State) -> str:
    """Trials in order on x; dots per measured trial, a step line for the running best."""
    order = [(0, 0, state.baseline["metric"], "baseline")]
    order += [(i, t["run"], t.get("metric"), t["status"]) for i, t in enumerate(state.trials, 1)]
    measured = [p for p in order if p[2] is not None]
    if len(order) < 2:
        return ""
    width, height, pad = 720, 260, 44
    values = [p[2] for p in measured]
    lo, hi = min(values), max(values)
    if hi == lo:
        hi, lo = hi + 1, lo - 1
    x_max = len(order) - 1

    def x(index: float) -> float:
        return pad + (width - 2 * pad) * index / x_max

    def y(value: float) -> float:
        return height - pad - (height - 2 * pad) * (value - lo) / (hi - lo)

    path = [f"M{x(0):.1f},{y(state.baseline['metric']):.1f}"]
    for index, _run, value, status in measured[1:]:
        if status == "keep":
            path.append(f"H{x(index):.1f}V{y(value):.1f}")
    path.append(f"H{x(x_max):.1f}")
    dots = []
    for index, run, value, status in order:
        if value is None:
            dots.append(f'<text x="{x(index):.1f}" y="{height - pad + 16}" fill="var(--bad)" text-anchor="middle" font-size="12">x<title>#{run} {status}</title></text>')
            continue
        color = {"keep": "var(--keep)", "baseline": "var(--ink)"}.get(status, "var(--muted)")
        dots.append(f'<circle cx="{x(index):.1f}" cy="{y(value):.1f}" r="4" fill="{color}"><title>#{run} {status} {fmt(value)}</title></circle>')
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="metric per trial">'
        f'<line x1="{pad}" y1="{height - pad}" x2="{width - pad}" y2="{height - pad}" stroke="var(--line)"/>'
        f'<text x="{pad}" y="{pad - 12}" fill="var(--muted)" font-size="12">{html.escape(fmt(hi))}</text>'
        f'<text x="{pad}" y="{height - pad + 30}" fill="var(--muted)" font-size="12">{html.escape(fmt(lo))} (trials in order on x)</text>'
        f'<path d="{" ".join(path)}" fill="none" stroke="var(--keep)" stroke-width="2"/>' + "".join(dots) + "</svg>"
    )


def render_html(state: State, ideas: str) -> str:
    config = state.config
    name = config["metric"]["name"]
    rows = []
    for trial in state.trials:
        notes = "<br>".join(html.escape(n) for n in state.notes.get(trial["run"], []))
        asi = trial.get("asi") or {}
        extra = "; ".join(f"{html.escape(k)}: {html.escape(str(v))}" for k, v in asi.items())
        detail = " ".join(x for x in (html.escape(trial.get("hypothesis") or ""), extra, notes) if x)
        rows.append(
            f'<tr class="{trial["status"]}"><td>#{trial["run"]}</td><td>{trial["status"]}</td>'
            f'<td class="num">{fmt(trial.get("metric"))}</td><td class="num">{pct(trial.get("metric"), trial.get("best_before")) if trial.get("metric") is not None else "-"}</td>'
            f'<td><code>{short(trial.get("commit"))}</code></td><td>{html.escape(trial["description"])}</td><td class="muted">{detail}</td></tr>'
        )
    counts = state.counts()
    summary = ", ".join(f"{v} {k}" for k, v in counts.items() if v)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Autoresearch Report</title>
<style>
:root {{ --bg:#fbfaf8; --ink:#1d1d1f; --muted:#6b6b70; --line:#d9d6d0; --keep:#1f7a4d; --bad:#b3261e; --card:#fff; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#141416; --ink:#ececee; --muted:#9a9aa1; --line:#33333a; --keep:#4cc38a; --bad:#ff6b5e; --card:#1c1c1f; }} }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width:1000px; margin:0 auto; padding:24px 16px 48px; }}
h1 {{ font-size:22px; margin:0 0 4px; }} .muted {{ color:var(--muted); }}
.cards {{ display:flex; flex-wrap:wrap; gap:12px; margin:16px 0; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px 14px; min-width:140px; }}
.card b {{ display:block; font-size:20px; font-variant-numeric:tabular-nums; }}
svg {{ width:100%; height:auto; background:var(--card); border:1px solid var(--line); border-radius:8px; }}
.table {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; margin-top:16px; font-size:14px; }}
th, td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); vertical-align:top; }}
.num {{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }}
tr.keep td:nth-child(2) {{ color:var(--keep); font-weight:600; }} tr.crash td:nth-child(2), tr.timeout td:nth-child(2), tr.checks_failed td:nth-child(2) {{ color:var(--bad); }}
pre {{ white-space:pre-wrap; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px; }}
</style></head><body><main>
<h1>{html.escape(config['goal'])}</h1>
<div class="muted">branch <code>{html.escape(config['branch'])}</code> | {html.escape(name)} ({config['metric']['direction']} is better) | measure <code>{html.escape(config['measure'])}</code></div>
<div class="cards">
<div class="card"><span class="muted">baseline</span><b>{fmt(state.baseline['metric'])}</b></div>
<div class="card"><span class="muted">best</span><b>{fmt(state.best_metric)}</b><span class="muted">{pct(state.best_metric, state.baseline['metric'])}</span></div>
<div class="card"><span class="muted">trials</span><b>{len(state.trials)}</b><span class="muted">{html.escape(summary)}</span></div>
</div>
{render_chart(state)}
<div class="table"><table><thead><tr><th>run</th><th>status</th><th class="num">{html.escape(name)}</th><th class="num">vs best</th><th>commit</th><th>description</th><th>hypothesis / notes</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<h2>Ideas backlog</h2><pre>{html.escape(ideas)}</pre>
</main></body></html>
"""


def render_summary(state: State, ideas: str, repo: Path) -> str:
    config = state.config
    name = config["metric"]["name"]
    counts = state.counts()
    lines = [
        f"# Autoresearch: {config['goal']}",
        "",
        f"- Branch: `{config['branch']}` (base `{short(config['base_commit'])}`)",
        f"- Metric: `{name}` ({config['metric']['direction']} is better): baseline {fmt(state.baseline['metric'])} -> best {fmt(state.best_metric)} ({pct(state.best_metric, state.baseline['metric'])})",
        f"- Trials: {len(state.trials)} (" + ", ".join(f"{v} {k}" for k, v in counts.items() if v) + ")",
        f"- Measure: `{config['measure']}`" + (f"; checks: `{config['checks']}`" if config.get("checks") else ""),
        "",
        "## Kept changes",
        "",
        "| # | commit | metric | vs previous best | description |",
        "|---|--------|--------|------------------|-------------|",
    ]
    kept = [t for t in state.trials if t["status"] == "keep" and any(t["commit"] == c for c, _ in state.stack)]
    for trial in kept:
        lines.append(f"| {trial['run']} | `{short(trial['commit'])}` | {fmt(trial['metric'])} | {pct(trial['metric'], trial['best_before'])} | {trial['description']} |")
    lost = [t for t in state.trials if t["status"] != "keep"]
    if lost:
        lines += ["", "## Dead ends", ""]
        for trial in lost:
            why = "; ".join(state.notes.get(trial["run"], [])) or trial.get("reason") or ""
            value = f"{fmt(trial['metric'])} ({pct(trial['metric'], trial['best_before'])})" if trial.get("metric") is not None else trial["status"]
            lines.append(f"- #{trial['run']} {trial['description']}: {value}" + (f" - {why}" if why else ""))
    open_ideas = [line for line in ideas.splitlines() if line.strip().startswith(("-", "*"))]
    if open_ideas:
        lines += ["", "## Open ideas", ""] + open_ideas
    lines += [
        "",
        "## Review and land",
        "",
        f"- Commits: `git log --oneline {short(config['base_commit'])}..{config['branch']}`",
        f"- Squash into one change: `git switch -c <name> {short(config['base_commit'])} && git merge --squash {config['branch']}`",
        "",
    ]
    return "\n".join(lines)


def cmd_report(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    ideas = session.ideas.read_text(encoding="utf-8") if session.ideas.exists() else ""
    report = session.dir / "report.html"
    summary = session.dir / "summary.md"
    report.write_text(render_html(state, ideas), encoding="utf-8")
    summary.write_text(render_summary(state, ideas, repo), encoding="utf-8")
    status, reason = effective(state, session)
    print(f"{state.config['metric']['name']}: baseline {fmt(state.baseline['metric'])} -> best {fmt(state.best_metric)} ({pct(state.best_metric, state.baseline['metric'])}) | {progress_line(state, session)} | state {status}")
    print(f"report: {report}")
    print(f"summary: {summary}")
    return 0


# --------------------------------------------------------------------- relay


WORKER_PROMPT = """You are relay worker {worker} in an agent-autoresearch session: an autonomous loop that improves one metric through measured, reversible experiments. No human is watching, so decide for yourself and never ask questions.

Repository: {repo}
Goal: {goal}
Metric: {metric} ({direction} is better). Baseline {baseline}, best so far {best} after {trials} trials.
Controller: {ar}
Method (read the "Experiment loop" section if you need detail): {skill}

1. Orient: run `{ar} status`, then read {program} and {ideas}.
2. Run up to {per_worker} experiments, starting the first within a few steps. For each: pick one hypothesis from the evidence, edit files inside the scope, then run
   `{ar} trial --description "<what you changed>" --hypothesis "<why it should help>"`
   The controller measures, keeps or reverts, commits, and logs. Read its verdict before choosing the next experiment. Screening variants on a quick private probe is fine, but only `trial` adopts a change; note what screening ruled out.
3. Before you exit, record what you learned under "What's been tried" in {program} and append deferred ideas to {ideas}.

The controller owns git: leave commits, resets, stashes, and branch switches to it. Leave the measurement and protected files as they are. Exit as soon as the controller reports the session stopped or complete.
{extra}"""


def worker_command(args: argparse.Namespace) -> Tuple[Any, bool]:
    """Returns (command, shell). Prompt goes to stdin unless the template names {prompt} or {prompt_file}."""
    if args.agent_cmd:
        return args.agent_cmd, True
    preset = PRESETS.get(args.agent)
    if preset is None:
        raise ARError(f"unknown --agent {args.agent!r}; choose {', '.join(PRESETS)} or pass --agent-cmd")
    argv = list(preset["argv"])
    if args.model:
        argv += preset["model"] + [args.model]
    argv += preset.get("tail", [])
    if shutil.which(argv[0]) is None:
        raise ARError(f"{argv[0]} is not on PATH; install it or pass --agent-cmd")
    return argv, False


def cmd_relay(args: argparse.Namespace) -> int:
    repo, session, state = load(args)
    command, shell = worker_command(args)
    session.relay.mkdir(parents=True, exist_ok=True)
    idle = 0
    with Lock(session.dir / "relay.lock"):
        for worker in range(1, args.max_workers + 1):
            state = replay(session.read())
            status, reason = effective(state, session)
            if status != "active":
                print(f"relay: session {status} ({reason}); done")
                break
            before = len(state.trials)
            prompt = WORKER_PROMPT.format(
                worker=worker,
                repo=repo,
                goal=state.config["goal"],
                metric=state.config["metric"]["name"],
                direction=state.direction,
                baseline=fmt(state.baseline["metric"]),
                best=fmt(state.best_metric),
                trials=before,
                ar=shlex.quote(str(session.launcher)),
                skill=SKILL_DIR / "SKILL.md",
                program=session.program,
                ideas=session.ideas,
                per_worker=args.trials_per_worker,
                extra=(args.prompt_extra + "\n") if args.prompt_extra else "",
            )
            stem = session.relay / f"worker-{worker:03d}"
            prompt_file = stem.with_suffix(".prompt.md")
            prompt_file.write_text(prompt, encoding="utf-8")
            argv: Any = command
            stdin_text: Optional[str] = prompt
            if shell:
                argv = command.replace("{prompt_file}", shlex.quote(str(prompt_file))).replace("{prompt}", shlex.quote(prompt))
                if "{prompt" in command:
                    stdin_text = None
            print(f"relay: worker {worker} starting ({'custom command' if shell else ' '.join(command)})", flush=True)
            started = time.monotonic()
            with stem.with_suffix(".log").open("w", encoding="utf-8") as log:
                proc = subprocess.Popen(
                    argv,
                    shell=shell,
                    cwd=str(repo),
                    stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    text=True,
                    start_new_session=os.name != "nt",
                )
                try:
                    proc.communicate(input=stdin_text, timeout=args.worker_timeout)
                except subprocess.TimeoutExpired:
                    kill_tree(proc)
                    print(f"relay: worker {worker} hit the {args.worker_timeout}s worker timeout", flush=True)
                except KeyboardInterrupt:
                    kill_tree(proc)
                    print("relay: interrupted")
                    return 130
            state = replay(session.read())
            if branch_name(repo) != state.config["branch"]:
                print(f"relay: worker {worker} left HEAD off the session branch {state.config['branch']}; stopping. Inspect the repository by hand.")
                return 1
            leftover = snapshot(repo) != tree_of(repo, state.best_commit) or head_sha(repo) != state.best_commit
            if leftover and effective(state, session)[0] == "active":
                print(f"relay: worker {worker} left unevaluated changes; evaluating them", flush=True)
                leftover_args = argparse.Namespace(
                    repo=str(repo), description=f"relay worker {worker}: changes left without a trial",
                    hypothesis=None, asi=None, simplification=False, revisits=None, detach=False,
                )
                try:
                    cmd_trial(leftover_args)
                except ARError as exc:
                    print(f"relay: could not evaluate leftovers ({exc}); reverting to the best commit")
                    revert_to(repo, state.best_commit)
            state = replay(session.read())
            made = len(state.trials) - before
            elapsed = (time.monotonic() - started) / 60
            print(f"relay: worker {worker} exit {proc.returncode} after {elapsed:.1f} min, {made} trial(s); {progress_line(state, session)}", flush=True)
            idle = idle + 1 if made == 0 else 0
            if idle >= 2:
                print(f"relay: two workers in a row ran no trial; stopping. Inspect {session.rel(stem.with_suffix('.log'))}")
                break
    state = replay(session.read())
    print(f"relay finished: {progress_line(state, session)}")
    return 0


# ----------------------------------------------------------------------- cli


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="autoresearch.py",
        description="Controller for agent-autoresearch: measure, keep or revert, and log experiments.",
    )
    parser.add_argument("--repo", help="path inside the target git repository (default: current directory)")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    init = sub.add_parser("init", parents=[common], help="start a session: branch, baseline, session files")
    init.add_argument("--goal", help="what the research should achieve")
    init.add_argument("--metric", help="primary metric name as printed by the measure command")
    init.add_argument("--direction", choices=["lower", "higher"], help="which way is better")
    init.add_argument("--unit", help="display unit, e.g. ms, KB")
    init.add_argument("--measure", help="command that prints METRIC name=value lines (or a final numeric line)")
    init.add_argument("--checks", help="correctness gate run before any keep; exit 0 = pass")
    init.add_argument("--no-checks", action="store_true", help="drop the checks command (with --rebaseline)")
    init.add_argument("--scope", action="append", help="editable file or directory (repeatable; default: whole repo)")
    init.add_argument("--protect", action="append", help="file or directory trials may never change (repeatable)")
    init.add_argument("--target", type=float, help="stop as complete once the best metric reaches this")
    init.add_argument("--max-iterations", type=int, help="stop after this many trials")
    init.add_argument("--budget-minutes", type=float, help="stop starting trials after this many minutes")
    init.add_argument("--patience", type=int, help="stop after this many trials in a row without a keep")
    init.add_argument("--runs", type=int, help="measure runs per trial; the median counts (default 1)")
    init.add_argument("--min-delta", type=float, help="minimum absolute improvement that counts as a keep")
    init.add_argument("--min-rel", type=float, help="minimum relative improvement, e.g. 0.01 for 1%%")
    init.add_argument("--timeout", type=float, help="seconds before a measure run is killed (default 600)")
    init.add_argument("--checks-timeout", type=float, help="seconds before checks are killed (default: --timeout)")
    init.add_argument("--branch", help="session branch name, or 'current' to stay (default: new autoresearch/<tag>-<date>)")
    init.add_argument("--tag", help="short tag for the default branch name")
    init.add_argument("--rebaseline", action="store_true", help="new segment on this branch with a changed measurement")
    init.add_argument("--fresh", action="store_true", help="archive the existing session and start a new one")
    init.set_defaults(func=cmd_init)

    trial = sub.add_parser("trial", parents=[common], help="measure the working-tree change, then keep or revert it")
    trial.add_argument("--description", required=True, help="what this experiment changed")
    trial.add_argument("--hypothesis", help="why it should improve the metric")
    trial.add_argument("--asi", action="append", metavar="KEY=VALUE", help="extra notes for future iterations (repeatable)")
    trial.add_argument("--simplification", action="store_true", help="keep when the metric is not worse (the change simplifies code)")
    trial.add_argument("--revisits", type=int, metavar="N", help="this retries discarded trial N because an assumption changed")
    trial.add_argument("--detach", action="store_true", help="run in the background; collect the verdict with `wait`")
    trial.set_defaults(func=cmd_trial)

    status = sub.add_parser("status", parents=[common], help="session state, best result, recent trials")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=cmd_status)

    log = sub.add_parser("log", parents=[common], help="all trials of this segment")
    log.add_argument("--tsv", action="store_true", help="tab-separated, results.tsv style")
    log.add_argument("--json", action="store_true")
    log.add_argument("--all", action="store_true", help="include earlier segments")
    log.set_defaults(func=cmd_log)

    measure_cmd = sub.add_parser("measure", parents=[common], help="measure the working tree without recording anything")
    measure_cmd.add_argument("--runs", type=int)
    measure_cmd.set_defaults(func=cmd_measure)

    recheck = sub.add_parser("recheck", parents=[common], help="re-measure the best commit and use that value")
    recheck.add_argument("--runs", type=int)
    recheck.set_defaults(func=cmd_recheck)

    undo = sub.add_parser("undo", parents=[common], help="drop the latest keep and return to the previous best")
    undo.add_argument("--reason", required=True)
    undo.set_defaults(func=cmd_undo)

    restore = sub.add_parser("restore", parents=[common], help="re-apply a trial's saved patch to the working tree")
    restore.add_argument("run", type=int)
    restore.add_argument("--force", action="store_true", help="apply on top of uncommitted changes")
    restore.set_defaults(func=cmd_restore)

    note = sub.add_parser("note", parents=[common], help="attach a learning to a trial (default: the latest)")
    note.add_argument("text")
    note.add_argument("--run", type=int)
    note.set_defaults(func=cmd_note)

    stop = sub.add_parser("stop", parents=[common], help="end the session (it can be resumed)")
    stop.add_argument("--reason", default="stopped by request")
    stop.set_defaults(func=cmd_stop)

    resume = sub.add_parser("resume", parents=[common], help="reactivate a stopped session, optionally with new limits")
    resume.add_argument("--more", type=int, help="allow this many more trials")
    resume.add_argument("--max-iterations", type=int)
    resume.add_argument("--budget-minutes", type=float, help="new time budget starting now")
    resume.add_argument("--target", type=float)
    resume.add_argument("--no-limit", action="store_true", help="clear the iteration and time limits")
    resume.add_argument("--note", help="new direction for the research")
    resume.set_defaults(func=cmd_resume)

    wait = sub.add_parser("wait", parents=[common], help="wait for a detached trial and print its verdict")
    wait.add_argument("--timeout", type=float, default=500, help="seconds to block before returning (default 500)")
    wait.set_defaults(func=cmd_wait)

    report = sub.add_parser("report", parents=[common], help="write report.html and summary.md")
    report.set_defaults(func=cmd_report)

    relay = sub.add_parser("relay", parents=[common], help="drive the loop with fresh headless agent processes")
    relay.add_argument("--agent", default="claude", help="preset: " + ", ".join(PRESETS))
    relay.add_argument("--agent-cmd", help="custom shell template; prompt on stdin, or use {prompt} / {prompt_file}")
    relay.add_argument("--model", help="model passed to the preset agent")
    relay.add_argument("--trials-per-worker", type=int, default=5)
    relay.add_argument("--max-workers", type=int, default=100)
    relay.add_argument("--worker-timeout", type=float, default=3600)
    relay.add_argument("--prompt-extra", help="extra instructions appended to every worker prompt")
    relay.set_defaults(func=cmd_relay)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except ARError as exc:
        print(f"error: {exc}" if not isinstance(exc, Halt) else str(exc), file=sys.stderr)
        return exc.code
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
