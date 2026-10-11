"""End-to-end tests for scripts/autoresearch.py against throwaway git repositories.

Run: python3 -m unittest discover -s agent-autoresearch/tests -v
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "autoresearch.py"
SPEC = importlib.util.spec_from_file_location("autoresearch", SCRIPT)
autoresearch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(autoresearch)

MEASURE = """\
import pathlib, sys, time
words = pathlib.Path("src/value.txt").read_text().split()
head = words[0]
if head == "crash":
    sys.exit(1)
if head == "hang":
    time.sleep(30)
if head == "dirty":
    pathlib.Path("src/generated.txt").write_text("side effect")
    head = "5"
value = float(head)
print("warming up")
print(f"METRIC score={value}")
print(f"METRIC aux={value * 2}")
"""

CHECKS = """\
import pathlib, sys
sys.exit(1 if "bad" in pathlib.Path("src/value.txt").read_text() else 0)
"""

FAKE_AGENT = """\
import pathlib, subprocess, sys
sys.stdin.read()
repo = pathlib.Path.cwd()
value = repo / "src" / "value.txt"
current = float(value.read_text().split()[0])
value.write_text(f"{current - 1:g}\\n")
if "--no-trial" not in sys.argv:
    subprocess.run([str(repo / ".autoresearch" / "ar"), "trial", "--description", f"decrement to {current - 1:g}"], check=True)
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


class ControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "src").mkdir(parents=True)
        (self.repo / "bench").mkdir()
        (self.repo / "src" / "value.txt").write_text("10\n")
        (self.repo / "bench" / "measure.py").write_text(MEASURE)
        (self.repo / "bench" / "checks.py").write_text(CHECKS)
        (self.repo / "agent.py").write_text(FAKE_AGENT)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "start")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def ar(self, *args: str, expect: int = 0) -> str:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo), *args],
            capture_output=True,
            text=True,
        )
        output = proc.stdout + proc.stderr
        self.assertEqual(proc.returncode, expect, output)
        return output

    def init(self, *extra: str) -> str:
        return self.ar(
            "init",
            "--goal", "lower the score",
            "--metric", "score",
            "--direction", "lower",
            "--measure", f"{sys.executable} bench/measure.py",
            "--scope", "src",
            "--protect", "bench",
            "--runs", "1",
            *extra,
        )

    def write(self, text: str, name: str = "src/value.txt") -> None:
        (self.repo / name).write_text(text)

    def status(self) -> dict:
        return json.loads(self.ar("status", "--json"))

    def entries(self) -> list:
        log = self.repo / ".autoresearch" / "log.jsonl"
        return [json.loads(line) for line in log.read_text().splitlines()]

    def test_init_creates_branch_baseline_and_launcher(self) -> None:
        out = self.init()
        self.assertIn("Baseline score = 10", out)
        self.assertTrue(git(self.repo, "branch", "--show-current").startswith("autoresearch/score-"))
        launcher = self.repo / ".autoresearch" / "ar"
        self.assertTrue(os.access(launcher, os.X_OK))
        exclude = Path(git(self.repo, "rev-parse", "--git-path", "info/exclude"))
        exclude = exclude if exclude.is_absolute() else self.repo / exclude
        self.assertIn("/.autoresearch/", exclude.read_text())
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        state = self.status()
        self.assertEqual(state["state"], "active")
        self.assertEqual(state["baseline"], 10.0)
        launched = subprocess.run([str(launcher), "status", "--json"], capture_output=True, text=True, cwd="/")
        self.assertEqual(json.loads(launched.stdout)["best"], 10.0)

    def test_init_rejects_dirty_tree_and_existing_session(self) -> None:
        self.write("9\n")
        self.assertIn("uncommitted changes", self.init_expect_error())
        git(self.repo, "checkout", "--", ".")
        self.init()
        self.assertIn("already exists", self.init_expect_error())

    def init_expect_error(self) -> str:
        return self.ar(
            "init", "--goal", "g", "--metric", "score", "--direction", "lower",
            "--measure", f"{sys.executable} bench/measure.py", expect=2,
        )

    def test_keep_commits_one_change_and_advances_best(self) -> None:
        self.init()
        base = git(self.repo, "rev-parse", "HEAD")
        self.write("8\n")
        out = self.ar("trial", "--description", "smaller value", "--hypothesis", "lower is better")
        self.assertIn("#1 KEEP", out)
        self.assertEqual(git(self.repo, "rev-parse", "HEAD~1"), base)
        message = git(self.repo, "log", "-1", "--format=%B")
        self.assertIn("autoresearch #1: smaller value", message)
        self.assertIn('"score": 8.0', message)
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        state = self.status()
        self.assertEqual(state["best"], 8.0)
        self.assertEqual(state["counts"]["keep"], 1)

    def test_discard_reverts_tree_and_keeps_patch(self) -> None:
        self.init()
        self.write("12\n")
        self.write("scratch", "src/new_file.txt")
        out = self.ar("trial", "--description", "bigger value")
        self.assertIn("#1 DISCARD", out)
        self.assertEqual((self.repo / "src" / "value.txt").read_text(), "10\n")
        self.assertFalse((self.repo / "src" / "new_file.txt").exists())
        patch = (self.repo / ".autoresearch" / "patches" / "0001.patch").read_text()
        self.assertIn("+12", patch)
        self.assertIn("new_file.txt", patch)
        self.ar("restore", "1")
        self.assertEqual((self.repo / "src" / "value.txt").read_text(), "12\n")
        self.assertTrue((self.repo / "src" / "new_file.txt").exists())

    def test_crash_and_timeout_are_reverted(self) -> None:
        self.init("--timeout", "2")
        self.write("crash\n")
        out = self.ar("trial", "--description", "breaks the build")
        self.assertIn("#1 CRASH", out)
        self.assertIn("measure exited 1", out)
        self.write("hang\n")
        out = self.ar("trial", "--description", "never finishes")
        self.assertIn("#2 TIMEOUT", out)
        self.assertEqual((self.repo / "src" / "value.txt").read_text(), "10\n")

    def test_checks_gate_blocks_keep(self) -> None:
        self.init("--checks", f"{sys.executable} bench/checks.py")
        self.write("8 bad\n")
        out = self.ar("trial", "--description", "faster but wrong")
        self.assertIn("#1 CHECKS_FAILED", out)
        self.assertEqual(self.status()["best"], 10.0)
        self.write("8\n")
        self.assertIn("#2 KEEP", self.ar("trial", "--description", "faster and right"))

    def test_scope_and_protected_paths_are_enforced(self) -> None:
        self.init()
        self.write("print('METRIC score=0')\n", "bench/measure.py")
        out = self.ar("trial", "--description", "game the benchmark", expect=2)
        self.assertIn("protected: bench/measure.py", out)
        self.assertIn("score=0", (self.repo / "bench" / "measure.py").read_text())
        git(self.repo, "checkout", "--", "bench/measure.py")
        self.write("x", "README.md")
        out = self.ar("trial", "--description", "outside", expect=2)
        self.assertIn("outside the scope", out)

    def test_manual_commits_fold_into_one_trial(self) -> None:
        self.init()
        base = git(self.repo, "rev-parse", "HEAD")
        self.write("9\n")
        git(self.repo, "commit", "-qam", "agent commit one")
        self.write("7\n")
        git(self.repo, "commit", "-qam", "agent commit two")
        out = self.ar("trial", "--description", "two steps")
        self.assertIn("2 manual commit(s) folded in", out)
        self.assertEqual(git(self.repo, "rev-parse", "HEAD~1"), base)

    def test_iteration_limit_stops_and_resume_extends(self) -> None:
        self.init("--max-iterations", "1")
        self.write("9\n")
        out = self.ar("trial", "--description", "one")
        self.assertIn("next: STOP", out)
        self.write("8\n")
        out = self.ar("trial", "--description", "two", expect=3)
        self.assertIn("session is stopped", out)
        self.ar("resume", "--more", "1")
        self.assertIn("#2 KEEP", self.ar("trial", "--description", "two"))

    def test_target_completes_session(self) -> None:
        self.init("--target", "9")
        self.write("8\n")
        out = self.ar("trial", "--description", "hit it")
        self.assertIn("session is complete", out)
        self.assertEqual(self.status()["state"], "complete")
        out = self.ar("resume")
        self.assertIn("still complete", out)

    def test_simplification_keeps_equal_metric(self) -> None:
        self.init()
        self.write("10 \n")
        self.assertIn("#1 DISCARD", self.ar("trial", "--description", "same value"))
        self.write("10 \n")
        out = self.ar("trial", "--description", "same value, simpler", "--simplification")
        self.assertIn("#2 KEEP", out)
        self.assertIn("simplification", out)

    def test_measure_side_effects_count_as_crash(self) -> None:
        self.init()
        self.write("dirty\n")
        out = self.ar("trial", "--description", "measure writes files")
        self.assertIn("#1 CRASH", out)
        self.assertIn("side-effect free", out)
        self.assertFalse((self.repo / "src" / "generated.txt").exists())

    def test_noise_threshold_requires_real_gain(self) -> None:
        self.init("--min-delta", "1.5")
        self.write("9\n")
        self.assertIn("#1 DISCARD", self.ar("trial", "--description", "within noise"))
        self.write("8\n")
        self.assertIn("#2 KEEP", self.ar("trial", "--description", "beyond noise"))

    def test_undo_recheck_note_log_and_report(self) -> None:
        self.init()
        self.write("8\n")
        self.ar("trial", "--description", "keep me")
        self.ar("note", "smaller numbers win")
        self.write("7\n")
        self.ar("trial", "--description", "keep me too")
        out = self.ar("undo", "--reason", "too hacky")
        self.assertIn("undid keep", out)
        self.assertEqual((self.repo / "src" / "value.txt").read_text(), "8\n")
        self.assertEqual(self.status()["best"], 8.0)
        self.assertIn("recheck score", self.ar("recheck", "--runs", "3"))
        tsv = self.ar("log", "--tsv").splitlines()
        self.assertEqual(tsv[0].split("\t")[:4], ["run", "commit", "score", "status"])
        self.assertIn("note: smaller numbers win", self.ar("status"))
        self.ar("report")
        report = (self.repo / ".autoresearch" / "report.html").read_text()
        self.assertIn("<svg", report)
        summary = (self.repo / ".autoresearch" / "summary.md").read_text()
        self.assertIn("keep me", summary)
        self.assertNotIn("| 2 |", summary)

    def test_detached_trial_and_wait(self) -> None:
        self.init()
        self.write("6\n")
        self.assertIn("background", self.ar("trial", "--description", "detached", "--detach"))
        out = self.ar("wait", "--timeout", "60")
        self.assertIn("#1 KEEP", out)

    def test_hooks_output_reaches_agent(self) -> None:
        self.init()
        hook = self.repo / ".autoresearch" / "hooks" / "after.sh"
        hook.parent.mkdir()
        hook.write_text("#!/bin/sh\npython3 -c 'import json,sys; print(\"saw\", json.load(sys.stdin)[\"run_entry\"][\"status\"])'\n")
        hook.chmod(0o755)
        self.write("8\n")
        self.assertIn("hook after: saw keep", self.ar("trial", "--description", "with hook"))

    def test_relay_drives_workers_and_evaluates_leftovers(self) -> None:
        self.init("--max-iterations", "3")
        out = self.ar("relay", "--agent-cmd", f"{sys.executable} agent.py", "--max-workers", "2", "--trials-per-worker", "1")
        self.assertIn("relay: worker 2", out)
        self.assertEqual(self.status()["best"], 8.0)
        out = self.ar("relay", "--agent-cmd", f"{sys.executable} agent.py --no-trial", "--max-workers", "1")
        self.assertIn("left unevaluated changes", out)
        state = self.status()
        self.assertEqual(state["best"], 7.0)
        self.assertEqual(state["state"], "stopped")
        prompt = (self.repo / ".autoresearch" / "relay" / "worker-001.prompt.md").read_text()
        self.assertIn("trial --description", prompt)

    def test_noise_probe_reports_spread(self) -> None:
        out = self.ar(
            "init", "--goal", "g", "--metric", "score", "--direction", "lower",
            "--measure", f"{sys.executable} bench/measure.py", "--scope", "src",
        )
        self.assertIn("Noise: 3 runs", out)


