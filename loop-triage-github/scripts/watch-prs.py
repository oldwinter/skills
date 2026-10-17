#!/usr/bin/env python3
"""Print one line per event on the pull requests the GitHub triage loop follows.

Wake-the-loop contract
----------------------
Run this under whatever the harness uses to watch a long-running command: a
background job, a log watcher, cron, Task Scheduler, or a systemd unit. **Each
stdout line is a wake-up.** Every event line is printed with ``flush=True`` the
moment it is seen, so a harness that reads this process's stream can start a
triage tick right away instead of waiting for the next scheduled one. Nothing
else is ever printed. The process runs until it is stopped; ``--once`` does a
single pass and exits, which is what tests and manual runs use.

What is watched
---------------
The watch list is re-read from ``<state>/watch.json`` on every pass, so a tick
that opens or closes a PR changes what is watched without restarting the
watcher: ``[{"repo": "owner/name", "number": 123}]``. What was already reported
is kept in ``<state>/watch-seen.json``, so a re-armed watcher neither repeats
events nor misses the ones that happened while it was down. The first time a PR
is seen, its current checks, reviews and comments are recorded without being
reported: the tick that put it on the list already knows about them.

Trust boundary
--------------
Only PRs authored by the account it runs as are read. Any other PR on the list
is reported as ``SKIPPED_NOT_OWNER`` and nothing else about it is requested: no
diff, files, commits, check runs, reviews or comments. A commit by anyone else
on a followed PR is reported as ``FOREIGN_COMMIT``, which stops the loop's work
on that PR. Each review and comment is tagged ``trusted`` when its author is in
the trusted-login set (default ``coderabbitai[bot]``; override with
``--trusted-login`` or ``WATCH_TRUSTED_LOGINS``) and ``untrusted`` otherwise;
the owner's own reviews and comments are not reported at all. The original
script hardcoded the review bot's login *and* its account type; here the set is
configuration, so a project may also trust a human maintainer's login. The text
of a review or comment is never printed, only its author, kind and location:
the watcher reads GitHub, it does not interpret it.

Owner login
-----------
The owner is ``gh api user --jq .login``. If it cannot be read, the watcher
prints ``WATCH_ERROR`` and exits 1 rather than mislabelling every PR as foreign.

Testability
-----------
Every ``gh`` call goes through the single module-level ``RUNNER``, so tests
drive the whole event logic with a fake and never need ``gh`` or the network.

State directory
---------------
``--state DIR`` wins; then ``$LOOP_STATE``; then the ``stateDir`` of the nearest
``.loop/config.json`` at or above the working directory. No state path, repo,
owner or interval is hardcoded.

Usage
-----
    watch-prs.py [--state DIR] [--once] [--interval SECONDS]
                 [--trusted-login LOGIN] [--status-context CONTEXT]

Exit codes: 0 one pass done (``--once``), 1 the owner login could not be read,
2 no state directory could be resolved.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

DEFAULT_INTERVAL = 60.0
# A failing PR is re-reported at most this often, so a broken endpoint cannot
# flood the stream with identical errors.
ERROR_REPORT_SECONDS = 600.0
# Conclusions that are not a pass. ``skipped`` is deliberately absent: a skipped
# job counts as not run, and it is reported separately.
RED = frozenset(
    {"failure", "cancelled", "timed_out", "action_required", "startup_failure", "stale"}
)
DEFAULT_TRUSTED_LOGINS = ("coderabbitai[bot]",)
# Review bots report a commit status, not a check run, so their "done" signal is
# read from the commit status contexts.
DEFAULT_STATUS_CONTEXTS = ("CodeRabbit",)


class GhError(RuntimeError):
    """A ``gh`` call failed, or returned something that cannot be used."""


class StateError(RuntimeError):
    """A state file exists but cannot be read: never treat that as quiet."""


def default_runner(argv: list[str]) -> Any:
    """Run ``gh <argv>`` and return a CompletedProcess-like object."""
    return subprocess.run(["gh", *argv], capture_output=True, text=True, timeout=60)


#: The one injectable seam: tests replace this with a fake.
RUNNER: Callable[[list[str]], Any] = default_runner


def first_line(text: str | None) -> str:
    lines = (text or "").strip().splitlines()
    return (lines[0] if lines else "no output")[:200]


def gh_json(path: str, jq: str | None = None) -> Any:
    """One ``gh api`` call, parsed as JSON.

    One page (``per_page=100``) covers a PR's runs, reviews and comments; older
    ``gh`` releases have no ``--slurp`` to merge pages. With ``jq``, a scalar
    result (``gh api user --jq .login``) is returned as the raw string.
    """
    argv = ["api", path] + (["--jq", jq] if jq else [])
    out = RUNNER(argv)
    if out.returncode != 0:
        raise GhError(f"gh api {path}: {first_line(out.stderr)}")
    text = (out.stdout or "").strip()
    if jq:
        # jq output is not always JSON (a string field comes back bare), so a
        # scalar result is returned as text rather than rejected.
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise GhError(f"gh api {path}: unreadable JSON ({exc})") from exc


def emit(line: str) -> None:
    """Print one event line and flush it: this is the wake-up signal."""
    print(line, flush=True)


def load_json(path: Path, default: Any) -> Any:
    """Read a state file. Missing means ``default``; unreadable means an error.

    A file that exists but cannot be parsed must never fall back to the default:
    an empty watch list and a corrupt one would both look like "quiet". The
    encoding is ``utf-8-sig`` because a state file hand-edited on Windows often
    carries a UTF-8 BOM, which plain ``utf-8`` turns into a parse error.
    """
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return default
    except OSError as exc:
        raise StateError(f"{path}: {exc}") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise StateError(f"{path}: unreadable JSON ({exc})") from exc


def save_json(path: Path, data: Any) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def check(
    repo: str,
    number: Any,
    me: str,
    seen: dict[str, Any],
    trusted: tuple[str, ...],
    contexts: tuple[str, ...],
) -> bool:
    """One pass over one watched PR. Returns False when the PR is not followed."""
    key = f"{repo}#{number}"
    state = seen.setdefault(key, {"ids": [], "done": []})
    first = not state.get("init")
    ids = set(state.get("ids", []))
    done = set(state.get("done", []))

    def remember() -> None:
        state.update(ids=sorted(ids), done=sorted(done), init=True)

    pr = gh_json(f"repos/{repo}/pulls/{number}")
    author = (pr.get("user") or {}).get("login") or "?"
    if author != me:
        # Trust boundary: stop here. Nothing else about this PR is requested.
        if "not-owner" not in done:
            done.add("not-owner")
            emit(f"SKIPPED_NOT_OWNER {key} by {author}")
        remember()
        return False

    head = (pr.get("head") or {}).get("sha") or ""
    for commit in gh_json(f"repos/{repo}/pulls/{number}/commits?per_page=100") or []:
        sha = commit.get("sha") or ""
        who = (
            (commit.get("author") or {}).get("login")
            or ((commit.get("commit") or {}).get("author") or {}).get("name")
            or "?"
        )
        if who != me and f"foreign:{sha}" not in done:
            done.add(f"foreign:{sha}")
            emit(f"FOREIGN_COMMIT {key} {sha[:9]} by {who}")

    if pr.get("state") != "open":
        if "closed" not in done:
            done.add("closed")
            emit(f"CLOSED {key} merged={str(bool(pr.get('merged'))).lower()}")
        remember()
        return False

    runs = (gh_json(f"repos/{repo}/commits/{head}/check-runs?per_page=100") or {}).get(
        "check_runs"
    ) or []
    if runs and all(r.get("status") == "completed" for r in runs) and f"ci:{head}" not in done:
        done.add(f"ci:{head}")
        failing = sorted(r.get("name") or "?" for r in runs if r.get("conclusion") in RED)
        skipped = sorted(r.get("name") or "?" for r in runs if r.get("conclusion") == "skipped")
        result = "red " + ",".join(failing) if failing else "green"
        extra = f" skipped={','.join(skipped)}" if skipped else ""
        if not first:
            emit(f"CI_DONE {key} head={head[:9]} {result}{extra}")

    statuses = (gh_json(f"repos/{repo}/commits/{head}/status") or {}).get("statuses") or []
    for status in statuses:
        if status.get("context") not in contexts:
            continue
        if status.get("state") == "pending" or f"cr:{head}" in done:
            continue
        done.add(f"cr:{head}")
        if not first:
            description = (status.get("description") or "")[:80]
            emit(f"CODERABBIT_DONE {key} head={head[:9]} {status.get('state')}: {description}")

    items = [
        ("REVIEW", r) for r in gh_json(f"repos/{repo}/pulls/{number}/reviews?per_page=100") or []
    ]
    items += [
        ("REVIEW_COMMENT", c)
        for c in gh_json(f"repos/{repo}/pulls/{number}/comments?per_page=100") or []
    ]
    items += [
        ("COMMENT", c) for c in gh_json(f"repos/{repo}/issues/{number}/comments?per_page=100") or []
    ]
    for kind, item in items:
        item_id = f"{kind}:{item.get('id')}"
        if item_id in ids:
            continue
        ids.add(item_id)
        user = item.get("user") or {}
        who = user.get("login") or "?"
        if first or who == me:
            continue
        tag = "trusted" if who in trusted else "untrusted"
        suffix = ""
        if kind == "REVIEW":
            suffix = f" {item.get('state')}"
        elif kind == "REVIEW_COMMENT":
            suffix = f" {item.get('path')}"
        emit(f"{kind} {key} {tag} by {who}{suffix}")

    remember()
    return True


def resolve_state(explicit: str | None, cwd: Path) -> Path | None:
    """--state, then $LOOP_STATE, then the nearest .loop/config.json stateDir."""
    if explicit:
        return Path(explicit).expanduser()
    env = os.environ.get("LOOP_STATE")
    if env:
        return Path(env).expanduser()
    for base in (cwd, *cwd.parents):
        config = base / ".loop" / "config.json"
        if not config.is_file():
            continue
        try:
            data = load_json(config, None)
        except StateError:
            continue  # a config that cannot be parsed is reported as "no state dir"
        state = data.get("stateDir") if isinstance(data, dict) else None
        if state:
            return Path(os.path.expanduser(str(state)))
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="watch-prs.py",
        description="Print one line per event on the followed pull requests.",
    )
    parser.add_argument("--state", default=None, help="state directory (default: $LOOP_STATE)")
    parser.add_argument("--once", action="store_true", help="do one pass and exit")
    parser.add_argument(
        "--interval",
        type=float,
        default=float(os.environ.get("WATCH_INTERVAL") or DEFAULT_INTERVAL),
        help="seconds between passes (default 60)",
    )
    parser.add_argument(
        "--trusted-login",
        action="append",
        default=None,
        help="a login whose reviews and comments are tagged trusted (repeatable)",
    )
    parser.add_argument(
        "--status-context",
        action="append",
        default=None,
        help="a commit status context that signals a finished review bot (repeatable)",
    )
    args = parser.parse_args(argv)

    state_dir = resolve_state(args.state, Path.cwd())
    if state_dir is None:
        emit(
            "WATCH_ERROR no state directory: pass --state, set LOOP_STATE, "
            "or run inside a repository with .loop/config.json"
        )
        return 2
    trusted = tuple(args.trusted_login or ()) or tuple(
        login for login in (os.environ.get("WATCH_TRUSTED_LOGINS") or "").split(",") if login
    ) or DEFAULT_TRUSTED_LOGINS
    contexts = tuple(args.status_context or ()) or DEFAULT_STATUS_CONTEXTS

    try:
        me = str(gh_json("user", jq=".login") or "").strip()
    except GhError as exc:
        emit(f"WATCH_ERROR cannot read the gh login: {exc}")
        return 1
    if not me:
        emit("WATCH_ERROR cannot read the gh login: empty login")
        return 1

    watch_path = state_dir / "watch.json"
    seen_path = state_dir / "watch-seen.json"
    state_dir.mkdir(parents=True, exist_ok=True)

    errors: dict[str, float] = {}
    while True:
        try:
            seen = load_json(seen_path, {})
            watch_list = load_json(watch_path, [])
        except StateError as exc:
            # A state file that exists but cannot be read is a failed read, not
            # an empty watch list: say so and stop rather than run blind.
            emit(f"WATCH_ERROR {exc}")
            return 1
        if not isinstance(watch_list, list) or not isinstance(seen, dict):
            emit(
                f"WATCH_ERROR {watch_path}: expected a list of "
                '{"repo": "owner/name", "number": N} entries'
            )
            return 1
        for entry in watch_list:
            repo = entry.get("repo") if isinstance(entry, dict) else None
            number = entry.get("number") if isinstance(entry, dict) else None
            key = f"{repo}#{number}"
            try:
                check(repo, number, me, seen, trusted, contexts)
                errors.pop(key, None)
            except Exception as exc:  # one bad PR must not stop the watch, but never stay silent
                if time.time() - errors.get(key, 0.0) > ERROR_REPORT_SECONDS:
                    errors[key] = time.time()
                    emit(f"WATCH_ERROR {key} {exc}")
        save_json(seen_path, seen)
        if args.once:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
