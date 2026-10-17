#!/usr/bin/env python3
"""The Reply Desk: JSON cards in the state directory, rendered to static HTML.

Every outbound action a loop wants to take exists first as a card. A human
moves a card from ``pending`` (or ``stale``) to ``approved``; only then may a
loop ``claim`` it, which flips it to ``sending`` under an exclusive lock, do the
network call, and record ``sent``. The gate is the state machine, not the
rendered page: the page is how the human reads the drafts.

Exit codes: ``0`` ok, ``2`` usage or config error, ``3`` refused by state.

Standard library only; Windows and POSIX.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lockfile  # noqa: E402  (sibling module, resolved above)

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_STATE = 3

STATUSES = ("pending", "approved", "sending", "sent", "stale", "dropped")
HUMAN_STATUSES = ("pending", "stale")
SEND_STATUSES = ("approved", "sending", "sent")
LOCKED_BY_PUT = ("approved", "sending", "sent")
CLAIMABLE = ("approved", "stale")
KINDS = ("issue", "pr", "social")
VERDICTS = ("reply", "close", "merge", "request-changes", "retitle")
SEND_WITH = ("next-tick", "fix-pr")
THEN = (None, "close", "merge")
DEFAULT_STALE_SECONDS = 900
DEFAULT_GC_DAYS = 7

CARD_DEFAULTS: dict = {
    "id": None,
    "kind": "issue",
    "repo": None,
    "number": None,
    "where": None,
    "url": None,
    "title": "",
    "author": "",
    "lastComment": None,
    "verdict": "reply",
    "verdictLabel": "",
    "summary": "",
    "decision": None,
    "fix": None,
    "sendWith": "next-tick",
    "then": None,
    "headSha": None,
    "newTitle": None,
    "draft": "",
    "edited": None,
    "note": "",
    "status": "pending",
    "staleReason": None,
    "order": 0,
    "createdAt": None,
    "sentAt": None,
    "sentUrl": None,
    "version": 1,
}

GROUP_ORDER = ("pending", "stale", "approved", "sending", "sent", "dropped")
GROUP_TITLES = {
    "pending": "Waiting for you",
    "stale": "Stale: the thread moved",
    "approved": "Approved, waiting for a tick",
    "sending": "Mid-send: a tick died",
    "sent": "Sent",
    "dropped": "Dropped",
}


class StateRefusal(Exception):
    """The card state refuses the operation (exit code 3)."""


class UsageError(Exception):
    """Bad arguments or unusable configuration (exit code 2)."""


def now_iso() -> str:
    return lockfile.iso(lockfile.utc_now())


# --------------------------------------------------------------------------
# desk location
# --------------------------------------------------------------------------


def resolve_desk(state_arg: str | None, repo_root: Path) -> Path:
    """``--state`` wins, then the repo config's stateDir, then ``$LOOP_STATE``."""
    if state_arg:
        return Path(state_arg).expanduser()
    config_path = Path(repo_root) / ".loop" / "config.json"
    config = lockfile.read_json(config_path)
    if isinstance(config, dict) and config.get("stateDir"):
        return Path(os.path.expanduser(str(config["stateDir"]))) / "desk"
    env = os.environ.get("LOOP_STATE")
    if env:
        return Path(os.path.expanduser(env)) / "desk"
    raise UsageError(
        "no desk: pass --state, or run loopkit.py init to write .loop/config.json, "
        "or set LOOP_STATE"
    )


# --------------------------------------------------------------------------
# card storage
# --------------------------------------------------------------------------


def card_path(desk: Path, card_id: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "-" for ch in str(card_id))
    if not safe:
        raise UsageError("card id is empty")
    return Path(desk) / f"{safe}.json"


