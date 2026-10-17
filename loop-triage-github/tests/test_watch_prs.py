"""Tests for the GitHub loop's event watcher: no gh, no network, no sleeps.

The watcher's only outside dependency is the module-level ``RUNNER``, so every
test installs a fake that answers ``gh api`` from a route table and records the
calls it was asked to make. The recording is what proves the trust boundary: a
PR by someone else is answered from one endpoint and nothing else is read.
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "watch-prs.py"

# Loading the script by path must not leave a __pycache__ inside the skill.
sys.dont_write_bytecode = True

spec = importlib.util.spec_from_file_location("watch_prs", SCRIPT)
assert spec is not None and spec.loader is not None
watch_prs = importlib.util.module_from_spec(spec)
sys.modules["watch_prs"] = watch_prs
spec.loader.exec_module(watch_prs)

OWNER = "loopowner"
PR = "repos/acme/app/pulls/1"
HEAD = "abc1234567890"


class Result:
    """The part of subprocess.CompletedProcess the watcher uses."""

    def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class FakeGh:
    """A stand-in for RUNNER. Routes are keyed by api path without its query."""

    def __init__(self, routes=None, login: str = OWNER, login_error: str | None = None) -> None:
        self.routes = dict(routes or {})
        self.login = login
        self.login_error = login_error
        self.calls: list[list[str]] = []

    def __call__(self, argv: list[str]) -> Result:
        self.calls.append(list(argv))
        if argv[:2] == ["api", "user"]:
            if self.login_error is not None:
                return Result(1, "", self.login_error)
            return Result(0, self.login)
        path = argv[1] if len(argv) > 1 else ""
        route = self.routes.get(path.split("?", 1)[0])
        if route is None:
            return Result(1, "", f"gh: Not Found (HTTP 404) {path}")
        if isinstance(route, Exception):
            raise route
        return Result(0, json.dumps(route))

    def paths(self) -> list[str]:
        """Every PR endpoint read, in order. The login call is not a PR read."""
        return [
            call[1].split("?", 1)[0]
            for call in self.calls
            if call[:1] == ["api"] and call[1:2] != ["user"]
        ]


def pr_payload(author: str = OWNER, state: str = "open", merged: bool = False) -> dict:
    return {
        "number": 1,
        "state": state,
        "merged": merged,
        "user": {"login": author, "type": "User"},
        "head": {"sha": HEAD},
        "base": {"ref": "main"},
    }


def commits(*authors: tuple[str, str]) -> list[dict]:
    return [
        {"sha": sha, "author": {"login": login}, "commit": {"author": {"name": login}}}
        for login, sha in authors
    ]


def runs(*items: tuple[str, str]) -> dict:
    return {
        "check_runs": [
            {"name": name, "status": "completed", "conclusion": conclusion}
            for name, conclusion in items
        ]
    }


class WatchPrsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.state = Path(self.tmp.name)
        self._original_runner = watch_prs.RUNNER

    def tearDown(self) -> None:
        watch_prs.RUNNER = self._original_runner
        self.tmp.cleanup()

    def install(self, routes=None, login: str = OWNER, login_error: str | None = None) -> FakeGh:
        fake = FakeGh(routes, login=login, login_error=login_error)
        watch_prs.RUNNER = fake
        return fake

    def watch(self, repo: str = "acme/app", number: int = 1) -> None:
        (self.state / "watch.json").write_text(
            json.dumps([{"repo": repo, "number": number}]), encoding="utf-8"
        )

    def run_once(self, extra: list[str] | None = None) -> tuple[int, list[str]]:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = watch_prs.main(["--state", str(self.state), "--once", *(extra or [])])
        return code, [line for line in buffer.getvalue().splitlines() if line]

    def base_routes(self, **overrides) -> dict:
        """A followed PR whose checks are still running, so the first pass is quiet."""
        routes = {
            PR: pr_payload(),
            f"{PR}/commits": commits((OWNER, HEAD)),
            f"repos/acme/app/commits/{HEAD}/check-runs": {
                "check_runs": [{"name": "build", "status": "in_progress", "conclusion": None}]
            },
            f"repos/acme/app/commits/{HEAD}/status": {"statuses": []},
            f"{PR}/reviews": [],
            f"{PR}/comments": [],
            "repos/acme/app/issues/1/comments": [],
        }
        routes.update(overrides)
        return routes

    # -- first pass ---------------------------------------------------------

    def test_first_pass_records_without_reporting(self) -> None:
        """The tick that added the PR already knows its current state."""
        self.watch()
        self.install(
            self.base_routes(
                **{
                    f"{PR}/reviews": [
                        {
                            "id": 7,
                            "user": {"login": "coderabbitai[bot]", "type": "Bot"},
                            "state": "COMMENTED",
                        }
                    ]
                }
            )
        )
        code, lines = self.run_once()
        self.assertEqual(code, 0)
        self.assertEqual(lines, [])
        seen = json.loads((self.state / "watch-seen.json").read_text(encoding="utf-8"))
        self.assertEqual(seen["acme/app#1"]["ids"], ["REVIEW:7"])
        self.assertTrue(seen["acme/app#1"]["init"])

    # -- checks -------------------------------------------------------------

    def test_ci_done_green(self) -> None:
        self.watch()
        self.install(self.base_routes())
        self.run_once()  # first pass: still running
        self.install(self.base_routes(**{f"repos/acme/app/commits/{HEAD}/check-runs": runs(("build", "success"))}))
        code, lines = self.run_once()
        self.assertEqual(code, 0)
        self.assertEqual(lines, [f"CI_DONE acme/app#1 head={HEAD[:9]} green"])

    def test_ci_done_red_names_failing_and_skipped_checks(self) -> None:
        self.watch()
        self.install(self.base_routes())
        self.run_once()
        self.install(
            self.base_routes(
                **{
                    f"repos/acme/app/commits/{HEAD}/check-runs": runs(
                        ("build", "success"), ("unit", "failure"), ("android-e2e", "skipped")
                    )
                }
            )
        )
        _, lines = self.run_once()
        self.assertEqual(
            lines,
            [f"CI_DONE acme/app#1 head={HEAD[:9]} red unit skipped=android-e2e"],
        )

    def test_ci_done_waits_until_every_check_is_completed(self) -> None:
        self.watch()
        self.install(self.base_routes())
        self.run_once()
        self.install(
            self.base_routes(
                **{
                    f"repos/acme/app/commits/{HEAD}/check-runs": {
                        "check_runs": [
                            {"name": "build", "status": "completed", "conclusion": "success"},
                            {"name": "e2e", "status": "in_progress", "conclusion": None},
                        ]
                    }
                }
            )
        )
        _, lines = self.run_once()
        self.assertEqual(lines, [])

    def test_coderabbit_status_is_a_separate_event(self) -> None:
        """CodeRabbit reports a commit status, not a check run."""
        self.watch()
        self.install(self.base_routes())
        self.run_once()
        self.install(
            self.base_routes(
                **{
                    f"repos/acme/app/commits/{HEAD}/status": {
                        "statuses": [
                            {
                                "context": "CodeRabbit",
                                "state": "success",
                                "description": "Review completed",
                            },
                            {"context": "ci/other", "state": "failure", "description": "ignored"},
                        ]
                    }
                }
            )
        )
        _, lines = self.run_once()
        self.assertEqual(
            lines,
            [f"CODERABBIT_DONE acme/app#1 head={HEAD[:9]} success: Review completed"],
        )

    # -- reviews and comments ----------------------------------------------

    def test_trusted_and_untrusted_review_comment_and_comment(self) -> None:
        self.watch()
        self.install(self.base_routes())
        self.run_once()
        self.install(
            self.base_routes(
                **{
                    f"{PR}/reviews": [
                        {
                            "id": 11,
                            "user": {"login": "coderabbitai[bot]", "type": "Bot"},
                            "state": "CHANGES_REQUESTED",
                        },
                        {
                            "id": 12,
                            "user": {"login": "passerby", "type": "User"},
                            "state": "APPROVED",
                        },
                        {"id": 13, "user": {"login": OWNER, "type": "User"}, "state": "COMMENTED"},
                    ],
                    f"{PR}/comments": [
                        {
                            "id": 21,
                            "user": {"login": "coderabbitai[bot]", "type": "Bot"},
                            "path": "src/main.ts",
                        }
                    ],
                    "repos/acme/app/issues/1/comments": [
                        {"id": 31, "user": {"login": "passerby", "type": "User"}}
                    ],
                }
            )
        )
        _, lines = self.run_once()
        self.assertEqual(
            lines,
            [
                "REVIEW acme/app#1 trusted by coderabbitai[bot] CHANGES_REQUESTED",
                "REVIEW acme/app#1 untrusted by passerby APPROVED",
                "REVIEW_COMMENT acme/app#1 trusted by coderabbitai[bot] src/main.ts",
                "COMMENT acme/app#1 untrusted by passerby",
            ],
        )

    def test_an_event_is_reported_once(self) -> None:
        self.watch()
        self.install(self.base_routes())
        self.run_once()
        routes = self.base_routes(
            **{
                f"{PR}/reviews": [
                    {
                        "id": 11,
                        "user": {"login": "coderabbitai[bot]", "type": "Bot"},
                        "state": "COMMENTED",
                    }
                ]
            }
        )
        self.install(routes)
        _, first = self.run_once()
        self.install(routes)
        _, second = self.run_once()
        self.assertEqual(first, ["REVIEW acme/app#1 trusted by coderabbitai[bot] COMMENTED"])
        self.assertEqual(second, [])

    def test_trusted_logins_are_configurable(self) -> None:
        self.watch()
        self.install(self.base_routes())
        self.run_once()
        self.install(
            self.base_routes(
                **{
                    "repos/acme/app/issues/1/comments": [
                        {"id": 31, "user": {"login": "reviewbot[bot]", "type": "Bot"}}
                    ]
                }
            )
        )
        _, lines = self.run_once(["--trusted-login", "reviewbot[bot]"])
        self.assertEqual(lines, ["COMMENT acme/app#1 trusted by reviewbot[bot]"])

    # -- commits, state, foreign PRs ---------------------------------------

    def test_foreign_commit(self) -> None:
        self.watch()
        self.install(self.base_routes())
        self.run_once()
        self.install(
            self.base_routes(**{f"{PR}/commits": commits((OWNER, HEAD), ("driveby", "deadbeef1234"))})
        )
        _, lines = self.run_once()
        self.assertEqual(lines, ["FOREIGN_COMMIT acme/app#1 deadbeef1 by driveby"])

    def test_closed_merged(self) -> None:
        self.watch()
        self.install(self.base_routes())
        self.run_once()
        self.install(self.base_routes(**{PR: pr_payload(state="closed", merged=True)}))
        _, lines = self.run_once()
        self.assertEqual(lines, ["CLOSED acme/app#1 merged=true"])

    def test_closed_without_merge_reads_no_checks(self) -> None:
        self.watch()
        fake = self.install(self.base_routes(**{PR: pr_payload(state="closed", merged=False)}))
        _, lines = self.run_once()
        self.assertEqual(lines, ["CLOSED acme/app#1 merged=false"])
        self.assertNotIn(f"repos/acme/app/commits/{HEAD}/check-runs", fake.paths())

    def test_foreign_pr_is_skipped_without_reading_anything_else(self) -> None:
        """The trust boundary, asserted on the calls that were made."""
        self.watch()
        fake = self.install(self.base_routes(**{PR: pr_payload(author="stranger")}))
        code, lines = self.run_once()
        self.assertEqual(code, 0)
        self.assertEqual(lines, ["SKIPPED_NOT_OWNER acme/app#1 by stranger"])
        self.assertEqual(fake.paths(), [PR])

        # A second pass stays quiet, and still reads nothing else.
        fake.calls.clear()
        _, again = self.run_once()
        self.assertEqual(again, [])
        self.assertEqual(fake.paths(), [PR])

    def test_foreign_pr_that_is_closed_is_still_skipped(self) -> None:
        self.watch()
        fake = self.install(
            self.base_routes(**{PR: pr_payload(author="stranger", state="closed", merged=True)})
        )
        _, lines = self.run_once()
        self.assertEqual(lines, ["SKIPPED_NOT_OWNER acme/app#1 by stranger"])
        self.assertEqual(fake.paths(), [PR])

    # -- failures -----------------------------------------------------------

    def test_unreadable_login_errors_and_exits_1(self) -> None:
        self.watch()
        self.install(self.base_routes(), login_error="gh: not logged in to any hosts")
        code, lines = self.run_once()
        self.assertEqual(code, 1)
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("WATCH_ERROR cannot read the gh login:"), lines)
        self.assertIn("not logged in", lines[0])

    def test_empty_login_errors_and_exits_1(self) -> None:
        self.watch()
        self.install(self.base_routes(), login="")
        code, lines = self.run_once()
        self.assertEqual(code, 1)
        self.assertEqual(lines, ["WATCH_ERROR cannot read the gh login: empty login"])

    def test_a_failing_pr_reports_watch_error_and_the_others_still_run(self) -> None:
        (self.state / "watch.json").write_text(
            json.dumps([{"repo": "acme/app", "number": 1}, {"repo": "acme/app", "number": 2}]),
            encoding="utf-8",
        )
        routes = self.base_routes()
        routes["repos/acme/app/pulls/2"] = RuntimeError("boom")
        self.install(routes)
        code, lines = self.run_once()
        self.assertEqual(code, 0)
        self.assertEqual(lines, ["WATCH_ERROR acme/app#2 boom"])

    def test_no_state_directory_is_an_error(self) -> None:
        empty = Path(self.tmp.name) / "nowhere"
        empty.mkdir()
        previous_state = os.environ.pop("LOOP_STATE", None)
        previous_cwd = Path.cwd()
        try:
            os.chdir(empty)
            self.assertIsNone(watch_prs.resolve_state(None, Path.cwd()))
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = watch_prs.main(["--once"])
            lines = [line for line in buffer.getvalue().splitlines() if line]
        finally:
            os.chdir(previous_cwd)
            if previous_state is not None:
                os.environ["LOOP_STATE"] = previous_state
        self.assertEqual(code, 2)
        self.assertTrue(lines[0].startswith("WATCH_ERROR no state directory:"), lines)

    # -- plumbing -----------------------------------------------------------

    def test_missing_watch_list_is_quiet_and_creates_seen_state(self) -> None:
        self.install(self.base_routes())
        code, lines = self.run_once()
        self.assertEqual(code, 0)
        self.assertEqual(lines, [])
        self.assertEqual(json.loads((self.state / "watch-seen.json").read_text()), {})

    def test_state_defaults_to_loop_state_env(self) -> None:
        self.watch()
        self.install(self.base_routes())
        previous = os.environ.get("LOOP_STATE")
        os.environ["LOOP_STATE"] = str(self.state)
        try:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = watch_prs.main(["--once"])
        finally:
            if previous is None:
                os.environ.pop("LOOP_STATE", None)
            else:
                os.environ["LOOP_STATE"] = previous
        self.assertEqual(code, 0)
        self.assertTrue((self.state / "watch-seen.json").is_file())

    def test_resolve_state_reads_the_nearest_loop_config(self) -> None:
        project = Path(self.tmp.name) / "project"
        (project / "sub").mkdir(parents=True)
        (project / ".loop").mkdir()
        (project / ".loop" / "config.json").write_text(
            json.dumps({"stateDir": str(self.state)}), encoding="utf-8"
        )
        previous_state = os.environ.pop("LOOP_STATE", None)
        try:
            self.assertEqual(watch_prs.resolve_state(None, project / "sub"), self.state)
        finally:
            if previous_state is not None:
                os.environ["LOOP_STATE"] = previous_state

    def test_gh_json_surfaces_the_first_stderr_line(self) -> None:
        self.install(self.base_routes())
        with self.assertRaises(watch_prs.GhError) as caught:
            watch_prs.gh_json("repos/acme/app/pulls/99")
        self.assertEqual(
            str(caught.exception),
            "gh api repos/acme/app/pulls/99: gh: Not Found (HTTP 404) repos/acme/app/pulls/99",
        )

    def test_a_watch_list_with_a_utf8_bom_is_read(self) -> None:
        """A hand-edited state file on Windows often carries a BOM."""
        (self.state / "watch.json").write_text(
            json.dumps([{"repo": "acme/app", "number": 1}]), encoding="utf-8-sig"
        )
        self.install(self.base_routes(**{PR: pr_payload(author="stranger")}))
        code, lines = self.run_once()
        self.assertEqual(code, 0)
        self.assertEqual(lines, ["SKIPPED_NOT_OWNER acme/app#1 by stranger"])

    def test_a_corrupt_watch_list_is_an_error_not_silence(self) -> None:
        (self.state / "watch.json").write_text('{"repo": "acme/app", ', encoding="utf-8")
        self.install(self.base_routes())
        code, lines = self.run_once()
        self.assertEqual(code, 1)
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("WATCH_ERROR "), lines)
        self.assertIn("unreadable JSON", lines[0])

    def test_a_corrupt_dedupe_file_is_an_error_not_silence(self) -> None:
        self.watch()
        (self.state / "watch-seen.json").write_text("not json at all", encoding="utf-8")
        self.install(self.base_routes())
        code, lines = self.run_once()
        self.assertEqual(code, 1)
        self.assertIn("unreadable JSON", lines[0])

    def test_a_wrong_shaped_watch_list_is_an_error(self) -> None:
        (self.state / "watch.json").write_text('{"repo": "acme/app"}', encoding="utf-8")
        self.install(self.base_routes())
        code, lines = self.run_once()
        self.assertEqual(code, 1)
        self.assertTrue(lines[0].startswith("WATCH_ERROR "), lines)
        self.assertIn("expected a list", lines[0])

    def test_module_import_does_not_need_gh(self) -> None:
        self.assertIs(watch_prs.RUNNER, watch_prs.default_runner)


if __name__ == "__main__":
    unittest.main()
