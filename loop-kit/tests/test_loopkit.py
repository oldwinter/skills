#!/usr/bin/env python3
"""Tests for loopkit.py: init, doctor, status, config and the tick lock.

Standard library only, no network, no ``gh``. Each test builds a throwaway git
repository with a fake origin remote and a state directory inside the temp tree.
"""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import lockfile  # noqa: E402
import loopkit  # noqa: E402

import desk  # noqa: E402


def run_loopkit(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = loopkit.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def run_desk_for(state_dir: Path, *argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = desk.main(["--state", str(state_dir / "desk"), *argv])
    return code, out.getvalue(), err.getvalue()


def fake_gh(authenticated: bool = True):
    """A stand-in for the one ``gh`` runner the doctor uses."""

    def runner(args: list[str], timeout: int = 30) -> tuple[int, str, str]:
        if args[:1] == ["--version"]:
            return 0, "gh version 9.9.9 (fake)\n", ""
        if args[:2] == ["auth", "status"]:
            if authenticated:
                return 0, "github.com\n  Logged in to github.com account octocat (keyring)\n", ""
            return 1, "", "not logged in\n"
        return 1, "", f"unexpected gh {' '.join(args)}\n"

    return runner


NESTED_SKILLS = (".claude", "skills")


def make_sibling_skills(suite_root: Path) -> None:
    """Install the three tick skills a doctor run expects to find next to loop-kit."""
    for name in ("loop-triage-github", "loop-watch-social", "loop-nightly-review"):
        directory = suite_root / name
        (directory / "scripts").mkdir(parents=True, exist_ok=True)
        (directory / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
    watcher = suite_root / "loop-triage-github" / "scripts" / "watch-prs.py"
    watcher.write_text("#!/usr/bin/env python3\n", encoding="utf-8")


class LoopKitTestCase(unittest.TestCase):
    """The installed layout: the four skills live in <repo>/.claude/skills/.

    That is how a target project really gets the suite, and it is the layout
    where the suite root (the loop-kit skill's parent) is *not* the repository
    root. The skills-library layout is covered separately.
    """

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name).resolve()
        self.repo = self.root / "myapp"
        self.repo.mkdir()
        self.suite_root = self.repo.joinpath(*NESTED_SKILLS)
        self.suite_root.mkdir(parents=True)
        self.state = self.root / "state"
        self._real_run_gh = loopkit.run_gh
        loopkit.run_gh = fake_gh()
        self.addCleanup(self._restore_gh)
        self.git("init", "-q")
        self.git("remote", "add", "origin", "https://github.com/owner/myapp.git")
        make_sibling_skills(self.suite_root)

    def _restore_gh(self) -> None:
        loopkit.run_gh = self._real_run_gh

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args], cwd=str(self.repo), capture_output=True, text=True, timeout=60
        )

    def init(self, *extra: str) -> tuple[int, str, str]:
        return run_loopkit(
            "--repo-root", str(self.repo),
            "init", "--state-dir", str(self.state),
            "--suite-root", str(self.suite_root),
            *extra,
        )

    def doctor(self, *extra: str) -> tuple[int, str, str]:
        return run_loopkit(
            "--repo-root", str(self.repo), "doctor", "--suite-root", str(self.suite_root), *extra
        )

    def read_config(self) -> dict:
        return json.loads((self.repo / ".loop" / "config.json").read_text(encoding="utf-8"))