def normalize_card(raw: object) -> dict:
    if not isinstance(raw, dict):
        raise UsageError("a card must be a JSON object")
    card = dict(CARD_DEFAULTS)
    card.update(raw)
    if not card.get("id"):
        raise UsageError("a card needs an id")
    if card["kind"] not in KINDS:
        raise UsageError(f"card {card['id']}: kind must be one of {', '.join(KINDS)}")
    if card["verdict"] not in VERDICTS:
        raise UsageError(f"card {card['id']}: verdict must be one of {', '.join(VERDICTS)}")
    if card["sendWith"] not in SEND_WITH:
        raise UsageError(f"card {card['id']}: sendWith must be one of {', '.join(SEND_WITH)}")
    if card["then"] not in THEN:
        raise UsageError(f"card {card['id']}: then must be null, close or merge")
    if card["status"] not in STATUSES:
        raise UsageError(f"card {card['id']}: status must be one of {', '.join(STATUSES)}")
    if card["then"] == "merge" and not card.get("headSha"):
        raise UsageError(f"card {card['id']}: then=merge needs headSha")
    if not card.get("createdAt"):
        card["createdAt"] = now_iso()
    try:
        card["version"] = max(1, int(card.get("version") or 1))
    except (TypeError, ValueError):
        card["version"] = 1
    try:
        card["order"] = int(card.get("order") or 0)
    except (TypeError, ValueError):
        card["order"] = 0
    return card


def load_card(desk: Path, card_id: str) -> dict:
    path = card_path(desk, card_id)
    payload = lockfile.read_json(path)
    if not isinstance(payload, dict):
        raise UsageError(f"no card {card_id} in {desk}")
    return payload


def save_card(desk: Path, card: dict) -> None:
    lockfile.write_json(card_path(desk, card["id"]), card)


def read_cards(desk: Path, statuses: tuple[str, ...] | None = None) -> list[dict]:
    if not Path(desk).is_dir():
        return []
    cards: list[dict] = []
    for path in sorted(Path(desk).glob("*.json")):
        payload = lockfile.read_json(path)
        if not isinstance(payload, dict) or "id" not in payload:
            continue
        if statuses is not None and payload.get("status") not in statuses:
            continue
        cards.append(payload)
    cards.sort(key=lambda card: (int(card.get("order") or 0), str(card.get("id"))))
    return cards


def parse_cards(text: str) -> list[dict]:
    """Accept one card object, an array of cards, or one card per JSON line."""
    text = text.strip()
    if not text:
        raise UsageError("no card data on stdin")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict):
        return [normalize_card(payload)]
    if isinstance(payload, list):
        return [normalize_card(item) for item in payload]
    cards: list[dict] = []
    for number, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            cards.append(normalize_card(json.loads(line)))
        except json.JSONDecodeError as error:
            raise UsageError(f"line {number} is not JSON: {error}") from error
    if not cards:
        raise UsageError("no cards found in the input")
    return cards


def read_text_file(path: str) -> str:
    """Read a hand-editable text file.

    ``utf-8-sig`` accepts a BOM, which Notepad and other Windows editors add by
    default, and is otherwise identical to ``utf-8``.
    """
    try:
        return Path(path).expanduser().read_text(encoding="utf-8-sig")
    except OSError as error:
        raise UsageError(f"cannot read {path}: {error}") from error


def read_input(path_arg: str | None) -> str:
    if path_arg in (None, "-"):
        return sys.stdin.read()
    return read_text_file(path_arg)


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------


def cmd_put(desk: Path, args: argparse.Namespace) -> int:
    cards = parse_cards(read_input(args.file))
    written: list[str] = []
    for card in cards:
        path = card_path(desk, card["id"])
        existing = lockfile.read_json(path)
        if isinstance(existing, dict):
            if existing.get("status") in LOCKED_BY_PUT and not args.replace:
                raise StateRefusal(
                    f"{card['id']} is {existing.get('status')}; "
                    "the maintainer's decision stands. Use --replace to overwrite it, "
                    "or draft a follow-up card with a new id."
                )
            card["version"] = max(1, int(existing.get("version") or 1)) + 1
        save_card(desk, card)
        written.append(str(card["id"]))
    print(json.dumps({"written": written, "count": len(written)}, sort_keys=True))
    return EXIT_OK


def cmd_list(desk: Path, args: argparse.Namespace) -> int:
    statuses: tuple[str, ...] | None = None
    if args.status:
        statuses = tuple(part.strip() for part in args.status.split(",") if part.strip())
        unknown = [name for name in statuses if name not in STATUSES]
        if unknown:
            raise UsageError(f"unknown status: {', '.join(unknown)}")
    cards = read_cards(desk, statuses)
    if args.json:
        print(json.dumps(cards, indent=2, sort_keys=True))
        return EXIT_OK
    if not cards:
        print("no cards")
        return EXIT_OK
    for card in cards:
        draft = card.get("edited") or card.get("draft") or ""
        first_line = draft.strip().splitlines()[0] if draft.strip() else ""
        print(
            f"{card.get('status'):9} {card.get('id'):20} {card.get('kind'):6} "
            f"{(card.get('verdict') or ''):15} {card.get('summary') or first_line}"
        )
    print(f"{len(cards)} card(s)")
    return EXIT_OK


