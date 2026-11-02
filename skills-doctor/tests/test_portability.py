from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from skills_doctor.catalog import CatalogError, discover_skills, load_catalog, tool_mentions
from skills_doctor.cli import diagnose, main, markdown, requirement_status
from skills_doctor.probes import MAX_OUTPUT, Probes, run_command
from test_probes import Recorder, fixture, options


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.data = fixture(self.root)
        self.path = self.root / ".skills-doctor.json"

    def load(self):
        self.path.write_text(json.dumps(self.data), encoding="utf-8")
        return load_catalog(self.root, self.path, discover_skills(self.root))

    def test_valid_declaration(self):
        self.assertEqual(self.load(), self.data)

    def test_undeclared_new_skill_fails_coverage(self):
        entry = self.root / ".claude/skills/new/SKILL.md"
        entry.parent.mkdir()
        entry.write_text("New", encoding="utf-8")
        with self.assertRaisesRegex(CatalogError, "missing=.*new"):
            self.load()

    def test_invalid_declarations_fail_closed(self):
        original = copy.deepcopy(self.data)
        mutations = [
            lambda d: d.update(version=True),
            lambda d: d["capabilities"]["lark"].update(command="echo unsafe"),
            lambda d: d["capabilities"]["lark"].update(probe="run-shell"),
            lambda d: d["capabilities"]["lark"].update(tools=["python3;echo"]),
            lambda d: d["skills"]["example"].update(profiles={"empty": []}),
            lambda d: d["skills"]["example"].update(profiles={"bad": [["unknown"]]}),
            lambda d: d["skills"]["example"].update(profiles={"bad": [[]]}),
            lambda d: d["skills"]["example"]["sources"].append("../outside"),
            lambda d: d["skills"]["example"].update(sources=[]),
            lambda d: d["skills"].update(removed=d["skills"]["example"]),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.data = copy.deepcopy(original)
                mutate(self.data)
                with self.assertRaises(CatalogError):
                    self.load()

    def test_discovery_stays_within_target(self):
        with tempfile.TemporaryDirectory() as other:
            with self.assertRaises(CatalogError):
                discover_skills(self.root, [other])
            with self.assertRaises(CatalogError):
                load_catalog(self.root, Path(other) / "catalog.json", discover_skills(self.root))

    def test_evidence_symlink_cannot_escape_checkout(self):
        with tempfile.TemporaryDirectory() as other:
            external = Path(other) / "evidence.md"
            external.write_text("Outside", encoding="utf-8")
            link = self.root / "external.md"
            try:
                link.symlink_to(external)
            except OSError:
                self.skipTest("Symlinks unavailable for this operator")
            self.data["skills"]["example"]["sources"].append("external.md")
            with self.assertRaises(CatalogError):
                self.load()

    def test_nested_library_and_duplicate_ids(self):
        entry = self.root / "nested/other/SKILL.md"
        entry.parent.mkdir(parents=True)
        entry.write_text("Other", encoding="utf-8")
        self.assertEqual(set(discover_skills(self.root, ["."])), {"example", "other"})
        duplicate = self.root / "another/example/SKILL.md"
        duplicate.parent.mkdir(parents=True)
        duplicate.write_text("Duplicate", encoding="utf-8")
        with self.assertRaisesRegex(CatalogError, "Duplicate"):
            discover_skills(self.root, ["."])
        self.assertEqual(set(discover_skills(self.root)), {"example"})

    def test_empty_scope_is_not_ready(self):
        empty = self.root / "empty"
        empty.mkdir()
        with self.assertRaisesRegex(CatalogError, "No skills"):
            discover_skills(self.root, ["empty"])

    def test_tool_hints_do_not_confuse_hyphenated_hosts_with_node(self):
        folder = self.root / ".claude/skills/example"
        (folder / "SKILL.md").write_text("Read `worker-node` with `ssh`.", encoding="utf-8")
        self.assertEqual(set(tool_mentions(self.root, folder, {"node", "ssh"})), {"ssh"})

    def test_public_example_is_valid_for_its_fictional_target(self):
        data = json.loads((SKILL / "references/catalog.example.json").read_text(encoding="utf-8"))
        self.data = data
        self.assertEqual(self.load(), data)

    def test_catalog_cannot_read_env_file_as_evidence(self):
        (self.root / ".env").write_text("FIXTURE_SENSITIVE_MARKER", encoding="utf-8")
        self.data["skills"]["example"]["sources"].append(".env")
        with self.assertRaisesRegex(CatalogError, "Markdown documentation"):
            self.load()


class DiagnosisTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.catalog = fixture(self.root)

    def test_offline_scan_never_executes(self):
        args = options("--all")
        recorder = Recorder()
        report = diagnose(self.root, self.catalog, args, Probes(self.root, args, recorder), which=lambda _: "/fake")
        self.assertEqual(recorder.calls, [])
        self.assertEqual(report["summary"]["unverified"], 1)

    def test_missing_required_tool_blocks(self):
        report = diagnose(self.root, self.catalog, options(), which=lambda _: None)
        self.assertEqual(report["summary"]["blocked"], 1)
        self.assertIn("lark-cli (MISSING)", markdown(report))

    def test_or_and_runtime_semantics(self):
        def cap(status, runtime=None):
            return {"access": {"status": status}, "runtime_requirements": runtime or []}
        for checks, expected in [
            ([cap("denied"), cap("unverified")], "unverified"),
            ([cap("missing"), cap("denied")], "blocked"),
            ([cap("denied"), cap("verified")], "verified"),
            ([cap("verified", ["Browser runtime required"])], "unverified"),
        ]:
            self.assertEqual(requirement_status(checks), expected)

    def test_multi_profile_requires_selection(self):
        self.catalog["skills"]["example"]["profiles"]["alternate"] = ["lark"]
        with self.assertRaisesRegex(CatalogError, "needs --profile"):
            diagnose(self.root, self.catalog, options("--skill", "example"))

    def invoke(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
            code = main(["--repo-root", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_no_catalog_inventory_never_claims_missing_hint_is_required(self):
        with patch("skills_doctor.probes.subprocess.run", side_effect=AssertionError("Must not execute")):
            code, stdout, _ = self.invoke("--all", "--format", "json")
        report = json.loads(stdout)
        self.assertEqual(code, 3)
        self.assertEqual(report["catalog_mode"], "unreviewed-inventory")
        self.assertEqual(report["summary"]["unverified"], 1)
        self.assertIn("lark-cli", report["results"][0]["tool_mentions"])

    def test_catalog_validation_and_unknown_skill(self):
        path = self.root / ".skills-doctor.json"
        path.write_text(json.dumps(self.catalog), encoding="utf-8")
        self.assertEqual(self.invoke("--catalog", path.name, "--validate-catalog")[0], 0)
        self.assertEqual(self.invoke("--skill", "missing")[0], 2)

    def test_live_without_reviewed_catalog_or_explicit_scope_is_rejected(self):
        for args in [
            ("--skill", "example", "--live", "github"),
            ("--all", "--catalog", ".skills-doctor.json", "--live", "github"),
            ("--validate-catalog",),
            ("--timeout", "0"),
            ("--gitlab-host", "https://example.invalid"),
        ]:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    main(list(args))
                self.assertEqual(error.exception.code, 2)


class ProcessTests(unittest.TestCase):
    def test_real_process_success_failure_timeout_and_output_limit(self):
        env = dict(os.environ)
        result = run_command([sys.executable, "-c", "print('fixture')"], SKILL, 2, env)
        self.assertEqual((result.code, result.stdout.strip()), (0, "fixture"))
        missing = run_command(["nonexistent-skills-doctor-fixture"], SKILL, 1, env)
        self.assertEqual(missing.failure, "cannot-execute")
        slow = run_command([sys.executable, "-c", "import time; time.sleep(5)"], SKILL, 1, env)
        self.assertEqual(slow.failure, "timeout")
        large = run_command([sys.executable, "-c", f"print('x' * {MAX_OUTPUT + 1})"], SKILL, 2, env)
        self.assertEqual(large.failure, "output-limit")
        self.assertEqual(large.stdout, "")

    def test_detached_install_runs_from_another_checkout_without_source_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            installed = base / "installed/skills-doctor"
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
            target = base / "target"
            target.mkdir()
            fixture(target)
            result = subprocess.run(
                [sys.executable, str(installed / "scripts/doctor.py"), "--all", "--format", "json"],
                cwd=target, env=dict(os.environ, PYTHONPATH=""), capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 3, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["summary"]["skills"], 1)
            self.assertEqual(report["results"][0]["skill"], "example")

    def test_no_credentials_or_env_file_needed(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            fixture(target)
            (target / ".env").write_text("FIXTURE_SENSITIVE_MARKER", encoding="utf-8")
            env = {key: value for key, value in os.environ.items()
                   if not key.startswith(("AWS_", "GH_", "GITHUB_", "GITLAB_", "LARK"))}
            env["PYTHONPATH"] = ""
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts/doctor.py"), "--repo-root", str(target), "--format", "json"],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertNotIn("FIXTURE_SENSITIVE_MARKER", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
