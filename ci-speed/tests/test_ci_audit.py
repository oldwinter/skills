"""Tests for the CI audit's timing, forge detection, and trace parsing helpers."""

from __future__ import annotations

import datetime as dt
import io
import re
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ci_audit  # noqa: E402

START = dt.datetime(2026, 1, 1, 12, 0, 0, tzinfo=dt.UTC)


class SecondsTests(unittest.TestCase):
    def test_missing_endpoints_count_as_zero(self) -> None:
        self.assertEqual(ci_audit.seconds(None, START), 0.0)
        self.assertEqual(ci_audit.seconds(START, None), 0.0)

    def test_never_returns_negative_time(self) -> None:
        self.assertEqual(ci_audit.seconds(START, START - dt.timedelta(seconds=5)), 0.0)

    def test_returns_elapsed_seconds(self) -> None:
        self.assertEqual(ci_audit.seconds(START, START + dt.timedelta(seconds=12.5)), 12.5)


class ParseTimeTests(unittest.TestCase):
    def test_parses_zulu_timestamps(self) -> None:
        parsed = ci_audit.parse_time("2026-01-01T12:00:00Z")
        self.assertEqual(parsed, START)

    def test_none_stays_none(self) -> None:
        self.assertIsNone(ci_audit.parse_time(None))


class SummarizeTests(unittest.TestCase):
    def test_averages_and_ranks_by_queue_plus_run(self) -> None:
        summary = ci_audit.summarize(
            {
                "jobs": {
                    "queued": [
                        {"run": 1, "queue": 300.0, "total": 20.0, "setup": 2.0, "work": 18.0, "steps": []},
                        {"run": 2, "queue": 100.0, "total": 40.0, "setup": 4.0, "work": 36.0, "steps": []},
                    ],
                    "busy": [
                        {"run": 3, "queue": 0.0, "total": 200.0, "setup": 10.0, "work": 190.0, "steps": []},
                    ],
                },
                "steps": {"Run tests": [190.0], "Set up uv": [0.2, 0.4]},
            }
        )
        self.assertEqual([row["job"] for row in summary["jobs"]], ["queued", "busy"])
        queued = summary["jobs"][0]
        self.assertEqual(queued["queue_avg"], 200.0)
        self.assertEqual(queued["total_avg"], 30.0)
        self.assertEqual(queued["total_max"], 40.0)
        self.assertEqual(summary["slowest_steps"][0]["step"], "Run tests")

    def test_ignores_untraced_none_samples_for_setup_and_work_averages(self) -> None:
        summary = ci_audit.summarize(
            {
                "jobs": {
                    "lint": [
                        {"run": 1, "queue": 1.0, "total": 30.0, "setup": 10.0, "work": 20.0, "steps": []},
                        {"run": 2, "queue": 1.0, "total": 30.0, "setup": None, "work": None, "steps": []},
                    ]
                },
                "steps": {},
            }
        )
        lint = summary["jobs"][0]
        self.assertEqual(lint["setup_avg"], 10.0)
        self.assertEqual(lint["work_avg"], 20.0)

    def test_empty_input_is_empty(self) -> None:
        summary = ci_audit.summarize({"jobs": {}, "steps": {}})
        self.assertEqual(summary["jobs"], [])
        self.assertEqual(summary["slowest_steps"], [])


class SetupPatternTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pattern = re.compile(ci_audit.DEFAULT_SETUP_PATTERN, re.IGNORECASE)

    def test_counts_known_setup_steps(self) -> None:
        for name in ("Set up job", "Run actions/checkout@abc", "Install dependencies", "cache restore"):
            with self.subTest(name=name):
                self.assertIsNotNone(self.pattern.search(name.lower()))

    def test_does_not_count_real_work(self) -> None:
        for name in ("Run tests", "Lint", "Build", "Validate"):
            with self.subTest(name=name):
                self.assertIsNone(self.pattern.search(name.lower()))


class GitLabHelpersTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pattern = re.compile(ci_audit.DEFAULT_SETUP_PATTERN, re.IGNORECASE)

    def test_detect_forge_from_remote_and_flags(self) -> None:
        self.assertEqual(
            ci_audit.detect_forge("auto", "https://github.com/owner/repo.git", None, None),
            "github",
        )
        self.assertEqual(
            ci_audit.detect_forge("auto", "ssh://git@gitlab.example.com:2222/group/repo.git", None, None),
            "gitlab",
        )
        self.assertEqual(
            ci_audit.detect_forge("auto", "https://git.internal.example/group/repo.git", "https://git.internal.example", None),
            "gitlab",
        )
        self.assertEqual(
            ci_audit.detect_forge("github", "https://gitlab.example.com/group/repo.git", None, None),
            "github",
        )

    def test_resolve_gitlab_project_formats(self) -> None:
        self.assertEqual(ci_audit.resolve_gitlab_project("90", None), "90")
        self.assertEqual(ci_audit.resolve_gitlab_project("group/sub/repo", None), "group%2Fsub%2Frepo")
        self.assertEqual(
            ci_audit.resolve_gitlab_project(None, "ssh://git@gitlab.example.com:2222/group/sub/repo.git"),
            "group%2Fsub%2Frepo",
        )
        self.assertEqual(
            ci_audit.resolve_gitlab_project(None, "git@gitlab.example.com:group/repo.git"),
            "group%2Frepo",
        )

    def test_split_gitlab_trace_with_iso_timestamps_and_setup_commands(self) -> None:
        trace = "\n".join(
            [
                "2026-01-01T12:00:00Z 00O section_start:100:prepare_executor",
                "2026-01-01T12:00:05Z 00O section_end:105:prepare_executor",
                "2026-01-01T12:00:05Z 00O section_start:105:step_script",
                "2026-01-01T12:00:06Z 01O $ apk add --no-cache shellcheck",
                "2026-01-01T12:00:20Z 01O $ pytest -q",
                "2026-01-01T12:00:50Z 00O section_end:150:step_script",
                "2026-01-01T12:00:50Z 00O section_start:150:upload_artifacts",
                "2026-01-01T12:01:00Z 00O section_end:160:upload_artifacts",
            ]
        )
        setup_s, work_s, steps = ci_audit.split_gitlab_trace(
            trace,
            "2026-01-01T12:00:00Z",
            "2026-01-01T12:01:00Z",
            self.pattern,
        )
        self.assertEqual(work_s, 30.0)
        self.assertEqual(setup_s, 30.0)
        self.assertEqual(steps, [("prepare_executor", 5.0), ("step_script", 45.0), ("upload_artifacts", 10.0)])

    def test_split_gitlab_trace_with_section_epochs_only(self) -> None:
        trace = "\n".join(
            [
                "section_start:100:restore_cache\r\x1b[0KRestoring cache",
                "section_end:115:restore_cache\r\x1b[0K",
                "section_start:115:step_script\r\x1b[0K$ pytest",
                "section_end:155:step_script\r\x1b[0K",
                "section_start:155:upload_cache\r\x1b[0K",
                "section_end:160:upload_cache\r\x1b[0K",
            ]
        )
        setup_s, work_s, _ = ci_audit.split_gitlab_trace(
            trace,
            "2026-01-01T12:00:00Z",
            "2026-01-01T12:01:00Z",
            self.pattern,
        )
        self.assertEqual(work_s, 40.0)
        self.assertEqual(setup_s, 20.0)


class MainTests(unittest.TestCase):
    def test_rejects_non_positive_limit(self) -> None:
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            ci_audit.main(["--limit", "0"])

    def test_rejects_negative_trace_samples(self) -> None:
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            ci_audit.main(["--trace-samples", "-1"])


if __name__ == "__main__":
    unittest.main()