class InitTests(LoopKitTestCase):
    def test_init_creates_config_state_templates_and_block(self) -> None:
        code, out, err = self.init()
        self.assertEqual(code, 0, err)

        config = self.read_config()
        self.assertEqual(config["version"], 1)
        self.assertEqual(config["repo"], "owner/myapp")
        self.assertEqual(config["project"], "myapp")
        self.assertEqual(config["stateDir"], str(self.state))
        self.assertEqual(config["lessonsPath"], "LESSONS.md")
        self.assertEqual(config["rulesPath"], ".agents/rules/acceptance.md")
        self.assertEqual(config["agentsPath"], "AGENTS.md")
        self.assertEqual(config["desk"], {"kind": "files"})
        self.assertEqual(config["trustedLogins"], ["coderabbitai[bot]"])
        self.assertEqual(config["windowDays"], 3)
        self.assertEqual(config["loops"]["triage-github"], {"interval": "30m", "enabled": True})
        self.assertEqual(
            config["loops"]["watch-social"],
            {"interval": "60m", "enabled": False, "sources": ["x", "discord", "reddit"]},
        )
        self.assertEqual(config["loops"]["nightly-review"], {"interval": "24h", "enabled": True})

        lessons = self.repo / "LESSONS.md"
        rules = self.repo / ".agents" / "rules" / "acceptance.md"
        self.assertTrue(lessons.is_file())
        self.assertTrue(rules.is_file())
        self.assertIn("Lessons from merged work", lessons.read_text(encoding="utf-8"))
        self.assertIn("Acceptance criteria", rules.read_text(encoding="utf-8"))
        self.assertIn("## Moved from LESSONS.md", rules.read_text(encoding="utf-8"))

        agents = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("<!-- loop-kit:begin -->", agents)
        self.assertIn("<!-- loop-kit:end -->", agents)
        self.assertIn("loop-triage-github", agents)
        self.assertIn("LESSONS.md", agents)

        self.assertTrue((self.state / "desk").is_dir())
        self.assertTrue((self.state / "desk" / "archive").is_dir())
        self.assertEqual(json.loads((self.state / "github.json").read_text()), {"since": None})
        self.assertEqual(
            json.loads((self.state / "social.json").read_text()),
            {"seen": {"x": [], "discord": {}, "reddit": []}, "pending": []},
        )
        self.assertEqual(json.loads((self.state / "watch.json").read_text()), [])

        self.assertIn("config   ", out)
        self.assertIn("template ", out)

    def test_init_prints_doctor_rows_and_next_steps(self) -> None:
        shutil.rmtree(self.suite_root / "loop-triage-github")
        shutil.rmtree(self.suite_root / "loop-watch-social")
        shutil.rmtree(self.suite_root / "loop-nightly-review")
        code, out, _ = self.init()
        self.assertEqual(code, 0)
        self.assertIn("PASS config", out)
        self.assertIn("PASS repo", out)
        self.assertIn("PASS state dir", out)
        self.assertIn("PASS lessons file", out)
        self.assertIn("PASS rules file", out)
        self.assertIn("PASS AGENTS.md block", out)
        self.assertIn("FAIL skill triage-github", out)
        self.assertIn("4-59/5 * * * *", out)
        self.assertIn("*/30 * * * *", out)
        self.assertIn("0 3 * * *", out)
        self.assertIn(
            "npx --yes skills@latest add oldwinter/skills --skill loop-kit "
            "loop-triage-github loop-watch-social loop-nightly-review",
            out,
        )
        self.assertIn("<kit-dir>/references/harnesses.md", out)

    def test_init_says_all_skills_are_installed_when_they_are(self) -> None:
        code, out, _ = self.init()
        self.assertEqual(code, 0)
        self.assertIn("All three tick skills are installed next to loop-kit.", out)
        self.assertNotIn("npx --yes skills@latest", out)

    def test_init_is_idempotent_and_preserves_unknown_keys(self) -> None:
        self.init()
        config = self.read_config()
        config["myOwnKey"] = {"kept": True}
        config["loops"]["triage-github"]["enabled"] = False
        (self.repo / ".loop" / "config.json").write_text(json.dumps(config), encoding="utf-8")

        lessons = self.repo / "LESSONS.md"
        hand_edited = lessons.read_text(encoding="utf-8") + "\n**Hand-written lesson.**\n- Seen 1x.\n"
        lessons.write_text(hand_edited, encoding="utf-8")
        rules_before = (self.repo / ".agents" / "rules" / "acceptance.md").read_text(encoding="utf-8")
        agents_before = (self.repo / "AGENTS.md").read_text(encoding="utf-8")

        code, out, err = self.init()
        self.assertEqual(code, 0, err)

        after = self.read_config()
        self.assertEqual(after["myOwnKey"], {"kept": True})
        self.assertFalse(after["loops"]["triage-github"]["enabled"])
        self.assertEqual(lessons.read_text(encoding="utf-8"), hand_edited)
        self.assertIn("kept     ", out)
        self.assertEqual(
            (self.repo / ".agents" / "rules" / "acceptance.md").read_text(encoding="utf-8"),
            rules_before,
        )
        self.assertEqual((self.repo / "AGENTS.md").read_text(encoding="utf-8"), agents_before)

    def test_init_keeps_one_agents_block_when_it_already_exists(self) -> None:
        self.init()
        first = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.init()
        second = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(first, second)
        self.assertEqual(second.count("<!-- loop-kit:begin -->"), 1)

    def test_init_appends_the_block_to_an_existing_agents_file(self) -> None:
        (self.repo / "AGENTS.md").write_text("# House rules\n\nBe careful.\n", encoding="utf-8")
        self.init()
        text = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# House rules"))
        self.assertIn("Be careful.", text)
        self.assertEqual(text.count("<!-- loop-kit:begin -->"), 1)

    def test_init_respects_path_overrides(self) -> None:
        code, _, err = self.init(
            "--repo", "someone/other",
            "--project", "other",
            "--lessons", "docs/LESSONS.md",
            "--rules", "docs/acceptance.md",
            "--agents", "CLAUDE.md",
            "--default-branch", "trunk",
        )
        self.assertEqual(code, 0, err)
        config = self.read_config()
        self.assertEqual(config["repo"], "someone/other")
        self.assertEqual(config["project"], "other")
        self.assertEqual(config["defaultBranch"], "trunk")
        self.assertTrue((self.repo / "docs" / "LESSONS.md").is_file())
        self.assertTrue((self.repo / "docs" / "acceptance.md").is_file())
        self.assertTrue((self.repo / "CLAUDE.md").is_file())

    def test_init_refuses_an_unparsable_config_without_force(self) -> None:
        (self.repo / ".loop").mkdir()
        (self.repo / ".loop" / "config.json").write_text("{not json", encoding="utf-8")
        code, _, err = self.init()
        self.assertEqual(code, 2)
        self.assertIn("not valid JSON", err)
        code, _, err = self.init("--force")
        self.assertEqual(code, 0, err)