def cmd_show(desk: Path, args: argparse.Namespace) -> int:
    card = load_card(desk, args.id)
    print(json.dumps(card, indent=2, sort_keys=True))
    return EXIT_OK


def cmd_approve(desk: Path, args: argparse.Namespace) -> int:
    card = load_card(desk, args.id)
    status = card.get("status")
    if status not in HUMAN_STATUSES:
        raise StateRefusal(
            f"{args.id} is {status}; only a human moves pending or stale to approved"
        )
    if args.edited_file is not None:
        card["edited"] = read_text_file(args.edited_file)
    if args.note is not None:
        card["note"] = args.note
    card["status"] = "approved"
    card["staleReason"] = None
    card["approvedAt"] = now_iso()
    card["version"] = int(card.get("version") or 1) + 1
    save_card(desk, card)
    print(f"approved {args.id}")
    return EXIT_OK


def cmd_drop(desk: Path, args: argparse.Namespace) -> int:
    card = load_card(desk, args.id)
    if card.get("status") == "sent":
        raise StateRefusal(f"{args.id} is sent; nothing to drop")
    card["status"] = "dropped"
    if args.reason:
        card["staleReason"] = args.reason
    card["droppedAt"] = now_iso()
    card["version"] = int(card.get("version") or 1) + 1
    save_card(desk, card)
    print(f"dropped {args.id}")
    return EXIT_OK


def cmd_note(desk: Path, args: argparse.Namespace) -> int:
    card = load_card(desk, args.id)
    if card.get("status") == "sent":
        raise StateRefusal(f"{args.id} is sent; notes on sent cards are the nightly review's job")
    existing = (card.get("note") or "").strip()
    card["note"] = f"{existing}\n{args.text}".strip() if existing else args.text
    card["version"] = int(card.get("version") or 1) + 1
    save_card(desk, card)
    print(f"noted {args.id}")
    return EXIT_OK


def cmd_claim(desk: Path, args: argparse.Namespace) -> int:
    """approved|stale -> sending, atomically.

    The card is re-read inside an exclusive lock so two ticks cannot both claim
    it, and a second claim of a card already ``sending`` is refused.
    """
    desk = Path(desk)
    desk.mkdir(parents=True, exist_ok=True)
    lock_name = f"claim-{args.id}"
    taken = lockfile.acquire(desk, lock_name, stale_seconds=args.stale_seconds)
    if not taken["ok"]:
        raise StateRefusal(f"{args.id} is claimed by another tick ({taken['reason']})")
    try:
        card = load_card(desk, args.id)
        status = card.get("status")
        if status == "sending":
            raise StateRefusal(
                f"{args.id} is already sending: a previous tick died mid-send. "
                "Report it and re-read the thread; never resend."
            )
        if status not in CLAIMABLE:
            raise StateRefusal(f"{args.id} is {status}, not approved; claim refuses it")
        card["status"] = "sending"
        card["claimedAt"] = now_iso()
        card["version"] = int(card.get("version") or 1) + 1
        save_card(desk, card)
    finally:
        lockfile.release(desk, lock_name)
    print(f"claimed {args.id}")
    return EXIT_OK


def cmd_sent(desk: Path, args: argparse.Namespace) -> int:
    card = load_card(desk, args.id)
    if card.get("status") not in ("sending", "approved"):
        raise StateRefusal(f"{args.id} is {card.get('status')}, not sending; nothing was sent")
    card["status"] = "sent"
    card["sentAt"] = now_iso()
    card["sentUrl"] = args.url
    card["version"] = int(card.get("version") or 1) + 1
    save_card(desk, card)
    print(f"sent {args.id} {args.url}")
    return EXIT_OK


def cmd_stale(desk: Path, args: argparse.Namespace) -> int:
    card = load_card(desk, args.id)
    if card.get("status") == "sent":
        raise StateRefusal(f"{args.id} is sent; a sent card cannot go stale")
    card["status"] = "stale"
    card["staleReason"] = args.reason
    card["staleAt"] = now_iso()
    card["version"] = int(card.get("version") or 1) + 1
    save_card(desk, card)
    print(f"stale {args.id}: {args.reason}")
    return EXIT_OK


