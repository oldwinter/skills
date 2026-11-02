"""Tests for the CI audit's pure timing and ranking helpers."""

from __future__ import annotations

import datetime as dt
import io
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
    def test_parses_github_zulu_timestamps(self) -> None:
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

    def test_empty_input_is_empty(self) -> None:
        summary = ci_audit.summarize({"jobs": {}, "steps": {}})
        self.assertEqual(summary["jobs"], [])
        self.assertEqual(summary["slowest_steps"], [])


class SetupPatternTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pattern = ci_audit.re.compile(ci_audit.DEFAULT_SETUP_PATTERN, ci_audit.re.IGNORECASE)

    def test_counts_known_setup_steps(self) -> None:
        for name in ("Set up job", "Run actions/checkout@abc", "Install dependencies", "cache restore"):
            with self.subTest(name=name):
                self.assertIsNotNone(self.pattern.search(name.lower()))

    def test_does_not_count_real_work(self) -> None:
        for name in ("Run tests", "Lint", "Build", "Validate"):
            with self.subTest(name=name):
                self.assertIsNone(self.pattern.search(name.lower()))


class MainTests(unittest.TestCase):
    def test_rejects_non_positive_limit(self) -> None:
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            ci_audit.main(["--limit", "0"])


if __name__ == "__main__":
    unittest.main()
