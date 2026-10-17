#!/usr/bin/env python3
"""Tests for desk.py: the card lifecycle, the human gate and the rendered page.

Standard library only, no network. Every test drives the CLI in a throwaway
directory, so what is asserted is what the loops actually call.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import desk  # noqa: E402
import lockfile  # noqa: E402


def run_desk(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = desk.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def run_desk_stdin(text: str, *argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.object(sys, "stdin", io.StringIO(text)), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = desk.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def card(card_id: str = "123", **overrides) -> dict:
    payload = {
        "id": card_id,
        "kind": "issue",
        "repo": "owner/myapp",
        "number": 123,
        "url": "https://github.com/owner/myapp/issues/123",
        "title": "Crash on open",
        "author": "reporter",
        "verdict": "reply",
        "verdictLabel": "Answer",
        "summary": "answer the report",
        "draft": "Thanks, this is fixed by the next release.",
        "createdAt": "2026-10-14T06:33:00Z",
    }
    payload.update(overrides)
    return payload


class DeskTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.desk = Path(self._tmp.name).resolve() / "desk"
        self.desk.mkdir()

    def desk_args(self, *argv: str) -> tuple[int, str, str]:
        return run_desk("--state", str(self.desk), *argv)

    def put(self, payload: object) -> tuple[int, str, str]:
        text = payload if isinstance(payload, str) else json.dumps(payload)
        return run_desk_stdin(text, "--state", str(self.desk), "put", "--file", "-")

    def read(self, card_id: str) -> dict:
        return json.loads((self.desk / f"{card_id}.json").read_text(encoding="utf-8"))


class LifecycleTests(DeskTestCase):
    def test_put_list_approve_claim_sent_render(self) -> None:
        code, out, err = self.put(card("123"))
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["written"], ["123"])
        stored = self.read("123")
        self.assertEqual(stored["status"], "pending")
        self.assertEqual(stored["version"], 1)
        self.assertIsNone(stored["edited"])
        self.assertEqual(stored["note"], "")

        code, out, _ = self.desk_args("list", "--status", "pending")
        self.assertEqual(code, 0)
        self.assertIn("123", out)
        self.assertIn("answer the report", out)

        code, out, _ = self.desk_args("list", "--status", "sent")
        self.assertEqual(code, 0)
        self.assertIn("no cards", out)

        code, out, err = self.desk_args("approve", "123", "--note", "shorter please")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read("123")["status"], "approved")
        self.assertEqual(self.read("123")["note"], "shorter please")
        self.assertEqual(self.read("123")["version"], 2)

        code, out, err = self.desk_args("claim", "123")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read("123")["status"], "sending")

        code, out, err = self.desk_args("sent", "123", "--url", "https://github.com/owner/myapp/issues/123#issuecomment-1")
        self.assertEqual(code, 0, err)
        stored = self.read("123")
        self.assertEqual(stored["status"], "sent")
        self.assertEqual(stored["sentUrl"], "https://github.com/owner/myapp/issues/123#issuecomment-1")
        self.assertTrue(stored["sentAt"])

        code, out, _ = self.desk_args("render")
        self.assertEqual(code, 0)
        page = (self.desk / "index.html").read_text(encoding="utf-8")
        self.assertIn("<!DOCTYPE html>", page)
        self.assertIn("Thanks, this is fixed by the next release.", page)
        self.assertIn("Sent", page)

    def test_approve_with_an_edited_file_replaces_the_draft_on_the_page(self) -> None:
        self.put(card("123"))
        edited = self.desk / "edited.md"
        edited.write_text("A shorter answer.", encoding="utf-8")
        code, _, err = self.desk_args("approve", "123", "--edited-file", str(edited))
        self.assertEqual(code, 0, err)
        stored = self.read("123")
        self.assertEqual(stored["edited"], "A shorter answer.")
        self.assertEqual(stored["draft"], "Thanks, this is fixed by the next release.")
        self.desk_args("render")
        page = (self.desk / "index.html").read_text(encoding="utf-8")
        self.assertIn("A shorter answer.", page)
        self.assertNotIn("fixed by the next release", page)

    def test_put_accepts_a_card_file_with_a_utf8_bom(self) -> None:
        path = self.desk.parent / "card.json"
        path.write_text(json.dumps(card("bom-1")), encoding="utf-8-sig")
        self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))
        code, out, err = self.desk_args("put", "--file", str(path))
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["written"], ["bom-1"])
        self.assertEqual(self.read("bom-1")["draft"], "Thanks, this is fixed by the next release.")

    def test_approve_accepts_an_edited_file_with_a_utf8_bom(self) -> None:
        self.put(card("123"))
        edited = self.desk.parent / "edited.md"
        edited.write_text("A shorter answer.", encoding="utf-8-sig")
        code, _, err = self.desk_args("approve", "123", "--edited-file", str(edited))
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read("123")["edited"], "A shorter answer.")

    def test_json_on_disk_round_trips(self) -> None:
        payload = card("pr-9", kind="pr", verdict="merge", then="merge", headSha="abc123", order=4)
        self.put(payload)
        stored = self.read("pr-9")
        for key, value in payload.items():
            self.assertEqual(stored[key], value, key)
        self.assertEqual(stored["order"], 4)
        self.assertEqual(stored["then"], "merge")
        code, out, _ = self.desk_args("show", "pr-9")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), stored)

    def test_put_accepts_an_array_and_jsonl(self) -> None:
        code, out, err = self.put([card("1"), card("2")])
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["count"], 2)
        self.assertEqual(self.read("1")["status"], "pending")

        text = "\n".join(json.dumps(card(str(n))) for n in (3, 4))
        code, out, err = self.put(text)
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["written"], ["3", "4"])

    def test_put_keeps_unknown_fields(self) -> None:
        payload = card("1", maintainerNote="keep me", extra={"nested": [1, 2]})
        self.put(payload)
        stored = self.read("1")
        self.assertEqual(stored["maintainerNote"], "keep me")
        self.assertEqual(stored["extra"], {"nested": [1, 2]})

    def test_put_rejects_an_unknown_verdict(self) -> None:
        code, _, err = self.put(card("1", verdict="shrug"))
        self.assertEqual(code, 2)
        self.assertIn("verdict must be one of", err)

    def test_put_requires_head_sha_for_a_merge(self) -> None:
        code, _, err = self.put(card("1", then="merge"))
        self.assertEqual(code, 2)
        self.assertIn("needs headSha", err)


class HumanGateTests(DeskTestCase):
    def test_put_refuses_to_clobber_an_approved_card(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        code, _, err = self.put(card("123", draft="a different draft"))
        self.assertEqual(code, 3)
        self.assertIn("approved", err)
        self.assertEqual(self.read("123")["draft"], "Thanks, this is fixed by the next release.")
        self.assertEqual(self.read("123")["status"], "approved")

    def test_put_refuses_to_clobber_a_sent_card(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        self.desk_args("claim", "123")
        self.desk_args("sent", "123", "--url", "https://example.invalid/1")
        code, _, err = self.put(card("123", draft="clobbered"))
        self.assertEqual(code, 3)
        self.assertIn("sent", err)
        self.assertEqual(self.read("123")["status"], "sent")
        self.assertEqual(self.read("123")["draft"], "Thanks, this is fixed by the next release.")

    def test_put_refuses_to_clobber_a_sending_card(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        self.desk_args("claim", "123")
        code, _, err = self.put(card("123"))
        self.assertEqual(code, 3)
        self.assertEqual(self.read("123")["status"], "sending")

    def test_replace_overwrites_and_bumps_the_version(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        code, _, err = self._put_replace(card("123", draft="rewritten"))
        self.assertEqual(code, 0, err)
        stored = self.read("123")
        self.assertEqual(stored["draft"], "rewritten")
        self.assertEqual(stored["status"], "pending")
        self.assertEqual(stored["version"], 3)

    def _put_replace(self, payload: object) -> tuple[int, str, str]:
        return run_desk_stdin(
            json.dumps(payload), "--state", str(self.desk), "put", "--file", "-", "--replace"
        )

    def test_put_may_replace_a_pending_card(self) -> None:
        self.put(card("123"))
        code, _, err = self.put(card("123", draft="second draft"))
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read("123")["draft"], "second draft")
        self.assertEqual(self.read("123")["version"], 2)

    def test_claim_refuses_a_pending_card(self) -> None:
        self.put(card("123"))
        code, _, err = self.desk_args("claim", "123")
        self.assertEqual(code, 3)
        self.assertIn("not approved", err)
        self.assertEqual(self.read("123")["status"], "pending")

    def test_claim_refuses_a_second_claim(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        self.assertEqual(self.desk_args("claim", "123")[0], 0)
        code, _, err = self.desk_args("claim", "123")
        self.assertEqual(code, 3)
        self.assertIn("already sending", err)
        self.assertEqual(self.read("123")["status"], "sending")

    def test_claim_refuses_while_another_tick_holds_the_claim_lock(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        held = lockfile.acquire(self.desk, "claim-123", stale_seconds=3600)
        self.assertTrue(held["ok"])
        code, _, err = self.desk_args("claim", "123")
        self.assertEqual(code, 3)
        self.assertIn("claimed by another tick", err)
        self.assertEqual(self.read("123")["status"], "approved")

    def test_approve_refuses_a_card_that_is_not_pending_or_stale(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        code, _, err = self.desk_args("approve", "123")
        self.assertEqual(code, 3)
        self.assertIn("only a human moves pending or stale", err)

    def test_sent_refuses_a_card_that_was_never_claimed(self) -> None:
        self.put(card("123"))
        code, _, err = self.desk_args("sent", "123", "--url", "https://example.invalid/1")
        self.assertEqual(code, 3)
        self.assertIn("not sending", err)


class StaleAndDropTests(DeskTestCase):
    def test_stale_sets_the_reason_and_goes_back_to_the_maintainer(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        code, out, err = self.desk_args("stale", "123", "--reason", "reporter answered first")
        self.assertEqual(code, 0, err)
        stored = self.read("123")
        self.assertEqual(stored["status"], "stale")
        self.assertEqual(stored["staleReason"], "reporter answered first")
        self.assertTrue(stored["staleAt"])

        code, _, err = self.desk_args("approve", "123")
        self.assertEqual(code, 0, err)
        self.assertIsNone(self.read("123")["staleReason"])

    def test_a_stale_card_can_be_claimed_again(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        self.desk_args("stale", "123", "--reason", "thread moved")
        code, _, err = self.desk_args("claim", "123")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.read("123")["status"], "sending")

    def test_stale_refuses_a_sent_card(self) -> None:
        self.put(card("123"))
        self.desk_args("approve", "123")
        self.desk_args("claim", "123")
        self.desk_args("sent", "123", "--url", "https://example.invalid/1")
        code, _, err = self.desk_args("stale", "123", "--reason", "too late")
        self.assertEqual(code, 3)

    def test_drop_records_the_reason(self) -> None:
        self.put(card("123"))
        code, out, err = self.desk_args("drop", "123", "--reason", "duplicate")
        self.assertEqual(code, 0, err)
        stored = self.read("123")
        self.assertEqual(stored["status"], "dropped")
        self.assertEqual(stored["staleReason"], "duplicate")

    def test_note_appends_without_changing_the_status(self) -> None:
        self.put(card("123"))
        self.desk_args("note", "123", "say what happens next")
        self.desk_args("note", "123", "and keep it short")
        stored = self.read("123")
        self.assertEqual(stored["status"], "pending")
        self.assertEqual(stored["note"], "say what happens next\nand keep it short")

    def test_missing_card_is_a_usage_error(self) -> None:
        code, _, err = self.desk_args("show", "nope")
        self.assertEqual(code, 2)
        self.assertIn("no card nope", err)


class RenderTests(DeskTestCase):
    def test_render_groups_cards_and_escapes_the_draft(self) -> None:
        self.put(
            [
                card("1", draft="<script>alert(1)</script>"),
                card("2", status="pending"),
                card("3", status="approved"),
                card("4", status="sending"),
                card("5", status="sent", sentUrl="https://example.invalid/5", sentAt="2026-10-14T07:00:00Z"),
                card("6", status="stale", staleReason="thread moved"),
            ]
        )
        code, out, err = self.desk_args("render")
        self.assertEqual(code, 0, err)
        page = (self.desk / "index.html").read_text(encoding="utf-8")
        self.assertIn("Waiting for you", page)
        self.assertIn("Stale: the thread moved", page)
        self.assertIn("Approved, waiting for a tick", page)
        self.assertIn("Mid-send: a tick died", page)
        self.assertIn("Sent", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("6 card(s)", page)
        self.assertIn("thread moved", page)
        self.assertIn("https://example.invalid/5", page)

    def test_render_with_no_cards_says_so(self) -> None:
        code, out, err = self.desk_args("render")
        self.assertEqual(code, 0, err)
        page = (self.desk / "index.html").read_text(encoding="utf-8")
        self.assertIn("No cards.", page)


class GcTests(DeskTestCase):
    def test_gc_moves_only_old_sent_and_dropped_cards(self) -> None:
        self.put(
            [
                card("old-sent", status="sent", sentAt="2020-01-01T00:00:00Z"),
                card("new-sent", status="sent", sentAt=lockfile.iso(lockfile.utc_now())),
                card("old-dropped", status="dropped", droppedAt="2020-01-01T00:00:00Z"),
                card("still-pending", status="pending"),
            ]
        )
        code, out, err = self.desk_args("gc", "--older-than-days", "7")
        self.assertEqual(code, 0, err)
        self.assertEqual(sorted(json.loads(out)["archived"]), ["old-dropped", "old-sent"])
        archive = self.desk / "archive"
        self.assertTrue((archive / "old-sent.json").is_file())
        self.assertTrue((archive / "old-dropped.json").is_file())
        self.assertFalse((archive / "new-sent.json").exists())
        self.assertTrue((self.desk / "still-pending.json").is_file())
        self.assertTrue((self.desk / "new-sent.json").is_file())

    def test_gc_ignores_cards_whose_status_is_not_terminal(self) -> None:
        self.put(card("1", status="approved", createdAt="2020-01-01T00:00:00Z"))
        code, out, err = self.desk_args("gc", "--older-than-days", "1")
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["count"], 0)
        self.assertTrue((self.desk / "1.json").is_file())


class DeskLocationTests(unittest.TestCase):
    def test_state_defaults_to_the_repo_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            state = root / "state"
            (root / ".loop").mkdir()
            (root / ".loop" / "config.json").write_text(
                json.dumps({"stateDir": str(state)}), encoding="utf-8"
            )
            resolved = desk.resolve_desk(None, root)
            self.assertEqual(resolved, state / "desk")

    def test_loop_state_environment_is_the_last_resort(self) -> None:
        import os

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            os.environ["LOOP_STATE"] = str(root / "envstate")
            try:
                self.assertEqual(desk.resolve_desk(None, root), root / "envstate" / "desk")
            finally:
                del os.environ["LOOP_STATE"]

    def test_without_any_hint_it_is_a_usage_error(self) -> None:
        import os

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            os.environ.pop("LOOP_STATE", None)
            with self.assertRaises(desk.UsageError):
                desk.resolve_desk(None, root)


class UnitTests(unittest.TestCase):
    def test_normalize_fills_the_contract_defaults(self) -> None:
        normalized = desk.normalize_card({"id": "1"})
        self.assertEqual(normalized["kind"], "issue")
        self.assertEqual(normalized["status"], "pending")
        self.assertEqual(normalized["sendWith"], "next-tick")
        self.assertIsNone(normalized["then"])
        self.assertIsNone(normalized["edited"])
        self.assertEqual(normalized["note"], "")
        self.assertEqual(normalized["version"], 1)
        self.assertTrue(normalized["createdAt"])

    def test_render_page_is_deterministic(self) -> None:
        cards = [desk.normalize_card({"id": "1", "draft": "hello"})]
        self.assertEqual(desk.render_page(cards), desk.render_page(cards))


if __name__ == "__main__":
    unittest.main()