def cmd_gc(desk: Path, args: argparse.Namespace) -> int:
    desk = Path(desk)
    archive = desk / "archive"
    cutoff = lockfile.utc_now() - timedelta(days=args.older_than_days)
    moved: list[str] = []
    for card in read_cards(desk, ("sent", "dropped")):
        stamp = card.get("sentAt") or card.get("droppedAt") or card.get("createdAt")
        when = lockfile.parse_iso(str(stamp or ""))
        if when is None or when > cutoff:
            continue
        archive.mkdir(parents=True, exist_ok=True)
        source = card_path(desk, card["id"])
        try:
            os.replace(source, archive / source.name)
        except OSError as error:
            raise UsageError(f"cannot archive {card['id']}: {error}") from error
        moved.append(str(card["id"]))
    print(json.dumps({"archived": moved, "count": len(moved)}, sort_keys=True))
    return EXIT_OK


# --------------------------------------------------------------------------
# render
# --------------------------------------------------------------------------


def render_page(cards: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {name: [] for name in GROUP_ORDER}
    for card in cards:
        grouped.setdefault(str(card.get("status")), []).append(card)
    total = len(cards)
    waiting = len(grouped.get("pending", [])) + len(grouped.get("stale", []))
    parts: list[str] = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Reply Desk</title>",
        "<style>",
        ":root { color-scheme: light dark; }",
        "body { font: 15px/1.5 system-ui, sans-serif; margin: 0; padding: 1.5rem; max-width: 60rem; }",
        "h1 { font-size: 1.4rem; margin: 0 0 .25rem; }",
        "h2 { font-size: 1.05rem; margin: 2rem 0 .5rem; border-bottom: 1px solid currentColor; padding-bottom: .25rem; }",
        ".meta { opacity: .7; font-size: .85rem; }",
        ".card { border: 1px solid currentColor; border-radius: .5rem; padding: .75rem 1rem; margin: .75rem 0; }",
        ".card h3 { margin: 0 0 .25rem; font-size: 1rem; }",
        "pre { white-space: pre-wrap; background: rgba(127,127,127,.15); padding: .6rem; border-radius: .35rem; }",
        ".row { display: flex; gap: .75rem; flex-wrap: wrap; font-size: .85rem; opacity: .85; }",
        ".draft { border-left: 3px solid currentColor; padding-left: .6rem; }",
        ".tag { border: 1px solid currentColor; border-radius: 1rem; padding: 0 .5rem; font-size: .75rem; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Reply Desk</h1>",
        f'<p class="meta">{total} card(s), {waiting} waiting on you. '
        "Approve, edit or drop a card with <code>desk.py</code>, then run <code>desk.py render</code> again.</p>",
    ]
    if not cards:
        parts.append("<p>No cards. The loops have drafted nothing.</p>")
    for status in GROUP_ORDER:
        group = grouped.get(status) or []
        if not group:
            continue
        parts.append(f"<h2>{html.escape(GROUP_TITLES.get(status, status))} ({len(group)})</h2>")
        for card in group:
            draft = card.get("edited") if card.get("edited") is not None else card.get("draft")
            where = card.get("where") or card.get("repo") or ""
            number = card.get("number")
            if number is not None and card.get("repo"):
                where = f"{card['repo']}#{number}"
            parts.append('<article class="card">')
            parts.append(f"<h3>{html.escape(str(card.get('title') or card.get('id')))}</h3>")
            parts.append(
                '<p class="row">'
                f'<span class="tag">{html.escape(str(card.get("status")))}</span>'
                f'<span class="tag">{html.escape(str(card.get("kind")))}</span>'
                f'<span class="tag">{html.escape(str(card.get("verdict")))}</span>'
                f'<span>id {html.escape(str(card.get("id")))}</span>'
                f'<span>{html.escape(str(where))}</span>'
                f'<span>author {html.escape(str(card.get("author") or ""))}</span>'
                f'<span>created {html.escape(str(card.get("createdAt") or ""))}</span>'
                f'<span>version {html.escape(str(card.get("version")))}</span>'
                "</p>"
            )
            if card.get("summary"):
                parts.append(f'<p>{html.escape(str(card["summary"]))}</p>')
            if card.get("decision"):
                parts.append(f'<p><strong>Decision:</strong> {html.escape(str(card["decision"]))}</p>')
            if card.get("staleReason"):
                parts.append(f'<p><strong>Stale:</strong> {html.escape(str(card["staleReason"]))}</p>')
            if card.get("note"):
                parts.append(f'<p><strong>Note:</strong> {html.escape(str(card["note"]))}</p>')
            last = card.get("lastComment")
            if isinstance(last, dict):
                parts.append(
                    f'<p class="meta">last comment by {html.escape(str(last.get("author") or ""))} '
                    f'at {html.escape(str(last.get("at") or ""))}</p>'
                )
                parts.append(f'<pre>{html.escape(str(last.get("text") or ""))}</pre>')
            parts.append('<div class="draft"><p class="meta">draft</p>')
            parts.append(f"<pre>{html.escape(str(draft or ''))}</pre></div>")
            if card.get("sentUrl"):
                parts.append(
                    f'<p class="meta">sent at {html.escape(str(card.get("sentAt") or ""))}: '
                    f'{html.escape(str(card["sentUrl"]))}</p>'
                )
            parts.append("</article>")
    parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts) + "\n"