class DoctorTests(LoopKitTestCase):
    def test_doctor_passes_after_init_and_fails_without_config(self) -> None:
        self.init()
        code, out, _ = self.doctor()
        self.assertEqual(code, 0, out)
        self.assertIn("PASS config", out)
        self.assertIn("PASS gh", out)
        self.assertIn("PASS gh auth", out)
        self.assertIn("logged in as octocat", out)
        self.assertIn("doctor: no FAIL rows.", out)
        self.assertIn("PASS watcher", out)

        (self.repo / ".loop" / "config.json").unlink()
        code, out, _ = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("FAIL config", out)
        self.assertIn("FAIL lessons file", out)
        self.assertIn("FAIL rules file", out)
        self.assertIn("SKIP state dir", out)

    def test_doctor_fails_when_gh_is_not_authenticated(self) -> None:
        self.init()
        loopkit.run_gh = fake_gh(authenticated=False)
        code, out, _ = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("FAIL gh auth", out)
        self.assertIn("gh auth login", out)

    def test_doctor_skips_gh_when_the_github_loop_is_disabled(self) -> None:
        self.init()
        loopkit.run_gh = fake_gh(authenticated=False)
        config = self.read_config()
        config["loops"]["triage-github"]["enabled"] = False
        (self.repo / ".loop" / "config.json").write_text(json.dumps(config), encoding="utf-8")
        code, out, _ = self.doctor()
        self.assertEqual(code, 0, out)
        self.assertIn("WARN gh auth", out)
        self.assertIn("SKIP watcher", out)
        self.assertNotIn("FAIL gh auth", out)

    def test_doctor_does_not_clobber_the_rendered_page(self) -> None:
        self.init()
        desk = self.state / "desk"
        (desk / "1.json").write_text(
            json.dumps({"id": "1", "kind": "issue", "status": "pending", "draft": "keep me"}), encoding="utf-8"
        )
        code, _, err = run_desk_for(self.state, "render")
        self.assertEqual(code, 0, err)
        rendered = (desk / "index.html").read_text(encoding="utf-8")
        self.assertIn("keep me", rendered)

        self.doctor()
        self.assertEqual((desk / "index.html").read_text(encoding="utf-8"), rendered)
        leftovers = [path.name for path in desk.iterdir() if "probe" in path.name]
        self.assertEqual(leftovers, [])

    def test_doctor_json_reports_every_check(self) -> None:
        self.init()
        code, out, _ = self.doctor("--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["exit"], 0)
        names = {check["name"] for check in payload["checks"]}
        for expected in ("python", "gh", "gh auth", "config", "repo", "state dir", "desk renders"):
            self.assertIn(expected, names)
        for check in payload["checks"]:
            self.assertIn(check["status"], {"PASS", "WARN", "FAIL", "SKIP"})

    def test_doctor_warns_when_the_config_repo_disagrees_with_origin(self) -> None:
        self.init("--repo", "someone/else")
        code, out, _ = self.doctor()
        self.assertEqual(code, 0)
        self.assertIn("WARN repo", out)

    def test_doctor_fails_when_an_enabled_skill_directory_is_missing(self) -> None:
        self.init()
        code, out, _ = self.doctor()
        self.assertEqual(code, 0, out)
        self.assertIn("PASS skill triage-github", out)
        self.assertIn("PASS skill nightly-review", out)
        self.assertIn("PASS watcher", out)

        shutil.rmtree(self.suite_root / "loop-triage-github")
        code, out, _ = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("FAIL skill triage-github", out)
        self.assertIn("FAIL watcher", out)
        self.assertIn("npx --yes skills@latest add oldwinter/skills --skill loop-kit loop-triage-github", out)

    def test_doctor_finds_the_siblings_in_a_nested_skills_directory(self) -> None:
        """The installed layout: <repo>/.claude/skills/<skill>. Not the repo root."""
        self.assertEqual(self.suite_root, self.repo / ".claude" / "skills")
        code, out, err = self.init()
        self.assertEqual(code, 0, err)
        code, out, _ = self.doctor()
        self.assertEqual(code, 0, out)
        # Only enabled loops are checked; watch-social ships disabled by default.
        for name in ("triage-github", "nightly-review"):
            self.assertIn(f"PASS skill {name}", out)
            self.assertIn(str(self.suite_root / f"loop-{name}"), out)
        self.assertTrue((self.suite_root / "loop-watch-social" / "SKILL.md").is_file())
        self.assertIn("PASS watcher", out)
        self.assertIn(str(self.suite_root / "loop-triage-github" / "scripts" / "watch-prs.py"), out)
        # The repository root holds no skill directories at all in this layout.
        self.assertFalse((self.repo / "loop-triage-github").exists())

    def test_init_in_a_nested_layout_says_the_siblings_are_installed(self) -> None:
        code, out, err = self.init()
        self.assertEqual(code, 0, err)
        self.assertIn("All three tick skills are installed next to loop-kit.", out)
        self.assertNotIn("npx --yes skills@latest", out)

    def test_doctor_json_reports_the_nested_suite_root_paths(self) -> None:
        self.init()
        code, out, _ = self.doctor("--json")
        self.assertEqual(code, 0)
        checks = {check["name"]: check for check in json.loads(out)["checks"]}
        self.assertEqual(checks["skill triage-github"]["status"], "PASS")
        self.assertEqual(checks["skill triage-github"]["detail"], str(self.suite_root / "loop-triage-github"))
        self.assertEqual(
            checks["watcher"]["detail"],
            str(self.suite_root / "loop-triage-github" / "scripts" / "watch-prs.py"),
        )


class SkillsLibraryLayoutTests(unittest.TestCase):
    """The default suite root is this loop-kit's parent, wherever that is."""

    def test_default_suite_root_is_the_loop_kit_parent(self) -> None:
        self.assertEqual(loopkit.SKILL_ROOT, Path(loopkit.__file__).resolve().parents[1])
        self.assertEqual(loopkit.SKILL_ROOT.name, "loop-kit")
        self.assertTrue((loopkit.SKILL_ROOT / "SKILL.md").is_file())
        # The suite root is the skill's parent, not the skill itself and not the
        # repository root: in a target project it is <repo>/.claude/skills.
        self.assertEqual(loopkit.SUITE_ROOT, loopkit.SKILL_ROOT.parent)
        self.assertNotEqual(loopkit.SUITE_ROOT, loopkit.SKILL_ROOT)

    def test_default_doctor_finds_this_library_layout(self) -> None:
        """Run with no --suite-root: in the library the siblings sit next to loop-kit."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp).resolve() / "target"
            repo.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=str(repo), capture_output=True, text=True, timeout=60)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://github.com/owner/target.git"],
                cwd=str(repo), capture_output=True, text=True, timeout=60,
            )
            state = Path(tmp).resolve() / "state"
            real_gh = loopkit.run_gh
            loopkit.run_gh = fake_gh()
            try:
                code, out, err = run_loopkit(
                    "--repo-root", str(repo), "init", "--state-dir", str(state)
                )
                self.assertEqual(code, 0, err)
                code, out, _ = run_loopkit("--repo-root", str(repo), "doctor")
            finally:
                loopkit.run_gh = real_gh
            self.assertEqual(code, 0, out)
            self.assertIn("PASS skill triage-github", out)
            self.assertIn("PASS skill nightly-review", out)
            self.assertIn("PASS watcher", out)
            self.assertIn(str(loopkit.SUITE_ROOT / "loop-triage-github"), out)

    def test_next_steps_uses_the_suite_root_it_is_given(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            suite_root = Path(tmp).resolve() / "nested" / "skills"
            suite_root.mkdir(parents=True)
            make_sibling_skills(suite_root)
            (suite_root / "loop-nightly-review" / "SKILL.md").unlink()
            lines = loopkit.next_steps({"loops": {}}, suite_root)
            self.assertIn(
                "  npx --yes skills@latest add oldwinter/skills --skill loop-kit loop-nightly-review",
                lines,
            )
            self.assertIn(f"  (installs into {suite_root}, where this loop-kit lives)", lines)
            self.assertTrue(any("<kit-dir>/references/harnesses.md" in line for line in lines))


class LockTests(LoopKitTestCase):
    def test_lock_acquire_release_and_status(self) -> None:
        self.init()
        code, out, _ = run_loopkit(
            "--repo-root", str(self.repo), "lock", "acquire", "--name", "triage-github"
        )
        self.assertEqual(code, 0)
        self.assertIn("acquired lock triage-github", out)
        self.assertTrue((self.state / "tick-triage-github.lock").is_file())

        code, out, _ = run_loopkit(
            "--repo-root", str(self.repo), "lock", "status", "--name", "triage-github"
        )
        self.assertEqual(code, 0)
        self.assertIn("held", out)

        code, out, _ = run_loopkit(
            "--repo-root", str(self.repo), "lock", "release", "--name", "triage-github"
        )
        self.assertEqual(code, 0)
        self.assertFalse((self.state / "tick-triage-github.lock").exists())

        code, out, _ = run_loopkit(
            "--repo-root", str(self.repo), "lock", "status", "--name", "triage-github"
        )
        self.assertEqual(code, 0)
        self.assertIn("free", out)

    def test_lock_contention_exits_three(self) -> None:
        self.init()
        run_loopkit("--repo-root", str(self.repo), "lock", "acquire", "--name", "nightly-review")
        code, _, err = run_loopkit(
            "--repo-root", str(self.repo), "lock", "acquire", "--name", "nightly-review"
        )
        self.assertEqual(code, 3)
        self.assertIn("is held by pid", err)

    def test_stale_lock_is_taken_over_with_a_report(self) -> None:
        self.init()
        path = lockfile.lock_path(self.state, "triage-github")
        path.write_text(
            json.dumps(
                {
                    "name": "triage-github",
                    "pid": 4242,
                    "host": "elsewhere",
                    "acquiredAt": "2020-01-01T00:00:00Z",
                }
            ),
            encoding="utf-8",
        )
        code, out, err = run_loopkit(
            "--repo-root", str(self.repo), "lock", "acquire", "--name", "triage-github"
        )
        self.assertEqual(code, 0, err)
        self.assertIn("took over lock triage-github from pid 4242", out)
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertNotEqual(payload["pid"], 4242)

    def test_release_of_an_unheld_lock_is_refused(self) -> None:
        self.init()
        code, _, err = run_loopkit(
            "--repo-root", str(self.repo), "lock", "release", "--name", "triage-github"
        )
        self.assertEqual(code, 3)
        self.assertIn("not held", err)


class StatusAndConfigTests(LoopKitTestCase):
    def test_status_counts_cards_and_reports_locks(self) -> None:
        self.init()
        desk = self.state / "desk"
        (desk / "1.json").write_text(json.dumps({"id": "1", "status": "pending"}), encoding="utf-8")
        (desk / "2.json").write_text(json.dumps({"id": "2", "status": "sent"}), encoding="utf-8")
        run_loopkit("--repo-root", str(self.repo), "lock", "acquire", "--name", "triage-github")

        code, out, _ = run_loopkit("--repo-root", str(self.repo), "status", "--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["cards"], {"pending": 1, "sent": 1})
        locks = {lock["name"]: lock for lock in payload["locks"]}
        self.assertTrue(locks["triage-github"]["held"])
        self.assertFalse(locks["nightly-review"]["held"])

        code, out, _ = run_loopkit("--repo-root", str(self.repo), "status")
        self.assertEqual(code, 0)
        self.assertIn("cards        pending: 1", out)
        self.assertIn("lock         triage-github: held", out)

    def test_status_and_config_need_a_config(self) -> None:
        code, _, err = run_loopkit("--repo-root", str(self.repo), "status")
        self.assertEqual(code, 2)
        self.assertIn("loopkit.py init", err)
        code, _, err = run_loopkit("--repo-root", str(self.repo), "config")
        self.assertEqual(code, 2)

    def test_config_prints_the_resolved_file(self) -> None:
        self.init()
        code, out, _ = run_loopkit("--repo-root", str(self.repo), "config")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), self.read_config())


class UnitTests(unittest.TestCase):
    def test_parse_remote_forms(self) -> None:
        for url in (
            "https://github.com/owner/myapp.git",
            "https://github.com/owner/myapp",
            "git@github.com:owner/myapp.git",
            "ssh://git@github.com/owner/myapp.git",
        ):
            self.assertEqual(loopkit.parse_remote(url), "owner/myapp", url)
        for url in ("", "not a url", "https://github.com/owner"):
            self.assertIsNone(loopkit.parse_remote(url), url)

    def test_cron_for_interval(self) -> None:
        self.assertEqual(loopkit.cron_for_interval("5m"), "*/5 * * * *")
        self.assertEqual(loopkit.cron_for_interval("30m"), "*/30 * * * *")
        self.assertEqual(loopkit.cron_for_interval("60m"), "0 */1 * * *")
        self.assertEqual(loopkit.cron_for_interval("2h"), "0 */2 * * *")
        self.assertEqual(loopkit.cron_for_interval("24h"), "0 3 * * *")
        self.assertIn("unknown interval", loopkit.cron_for_interval("sometimes"))

    def test_scheduler_lines_skip_disabled_loops(self) -> None:
        config = {"loops": {"triage-github": {"interval": "30m", "enabled": True}, "watch-social": {"interval": "60m", "enabled": False}}}
        lines = loopkit.scheduler_lines(config)
        self.assertTrue(lines[0].startswith(loopkit.SEND_CHECK_CRON))
        self.assertIn("*/30 * * * *  # triage-github tick (every 30m)", lines)
        self.assertTrue(any(line.startswith("# watch-social is disabled") for line in lines))

    def test_render_template_substitutes_every_placeholder(self) -> None:
        config = {
            "project": "myapp",
            "repo": "owner/myapp",
            "stateDir": "~/.local/state/myapp-loops",
            "lessonsPath": "LESSONS.md",
            "rulesPath": ".agents/rules/acceptance.md",
        }
        text = loopkit.render_template("{{project}} {{repo}} {{stateDir}} {{lessonsPath}} {{rulesPath}}", config)
        self.assertEqual(
            text,
            "myapp owner/myapp ~/.local/state/myapp-loops LESSONS.md .agents/rules/acceptance.md",
        )

    def test_no_shipped_file_starts_with_a_utf8_bom(self) -> None:
        """The repo's contract checker reads plain utf-8; a BOM would hide frontmatter."""
        skill_root = Path(__file__).resolve().parents[1]
        offenders = [
            str(path.relative_to(skill_root))
            for path in sorted(skill_root.rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts and path.read_bytes()[:3] == b"\xef\xbb\xbf"
        ]
        self.assertEqual(offenders, [])

    def test_run_gh_decodes_output_as_utf8(self) -> None:
        """gh prints box-drawing and check-mark characters a console code page cannot decode."""
        captured: dict = {}

        def fake_run(argv, **kwargs):
            captured.update(kwargs)
            if kwargs.get("encoding") != "utf-8":
                raise UnicodeDecodeError("gbk", b"\x93", 15, 16, "illegal multibyte sequence")
            return subprocess.CompletedProcess(argv, 0, "github.com\n  \u2713 Logged in to github.com account octocat\n", "")

        with mock.patch.object(loopkit.subprocess, "run", fake_run):
            code, stdout, stderr = loopkit.run_gh(["auth", "status"])
        self.assertEqual(code, 0)
        self.assertEqual(captured.get("encoding"), "utf-8")
        self.assertEqual(captured.get("errors"), "replace")
        self.assertIn("octocat", stdout)
        self.assertEqual(stderr, "")

    def test_run_gh_reports_a_missing_binary_instead_of_raising(self) -> None:
        def fake_run(argv, **kwargs):
            raise FileNotFoundError("gh")

        with mock.patch.object(loopkit.subprocess, "run", fake_run):
            code, _, stderr = loopkit.run_gh(["--version"])
        self.assertEqual(code, 127)
        self.assertIn("gh", stderr)

    def test_write_json_is_atomic_and_leaves_no_temp_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "card.json"
            lockfile.write_json(path, {"id": "1"})
            lockfile.write_json(path, {"id": "2"})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"id": "2"})
            leftovers = [p.name for p in Path(tmp).iterdir() if p.name != "card.json"]
            self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