class ParseMetricsTest(unittest.TestCase):
    def test_metric_lines_win(self) -> None:
        out = "noise\nMETRIC total_ms=12.5\nMETRIC µs=3\n42\n"
        self.assertEqual(autoresearch.parse_metrics(out, "", "total_ms"), {"total_ms": 12.5, "µs": 3.0})

    def test_final_number_and_json_fallbacks(self) -> None:
        self.assertEqual(autoresearch.parse_metrics("log\n0.997\n", "", "val_bpb"), {"val_bpb": 0.997})
        parsed = autoresearch.parse_metrics('{"errors": 3, "ok": true, "name": "x"}\n', "", "errors")
        self.assertEqual(parsed, {"errors": 3.0})

    def test_rejects_non_finite_and_missing(self) -> None:
        self.assertEqual(autoresearch.parse_metrics("METRIC x=nan\n", "", "x"), {})
        self.assertEqual(autoresearch.parse_metrics("done\n", "", "x"), {})

    def test_decide_respects_direction_and_threshold(self) -> None:
        config = {"metric": {"direction": "higher"}, "min_delta": 0.5}
        self.assertEqual(autoresearch.decide(11.0, 10.0, config, False), "improved")
        self.assertEqual(autoresearch.decide(10.4, 10.0, config, False), "worse")
        self.assertEqual(autoresearch.decide(9.8, 10.0, config, True), "simplification")


if __name__ == "__main__":
    unittest.main()