def cmd_render(desk: Path, args: argparse.Namespace) -> int:
    desk = Path(desk)
    desk.mkdir(parents=True, exist_ok=True)
    cards = read_cards(desk)
    page = render_page(cards)
    lockfile.write_text(desk / "index.html", page)
    print(f"rendered {len(cards)} card(s) to {desk / 'index.html'}")
    return EXIT_OK


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="desk.py",
        description="Reply Desk: the human approval gate for loop outbound actions.",
    )
    parser.add_argument("--state", default=None, help="desk directory (default: the repo config's stateDir/desk, else $LOOP_STATE/desk)")
    parser.add_argument("--repo-root", default=".", help="repository root used to find .loop/config.json")
    sub = parser.add_subparsers(dest="command", required=True)

    put = sub.add_parser("put", help="write one card, an array of cards, or JSONL")
    put.add_argument("--file", default="-", help="card file, or - for stdin")
    put.add_argument("--replace", action="store_true", help="overwrite a card in approved/sending/sent")
    put.set_defaults(func=cmd_put)

    listing = sub.add_parser("list", help="list cards")
    listing.add_argument("--status", default=None, help="comma-separated statuses")
    listing.add_argument("--json", action="store_true", help="emit JSON")
    listing.set_defaults(func=cmd_list)

    show = sub.add_parser("show", help="print one card as JSON")
    show.add_argument("id")
    show.set_defaults(func=cmd_show)

    approve = sub.add_parser("approve", help="human: pending|stale -> approved")
    approve.add_argument("id")
    approve.add_argument("--edited-file", default=None, help="replace the draft with this file's text")
    approve.add_argument("--note", default=None, help="maintainer feedback for the loop")
    approve.set_defaults(func=cmd_approve)

    drop = sub.add_parser("drop", help="human: stop a card")
    drop.add_argument("id")
    drop.add_argument("--reason", default=None)
    drop.set_defaults(func=cmd_drop)

    note = sub.add_parser("note", help="append maintainer feedback to a card")
    note.add_argument("id")
    note.add_argument("text")
    note.set_defaults(func=cmd_note)

    claim = sub.add_parser("claim", help="loop: approved|stale -> sending, atomic")
    claim.add_argument("id")
    claim.add_argument("--stale-seconds", type=int, default=DEFAULT_STALE_SECONDS)
    claim.set_defaults(func=cmd_claim)

    sent = sub.add_parser("sent", help="loop: record that the card was posted")
    sent.add_argument("id")
    sent.add_argument("--url", required=True)
    sent.set_defaults(func=cmd_sent)

    stale = sub.add_parser("stale", help="loop: the thread moved, back to the maintainer")
    stale.add_argument("id")
    stale.add_argument("--reason", required=True)
    stale.set_defaults(func=cmd_stale)

    render = sub.add_parser("render", help="write index.html")
    render.set_defaults(func=cmd_render)

    gc = sub.add_parser("gc", help="move old sent/dropped cards to archive/")
    gc.add_argument("--older-than-days", type=int, default=DEFAULT_GC_DAYS)
    gc.set_defaults(func=cmd_gc)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        desk = resolve_desk(args.state, Path(args.repo_root))
        return int(args.func(desk, args))
    except StateRefusal as error:
        print(f"refused: {error}", file=sys.stderr)
        return EXIT_STATE
    except UsageError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_USAGE
    except BrokenPipeError:
        return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
