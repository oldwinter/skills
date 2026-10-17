#!/usr/bin/env python3
"""loop-kit runtime: init, doctor, status, config and the tick lock.

``init`` writes ``<repo>/.loop/config.json``, the state directory, the
``LESSONS.md`` and acceptance-rules templates, and its own marked block in
``AGENTS.md``. It is idempotent: an existing config keeps every key it has,
including keys this tool does not know, and an existing ``LESSONS.md`` or rules
file is never overwritten.

Standard library only; Windows and POSIX.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lockfile  # noqa: E402  (sibling module, resolved above)

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2
EXIT_STATE = 3

SKILL_ROOT = Path(__file__).resolve().parents[1]
# The directory the four skills are installed into: the loop-kit skill's own
# parent, which is where the sibling tick skills live. It is the repository root
# only inside the skills library; in a target project it is
# `<repo>/.claude/skills`.
SUITE_ROOT = SKILL_ROOT.parent
TEMPLATES_DIR = SKILL_ROOT / "templates"
BLOCK_BEGIN = "<!-- loop-kit:begin -->"
BLOCK_END = "<!-- loop-kit:end -->"

LOOP_SKILL_DIRS = {
    "triage-github": "loop-triage-github",
    "watch-social": "loop-watch-social",
    "nightly-review": "loop-nightly-review",
}
LOOP_DEFAULTS: dict[str, dict] = {
    "triage-github": {"interval": "30m", "enabled": True},
    "watch-social": {"interval": "60m", "enabled": False, "sources": ["x", "discord", "reddit"]},
    "nightly-review": {"interval": "24h", "enabled": True},
}
SEND_CHECK_CRON = "4-59/5 * * * *"

CONFIG_TEMPLATE: dict = {
    "version": 1,
    "project": None,
    "repo": None,
    "defaultBranch": "main",
    "stateDir": None,
    "lessonsPath": "LESSONS.md",
    "rulesPath": ".agents/rules/acceptance.md",
    "agentsPath": "AGENTS.md",
    "verifyDoc": None,
    "worktreeCmd": None,
    "checks": [],
    "trustedLogins": ["coderabbitai[bot]"],
    "windowDays": 3,
    "desk": {"kind": "files"},
    "loops": {},
}

TEMPLATE_FILES = {
    "lessonsPath": "LESSONS.md",
    "rulesPath": "acceptance.md",
}


class UsageError(Exception):
    """Bad arguments or an unusable repository (exit code 2)."""


def default_state_dir(project: str) -> str:
    return f"~/.local/state/{project}-loops"


def expand_state_dir(value: str) -> Path:
    return Path(os.path.expanduser(str(value)))


# --------------------------------------------------------------------------
# repository facts
# --------------------------------------------------------------------------


def git(args: list[str], repo_root: Path, check: bool = False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as error:
        if check:
            raise UsageError(f"git {' '.join(args)} failed: {error}") from error
        return subprocess.CompletedProcess(["git", *args], 1, "", str(error))


def remote_repo(repo_root: Path) -> str | None:
    result = git(["remote", "get-url", "origin"], repo_root)
    if result.returncode != 0:
        return None
    return parse_remote(result.stdout.strip())


def parse_remote(url: str) -> str | None:
    """``owner/name`` from an https, ssh or scp-style remote URL."""
    if not url:
        return None
    text = url.strip()
    if text.endswith(".git"):
        text = text[: -len(".git")]
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", text):
        parts = [part for part in text.split("://", 1)[1].split("/") if part]
        if len(parts) < 3:
            return None
        return f"{parts[-2]}/{parts[-1]}"
    scp = re.match(r"^([^/:\s]+):(.*)$", text)
    if scp:
        parts = [part for part in scp.group(2).split("/") if part]
        if len(parts) < 2:
            return None
        return f"{parts[-2]}/{parts[-1]}"
    parts = [part for part in text.split("/") if part]
    if len(parts) != 2:
        return None
    return f"{parts[0]}/{parts[1]}"


def current_branch(repo_root: Path) -> str | None:
    result = git(["symbolic-ref", "--quiet", "--short", "HEAD"], repo_root)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return None


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------


def config_path(repo_root: Path) -> Path:
    return Path(repo_root) / ".loop" / "config.json"


def load_config(repo_root: Path) -> dict | None:
    payload = lockfile.read_json(config_path(repo_root))
    return payload if isinstance(payload, dict) else None


def build_config(existing: dict | None, args: argparse.Namespace, repo_root: Path) -> dict:
    config = dict(CONFIG_TEMPLATE)
    config["loops"] = {name: dict(values) for name, values in LOOP_DEFAULTS.items()}
    if existing:
        for key, value in existing.items():
            config[key] = value
        loops = existing.get("loops")
        if isinstance(loops, dict):
            merged = {name: dict(values) for name, values in LOOP_DEFAULTS.items()}
            for name, values in loops.items():
                if isinstance(values, dict) and isinstance(merged.get(name), dict):
                    merged[name].update(values)
                else:
                    merged[name] = values
            config["loops"] = merged

    detected = remote_repo(repo_root)
    if args.repo:
        config["repo"] = args.repo
    elif not config.get("repo"):
        config["repo"] = detected
    if args.project:
        config["project"] = args.project
    elif not config.get("project"):
        if config.get("repo"):
            config["project"] = str(config["repo"]).split("/")[-1]
        else:
            config["project"] = Path(repo_root).resolve().name
    if args.state_dir:
        config["stateDir"] = args.state_dir
    elif not config.get("stateDir"):
        config["stateDir"] = default_state_dir(str(config["project"]))
    if args.default_branch:
        config["defaultBranch"] = args.default_branch
    elif not config.get("defaultBranch"):
        config["defaultBranch"] = current_branch(repo_root) or "main"
    for flag, key in (
        ("lessons", "lessonsPath"),
        ("rules", "rulesPath"),
        ("agents", "agentsPath"),
    ):
        value = getattr(args, flag, None)
        if value:
            config[key] = value
    if not config.get("lessonsPath"):
        config["lessonsPath"] = CONFIG_TEMPLATE["lessonsPath"]
    if not config.get("rulesPath"):
        config["rulesPath"] = CONFIG_TEMPLATE["rulesPath"]
    if not config.get("agentsPath"):
        config["agentsPath"] = CONFIG_TEMPLATE["agentsPath"]
    if not isinstance(config.get("desk"), dict) or not config["desk"].get("kind"):
        config["desk"] = {"kind": "files"}
    if not isinstance(config.get("checks"), list):
        config["checks"] = []
    if not isinstance(config.get("trustedLogins"), list):
        config["trustedLogins"] = list(CONFIG_TEMPLATE["trustedLogins"])
    try:
        config["version"] = int(config.get("version") or 1)
    except (TypeError, ValueError):
        config["version"] = 1
    return config


# --------------------------------------------------------------------------
# state dir and templates
# --------------------------------------------------------------------------


def state_files() -> dict[str, object]:
    return {
        "github.json": {"since": None},
        "social.json": {"seen": {"x": [], "discord": {}, "reddit": []}, "pending": []},
        "watch.json": [],
    }


def create_state(state_dir: Path) -> list[str]:
    created: list[str] = []
    for relative in ("", "desk", "desk/archive"):
        target = state_dir / relative if relative else state_dir
        if not target.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            created.append(str(target.resolve()))
    for name, payload in state_files().items():
        path = state_dir / name
        if not path.exists():
            lockfile.write_json(path, payload)
            created.append(str(path.resolve()))
    return created


def render_template(text: str, config: dict) -> str:
    values = {
        "project": str(config.get("project") or "project"),
        "repo": str(config.get("repo") or "owner/name"),
        "defaultBranch": str(config.get("defaultBranch") or "main"),
        "stateDir": str(config.get("stateDir") or default_state_dir("project")),
        "lessonsPath": str(config.get("lessonsPath") or "LESSONS.md"),
        "rulesPath": str(config.get("rulesPath") or ".agents/rules/acceptance.md"),
        "agentsPath": str(config.get("agentsPath") or "AGENTS.md"),
        "skillRoot": "loop-kit",
    }
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def template_text(name: str, config: dict, templates_dir: Path | None = None) -> str:
    directory = Path(templates_dir) if templates_dir else TEMPLATES_DIR
    path = directory / name
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as error:
        raise UsageError(f"missing template {path}: {error}") from error
    return render_template(raw, config)


def update_agents_block(repo_root: Path, config: dict, templates_dir: Path | None = None) -> tuple[bool, str]:
    """Insert or replace the loop-kit block. Returns (changed, detail)."""
    block = template_text("agents-block.md", config, templates_dir).strip()
    marked = f"{BLOCK_BEGIN}\n{block}\n{BLOCK_END}"
    path = Path(repo_root) / str(config.get("agentsPath") or "AGENTS.md")
    existing = ""
    if path.exists():
        existing = path.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(BLOCK_BEGIN) + r".*?" + re.escape(BLOCK_END),
        re.DOTALL,
    )
    if pattern.search(existing):
        if pattern.search(existing).group(0) == marked:
            return False, f"{path} block already current"
        updated = pattern.sub(lambda _match: marked, existing, count=1)
    elif existing:
        updated = existing.rstrip("\n") + "\n\n" + marked + "\n"
    else:
        updated = marked + "\n"
    lockfile.write_text(path, updated)
    return True, f"{path} block written"


# --------------------------------------------------------------------------
# doctor
# --------------------------------------------------------------------------


def make_check(name: str, status: str, detail: str) -> dict:
    return {"name": name, "status": status, "detail": detail}


def run_gh(args: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """The one place the doctor calls ``gh``; tests replace this.

    Output is decoded as UTF-8 with replacement: ``gh`` prints box-drawing and
    check-mark characters, and a Windows console code page cannot decode them.
    """
    try:
        result = subprocess.run(
            ["gh", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return 127, "", str(error)
    return result.returncode, result.stdout or "", result.stderr or ""


def gh_version(runner=None) -> tuple[bool, str]:
    if runner is None:
        if not shutil.which("gh"):
            return False, "gh is not on PATH"
        runner = globals()["run_gh"]
    code, stdout, stderr = runner(["--version"])
    if code != 0:
        first = (stderr.strip().splitlines() or ["no output"])[0]
        return False, f"gh --version exited {code}: {first[:120]}"
    lines = stdout.strip().splitlines()
    return True, lines[0] if lines else "gh (no version output)"


def gh_login(runner=None) -> tuple[bool, str]:
    if runner is None:
        if not shutil.which("gh"):
            return False, "gh is not on PATH"
        runner = globals()["run_gh"]
    code, stdout, stderr = runner(["auth", "status"])
    text = (stdout or "") + (stderr or "")
    match = re.search(r"Logged in to [^\s]+ account ([^\s(]+)", text)
    if code == 0 and match:
        return True, f"logged in as {match.group(1)}"
    if match:
        return False, f"logged in as {match.group(1)} but gh auth status exited {code}"
    return False, "gh is not authenticated: run gh auth login"


def check_state_writable(state_dir: Path) -> tuple[bool, str]:
    probe = state_dir / ".loopkit-write-probe"
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        probe.write_text("probe\n", encoding="utf-8")
        probe.unlink()
    except OSError as error:
        return False, f"{state_dir} is not writable: {error}"
    return True, f"{state_dir} is writable"


def check_desk_renders(state_dir: Path) -> tuple[bool, str]:
    """Render an empty desk through the real renderer, into a throwaway file.

    The probe must not touch ``desk/index.html``: a doctor run would otherwise
    replace the page the maintainer is reading with an empty one.
    """
    import desk as desk_cli  # sibling module; imported here to keep loopkit importable alone

    desk = state_dir / "desk"
    desk.mkdir(parents=True, exist_ok=True)
    probe = desk / ".loopkit-render-probe.html"
    try:
        lockfile.write_text(probe, desk_cli.render_page([]))
        if not probe.is_file():
            return False, f"{probe} was not written"
    except OSError as error:
        return False, f"cannot render into {desk}: {error}"
    finally:
        try:
            probe.unlink()
        except OSError:
            pass
    return True, f"renders into {desk}"


def collect_checks(
    repo_root: Path,
    config: dict | None,
    templates_dir: Path | None = None,
    runner=None,
    suite_root: Path | None = None,
) -> list[dict]:
    """Check the install.

    ``suite_root`` is where the sibling skills are installed: the parent of the
    loop-kit skill directory itself, not the target repository. The two coincide
    only inside the skills library, which is why the default is this file's own
    grandparent.
    """
    runner = runner or globals()["run_gh"]
    checks: list[dict] = []

    version = sys.version_info
    if version >= (3, 9):
        checks.append(make_check("python", "PASS", f"{version.major}.{version.minor}.{version.micro}"))
    else:
        checks.append(make_check("python", "FAIL", f"{version.major}.{version.minor} is older than 3.9"))

    loops = config.get("loops") if isinstance(config, dict) else {}
    loops = loops if isinstance(loops, dict) else {}
    github_enabled = bool((loops.get("triage-github") or {}).get("enabled"))

    have_gh, gh_detail = gh_version(runner)
    if have_gh:
        checks.append(make_check("gh", "PASS", gh_detail))
    elif github_enabled:
        checks.append(make_check("gh", "FAIL", gh_detail))
    else:
        checks.append(make_check("gh", "SKIP", f"{gh_detail}; the github loop is disabled"))

    if have_gh:
        ok, detail = gh_login(runner)
        checks.append(make_check("gh auth", "PASS" if ok else ("FAIL" if github_enabled else "WARN"), detail))
    else:
        checks.append(make_check("gh auth", "SKIP", "no gh on PATH"))

    if config is None:
        checks.append(
            make_check(
                "config",
                "FAIL",
                f"{config_path(repo_root)} is missing or not valid JSON: run loopkit.py init",
            )
        )
    else:
        checks.append(make_check("config", "PASS", f"{config_path(repo_root)} parses"))

    detected = remote_repo(repo_root)
    configured = str((config or {}).get("repo") or "")
    if not detected:
        checks.append(
            make_check(
                "repo",
                "SKIP" if not configured else "WARN",
                "no origin remote to compare against" if not configured else f"no origin remote; config says {configured}",
            )
        )
    elif not configured:
        checks.append(make_check("repo", "FAIL", f"config has no repo; origin is {detected}"))
    elif detected.lower() != configured.lower():
        checks.append(make_check("repo", "WARN", f"config {configured} != origin {detected}"))
    else:
        checks.append(make_check("repo", "PASS", f"{configured} matches origin"))

    state_dir = expand_state_dir(str((config or {}).get("stateDir") or default_state_dir("project")))
    if config is None:
        checks.append(make_check("state dir", "SKIP", "no config to name the state dir"))
    else:
        ok, detail = check_state_writable(state_dir)
        checks.append(make_check("state dir", "PASS" if ok else "FAIL", detail))

    if config is None:
        checks.append(make_check("desk renders", "SKIP", "no config to name the desk"))
    else:
        ok, detail = check_desk_renders(state_dir)
        checks.append(make_check("desk renders", "PASS" if ok else "FAIL", detail))

    for key, label in (("lessonsPath", "lessons file"), ("rulesPath", "rules file")):
        relative = (config or {}).get(key)
        if not relative:
            checks.append(make_check(label, "FAIL", f"config has no {key}"))
            continue
        target = Path(repo_root) / str(relative)
        if target.is_file():
            checks.append(make_check(label, "PASS", str(target)))
        else:
            checks.append(make_check(label, "FAIL", f"{target} is missing: run loopkit.py init"))

    agents_path = Path(repo_root) / str((config or {}).get("agentsPath") or "AGENTS.md")
    if not agents_path.is_file():
        checks.append(make_check("AGENTS.md block", "FAIL", f"{agents_path} is missing"))
    else:
        text = agents_path.read_text(encoding="utf-8")
        if BLOCK_BEGIN in text and BLOCK_END in text:
            checks.append(make_check("AGENTS.md block", "PASS", f"{agents_path} carries the loop-kit block"))
        else:
            checks.append(make_check("AGENTS.md block", "FAIL", f"{agents_path} has no loop-kit block: run loopkit.py init"))

    suite_root = Path(suite_root) if suite_root else SUITE_ROOT
    for name, values in loops.items():
        if not isinstance(values, dict) or not values.get("enabled"):
            continue
        directory = suite_root / LOOP_SKILL_DIRS.get(name, f"loop-{name}")
        if (directory / "SKILL.md").is_file():
            checks.append(make_check(f"skill {name}", "PASS", str(directory)))
        else:
            checks.append(
                make_check(
                    f"skill {name}",
                    "FAIL",
                    f"{directory} is missing: {install_command([LOOP_SKILL_DIRS.get(name, name)])}",
                )
            )

    if github_enabled:
        watcher = suite_root / LOOP_SKILL_DIRS["triage-github"] / "scripts" / "watch-prs.py"
        if watcher.is_file():
            checks.append(make_check("watcher", "PASS", str(watcher)))
        else:
            checks.append(make_check("watcher", "FAIL", f"{watcher} is missing"))
    else:
        checks.append(make_check("watcher", "SKIP", "the github loop is disabled"))

    return checks


def worst(checks: list[dict]) -> int:
    return EXIT_FAIL if any(check["status"] == "FAIL" for check in checks) else EXIT_OK


def print_checks(checks: list[dict]) -> None:
    width = max((len(check["name"]) for check in checks), default=4)
    for check in checks:
        print(f"{check['status']:4} {check['name']:<{width}}  {check['detail']}")


# --------------------------------------------------------------------------
# scheduler lines
# --------------------------------------------------------------------------


def cron_for_interval(interval: str) -> str:
    text = str(interval or "").strip().lower()
    match = re.fullmatch(r"(\d+)\s*([mhd])", text)
    if not match:
        return f"# unknown interval {interval!r}: schedule this loop by hand"
    value, unit = int(match.group(1)), match.group(2)
    if unit == "m":
        if value < 60:
            return f"*/{value} * * * *"
        return f"0 */{max(1, value // 60)} * * *"
    if unit == "h":
        return f"0 */{value} * * *" if value < 24 else "0 3 * * *"
    return "0 3 * * *"


def scheduler_lines(config: dict) -> list[str]:
    lines = [f"{SEND_CHECK_CRON}  # desk send check: post approved cards within five minutes"]
    loops = config.get("loops") if isinstance(config.get("loops"), dict) else {}
    for name in ("triage-github", "watch-social", "nightly-review"):
        values = loops.get(name) if isinstance(loops.get(name), dict) else {}
        interval = str(values.get("interval") or LOOP_DEFAULTS[name]["interval"])
        if values.get("enabled"):
            lines.append(f"{cron_for_interval(interval)}  # {name} tick (every {interval})")
        else:
            lines.append(f"# {name} is disabled in .loop/config.json (interval {interval})")
    return lines


SKILLS_PACKAGE = "oldwinter/skills"


def install_command(skill_names: list[str]) -> str:
    """The real install command for the skills this kit does not ship."""
    names = " ".join(skill_names)
    return f"npx --yes skills@latest add {SKILLS_PACKAGE} --skill loop-kit {names}"


def next_steps(config: dict, suite_root: Path) -> list[str]:
    """What the user does next: install what is missing, then arm a scheduler.

    ``suite_root`` is the directory the sibling skills are installed into — the
    loop-kit skill's own parent — not the target repository.
    """
    missing = [
        LOOP_SKILL_DIRS[name]
        for name in ("triage-github", "watch-social", "nightly-review")
        if not (Path(suite_root) / LOOP_SKILL_DIRS[name] / "SKILL.md").is_file()
    ]
    lines: list[str] = []
    if missing:
        lines.append("Install the sibling skills next to loop-kit:")
        lines.append(f"  {install_command(missing)}")
        lines.append(f"  (installs into {suite_root}, where this loop-kit lives)")
    else:
        lines.append("All three tick skills are installed next to loop-kit.")
    lines.append("Arm one scheduler line per loop (see <kit-dir>/references/harnesses.md):")
    lines.extend(f"  {line}" for line in scheduler_lines(config))
    return lines


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------


def cmd_init(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    if not repo_root.is_dir():
        raise UsageError(f"{repo_root} is not a directory")
    existing = load_config(repo_root)
    if config_path(repo_root).exists() and existing is None and not args.force:
        raise UsageError(f"{config_path(repo_root)} exists but is not valid JSON: fix it or pass --force")
    config = build_config(existing, args, repo_root)
    lockfile.write_json(config_path(repo_root), config)
    print(f"config   {config_path(repo_root)}")
    state_dir = expand_state_dir(str(config["stateDir"]))
    for created in create_state(state_dir):
        print(f"state    {created}")
    templates_dir = Path(args.templates) if args.templates else None
    for key, template_name in TEMPLATE_FILES.items():
        target = repo_root / str(config[key])
        if target.exists():
            print(f"kept     {target} (already there)")
            continue
        lockfile.write_text(target, template_text(template_name, config, templates_dir))
        print(f"template {target}")
    changed, detail = update_agents_block(repo_root, config, templates_dir)
    print(("wrote    " if changed else "kept     ") + detail)

    print("")
    suite_root = Path(args.suite_root).resolve() if args.suite_root else SUITE_ROOT
    checks = collect_checks(repo_root, config, templates_dir, suite_root=suite_root)
    print_checks(checks)
    failures = [check for check in checks if check["status"] == "FAIL"]
    print("")
    if failures:
        print(f"{len(failures)} check(s) FAIL: fix them before arming a scheduler.")
    else:
        print("doctor: no FAIL rows.")
    print("")
    for line in next_steps(config, suite_root):
        print(line)
    return EXIT_OK


def cmd_doctor(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    config = load_config(repo_root)
    suite_root = Path(args.suite_root).resolve() if args.suite_root else SUITE_ROOT
    checks = collect_checks(repo_root, config, suite_root=suite_root)
    if args.json:
        print(json.dumps({"checks": checks, "exit": worst(checks)}, indent=2, sort_keys=True))
    else:
        print_checks(checks)
        failed = [check["name"] for check in checks if check["status"] == "FAIL"]
        print("doctor: FAIL " + ", ".join(failed) if failed else "doctor: no FAIL rows.")
    return worst(checks)


def cmd_status(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    config = load_config(repo_root)
    if config is None:
        raise UsageError(f"{config_path(repo_root)} is missing: run loopkit.py init")
    state_dir = expand_state_dir(str(config["stateDir"]))
    desk = state_dir / "desk"
    cards: dict[str, int] = {}
    for path in sorted(desk.glob("*.json")) if desk.is_dir() else []:
        payload = lockfile.read_json(path)
        if isinstance(payload, dict):
            status = str(payload.get("status") or "unknown")
            cards[status] = cards.get(status, 0) + 1
    locks = []
    loops = config.get("loops") if isinstance(config.get("loops"), dict) else {}
    for name in loops:
        locks.append(lockfile.lock_state(state_dir, str(name)))
    report = {
        "project": config.get("project"),
        "repo": config.get("repo"),
        "defaultBranch": config.get("defaultBranch"),
        "stateDir": str(state_dir),
        "configPath": str(config_path(repo_root)),
        "cards": cards,
        "locks": [
            {
                "name": lock["name"],
                "held": lock["held"],
                "stale": lock["stale"],
                "ageSeconds": lock["ageSeconds"],
            }
            for lock in locks
        ],
    }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return EXIT_OK
    print(f"project      {report['project']}")
    print(f"repo         {report['repo']}")
    print(f"branch       {report['defaultBranch']}")
    print(f"state        {report['stateDir']}")
    print(f"config       {report['configPath']}")
    if cards:
        for status in sorted(cards):
            print(f"cards        {status}: {cards[status]}")
    else:
        print("cards        none")
    for lock in report["locks"]:
        if lock["held"]:
            age = "" if lock["ageSeconds"] is None else f", {int(lock['ageSeconds'])}s old"
            print(f"lock         {lock['name']}: held{' (stale)' if lock['stale'] else ''}{age}")
        else:
            print(f"lock         {lock['name']}: free")
    return EXIT_OK


def cmd_config(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    config = load_config(repo_root)
    if config is None:
        raise UsageError(f"{config_path(repo_root)} is missing: run loopkit.py init")
    print(json.dumps(config, indent=2, sort_keys=True))
    return EXIT_OK


def cmd_lock(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    config = load_config(repo_root)
    state_dir = expand_state_dir(
        str((config or {}).get("stateDir") or default_state_dir(Path(repo_root).name))
    )
    name = args.name
    if args.action == "acquire":
        result = lockfile.acquire(state_dir, name, stale_seconds=args.stale_seconds)
        if not result["ok"]:
            current = result.get("current") or {}
            payload = current.get("payload") or {}
            print(
                f"lock {name} is held by pid {payload.get('pid', '?')} on "
                f"{payload.get('host', '?')} since {payload.get('acquiredAt', '?')}",
                file=sys.stderr,
            )
            return EXIT_STATE
        if result.get("tookOver"):
            previous = result.get("previous") or {}
            age = result.get("previousAgeSeconds")
            print(
                f"took over lock {name} from pid {previous.get('pid', '?')} "
                f"(age {int(age) if age is not None else '?'}s > {args.stale_seconds}s)"
            )
        else:
            print(f"acquired lock {name}")
        return EXIT_OK
    if args.action == "release":
        result = lockfile.release(state_dir, name)
        if not result["ok"]:
            print(f"lock {name}: {result['reason']}", file=sys.stderr)
            return EXIT_STATE
        print(f"released lock {name}")
        return EXIT_OK
    state = lockfile.lock_state(state_dir, name, stale_seconds=args.stale_seconds)
    if args.json:
        print(json.dumps(state, indent=2, sort_keys=True, default=str))
        return EXIT_OK
    if not state["held"]:
        print(f"lock {name}: free")
        return EXIT_OK
    age = state["ageSeconds"]
    print(
        f"lock {name}: held{' (stale)' if state['stale'] else ''}"
        f"{'' if age is None else f', {int(age)}s old'}"
    )
    return EXIT_OK


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="loopkit.py", description="loop-kit runtime for the maintenance-loop suite.")
    parser.add_argument("--repo-root", default=".", help="repository root (default: the current directory)")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="write config, state dir, templates and the AGENTS.md block")
    init.add_argument("--repo", default=None, help="owner/name (default: parsed from git origin)")
    init.add_argument("--project", default=None, help="project name (default: the repo name)")
    init.add_argument("--state-dir", default=None, help="state directory (default: ~/.local/state/<project>-loops)")
    init.add_argument("--lessons", default=None, help="lessons file path in the repo")
    init.add_argument("--rules", default=None, help="acceptance rules path in the repo")
    init.add_argument("--agents", default=None, help="agents file to mark")
    init.add_argument("--default-branch", default=None, help="branch a tick works from")
    init.add_argument("--templates", default=None, help="template directory override (testing)")
    init.add_argument(
        "--suite-root",
        default=None,
        help="directory the sibling skills are installed into (default: this loop-kit skill's parent)",
    )
    init.add_argument("--force", action="store_true", help="overwrite an unparsable config")
    init.set_defaults(func=cmd_init)

    doctor = sub.add_parser("doctor", help="check the install")
    doctor.add_argument("--json", action="store_true")
    doctor.add_argument(
        "--suite-root",
        default=None,
        help="directory the sibling skills are installed into (default: this loop-kit skill's parent)",
    )
    doctor.set_defaults(func=cmd_doctor)

    status = sub.add_parser("status", help="show config, card counts and locks")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=cmd_status)

    config = sub.add_parser("config", help="print the resolved config")
    config.add_argument("--json", action="store_true")
    config.set_defaults(func=cmd_config)

    lock = sub.add_parser("lock", help="tick lock")
    lock.add_argument("action", choices=("acquire", "release", "status"))
    lock.add_argument("--name", required=True, help="loop name")
    lock.add_argument("--stale-seconds", type=int, default=lockfile.DEFAULT_STALE_SECONDS)
    lock.add_argument("--json", action="store_true")
    lock.set_defaults(func=cmd_lock)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except UsageError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())
