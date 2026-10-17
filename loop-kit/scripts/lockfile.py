#!/usr/bin/env python3
"""Exclusive tick locks and atomic JSON writes for the loop suite.

Standard library only, Windows and POSIX. A lock is a file created with
``O_CREAT | O_EXCL`` in the state directory, so two ticks racing for the same
loop cannot both win. Locks are advisory and age-based: a lock older than the
caller's stale threshold is reported and taken over, because a crashed tick
never releases its own.
"""

from __future__ import annotations

import json
import os
import socket
import tempfile
from datetime import datetime, timezone
from pathlib import Path

LOCK_SUFFIX = ".lock"
DEFAULT_STALE_SECONDS = 7200


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(ts: datetime) -> str:
    return ts.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def age_seconds(acquired_at: str, now: datetime | None = None) -> float | None:
    started = parse_iso(acquired_at)
    if started is None:
        return None
    return ((now or utc_now()) - started).total_seconds()


def read_json(path: Path, default: object = None) -> object:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return default
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, payload: object) -> None:
    """Write JSON atomically: a sibling temp file, then ``os.replace``."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(path.parent),
        prefix=path.name + ".",
        suffix=".tmp",
        delete=False,
    )
    try:
        with handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(handle.name, path)
    except BaseException:
        try:
            os.unlink(handle.name)
        except OSError:
            pass
        raise


def write_text(path: Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(path.parent),
        prefix=path.name + ".",
        suffix=".tmp",
        delete=False,
        newline="\n",
    )
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(handle.name, path)
    except BaseException:
        try:
            os.unlink(handle.name)
        except OSError:
            pass
        raise


def lock_path(state_dir: Path, name: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "-" for ch in name)
    return Path(state_dir) / f"tick-{safe}{LOCK_SUFFIX}"


def lock_state(state_dir: Path, name: str, stale_seconds: int = DEFAULT_STALE_SECONDS) -> dict:
    """Describe a lock without changing it."""
    path = lock_path(state_dir, name)
    payload = read_json(path)
    if not isinstance(payload, dict):
        return {
            "name": name,
            "path": str(path),
            "held": False,
            "stale": False,
            "payload": None,
            "ageSeconds": None,
        }
    age = age_seconds(str(payload.get("acquiredAt", "")))
    stale = age is not None and age > stale_seconds
    return {
        "name": name,
        "path": str(path),
        "held": True,
        "stale": stale,
        "payload": payload,
        "ageSeconds": age,
    }


def acquire(state_dir: Path, name: str, stale_seconds: int = DEFAULT_STALE_SECONDS) -> dict:
    """Take the lock. Returns a dict with ``ok`` and, on refusal, ``reason``."""
    state_dir = Path(state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    path = lock_path(state_dir, name)
    payload = {
        "name": name,
        "pid": os.getpid(),
        "host": socket.gethostname(),
        "acquiredAt": iso(utc_now()),
    }
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        current = lock_state(state_dir, name, stale_seconds)
        if current["held"] and not current["stale"]:
            return {"ok": False, "path": str(path), "reason": "held", "current": current}
        took_over = current["payload"] or {}
        try:
            path.unlink()
        except OSError as error:
            return {"ok": False, "path": str(path), "reason": f"unlink failed: {error}", "current": current}
        try:
            fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return {"ok": False, "path": str(path), "reason": "held", "current": lock_state(state_dir, name, stale_seconds)}
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        return {
            "ok": True,
            "path": str(path),
            "tookOver": True,
            "previous": took_over,
            "previousAgeSeconds": current["ageSeconds"],
            "payload": payload,
        }
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return {"ok": True, "path": str(path), "tookOver": False, "payload": payload}


def release(state_dir: Path, name: str) -> dict:
    path = lock_path(state_dir, name)
    current = lock_state(state_dir, name)
    try:
        path.unlink()
    except FileNotFoundError:
        return {"ok": False, "path": str(path), "reason": "not held"}
    except OSError as error:
        return {"ok": False, "path": str(path), "reason": f"unlink failed: {error}"}
    return {"ok": True, "path": str(path), "released": current["payload"]}
