from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from skills_doctor.catalog import (
    KNOWN_TOOLS, CatalogError, discover_skills, load_catalog, tool_mentions, unreviewed_catalog,
)
from skills_doctor.probes import Check, Probes

def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Inspect skill prerequisites without running skill workflows.")
    result.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Target checkout, not the skill install directory")
    result.add_argument("--skills-dir", action="append", help="Skill directory relative to target checkout; repeatable")
    result.add_argument("--catalog", type=Path, help="Curated catalog inside target checkout; otherwise inventory stays unverified")
    select = result.add_mutually_exclusive_group()
    select.add_argument("--skill", action="append", help="Exact repo skill name; repeatable")
    select.add_argument("--all", action="store_true", help="Inspect every skill/profile offline (default)")
    result.add_argument("--profile", help="Required for a selected skill with several execution profiles")
    result.add_argument("--live", action="append", choices=["lark", "gitlab", "github", "aws", "kube"], default=[])
    result.add_argument("--gitlab-host", help="Expected host of this checkout's GitLab origin")
    result.add_argument("--github-org", help="Explicit GitHub organization slug")
    result.add_argument("--aws-profile", help="Named operator-local AWS profile")
    result.add_argument("--aws-account", help="Expected AWS account ID (never emitted)")
    result.add_argument("--kube-context", help="Explicit Kubernetes context")
    result.add_argument("--namespace", help="Explicit namespace; no ambient/default target")
    result.add_argument("--timeout", type=int, default=15, help="Per-command timeout, 1-30 seconds")
    result.add_argument("--format", choices=["markdown", "json"], default="markdown")
    result.add_argument("--validate-catalog", action="store_true", help="Check declarations/coverage only; no probes")
    return result


def requirement_status(checks: list[dict]) -> str:
    statuses = {
        "unverified" if check["access"]["status"] == "verified" and check["runtime_requirements"]
        else check["access"]["status"] for check in checks
    }
    if "verified" in statuses:
        return "verified"
    if "unverified" in statuses:
        return "unverified"
    return "blocked"


def diagnose(root: Path, catalog: dict, options, probes=None, which=shutil.which, skill_dirs=None) -> dict:
    probes = probes or Probes(root, options)
    skill_dirs = skill_dirs or discover_skills(root, options.skills_dir)
    all_tools = KNOWN_TOOLS | {tool for c in catalog["capabilities"].values() for tool in c["tools"]}
    installed = {tool: bool(which(tool)) for tool in sorted(all_tools)}
    cache: dict[str, dict] = {}

    def capability(name: str) -> dict:
        if name not in cache:
            spec = catalog["capabilities"][name]
            missing = [tool for tool in spec["tools"] if not installed[tool]]
            access = Check("missing", "required-tool-not-found") if missing else probes.check(spec["probe"])
            cache[name] = {
                "id": name, "tools": {tool: installed[tool] for tool in spec["tools"]},
                "access": asdict(access), "permission": spec["permission"], "owner": spec["owner"],
                "remediation": spec["remediation"], "execution_approval": spec["approval"],
                "runtime_requirements": spec["runtime"],
            }
        return cache[name]

    rows = []
    selected = options.skill or sorted(catalog["skills"])
    for name in selected:
        spec = catalog["skills"][name]
        profiles = [options.profile] if options.profile else list(spec["profiles"])
        if options.skill and len(profiles) > 1:
            raise CatalogError(f"{name} needs --profile: {', '.join(profiles)}")
        hints = tool_mentions(root, skill_dirs[name], all_tools)
        declared = {
            tool for reqs in spec["profiles"].values() for req in reqs
            for cap in (req if isinstance(req, list) else [req])
            for tool in catalog["capabilities"][cap]["tools"]
        }
        source_hash = hashlib.sha256()
        for source in spec["sources"]:
            source_hash.update(source.encode())
            source_hash.update((root / source).read_bytes())
        for profile in profiles:
            if profile not in spec["profiles"]:
                raise CatalogError(f"Unknown profile for {name}: {profile}")
            requirements = []
            for req in spec["profiles"][profile]:
                alternatives = [capability(cap) for cap in (req if isinstance(req, list) else [req])]
                requirements.append({"status": requirement_status(alternatives), "any_of": alternatives})
            states = {r["status"] for r in requirements}
            status = "blocked" if "blocked" in states else "unverified" if "unverified" in states else "verified"
            candidates = sorted(hints.keys() - declared)
            if candidates and status == "verified":
                status = "unverified"
            rows.append({
                "skill": name, "profile": profile, "status": status, "requirements": requirements,
                "sources": spec["sources"], "source_digest": source_hash.hexdigest(),
                "tool_mentions": hints, "undeclared_tool_hints": candidates,
                "tool_hint_presence": {tool: installed[tool] for tool in hints},
            })
    return {
        "schema_version": 1, "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "current-process tools and selected operator identities; not a colleague's readiness",
        "limitations": [
            "Tool discovery does not execute/version-check tools or validate target-runtime dependencies.",
            "Declarations plus inline-code hints are not exhaustive dependency discovery; hints require review.",
            "Verified prerequisites are not business-action tests, approval, or a guarantee of workflow success.",
            "No skill command, login flow, credential copy, sudo/SSH fallback, grant, message or invitation is executed.",
        ],
        "live_families": sorted(set(options.live)),
        "summary": {
            "skills": len(selected), "profiles": len(rows),
            **{status: sum(row["status"] == status for row in rows)
               for status in ("verified", "blocked", "unverified")},
        },
        "results": rows,
    }


def markdown(report: dict) -> str:
    lines = ["# Skills Doctor", "", report["scope"], "", f"Checked at: {report['checked_at']}",
             "", f"Summary: {json.dumps(report['summary'])}", ""]
    for note in report["limitations"]:
        lines.append(f"- {note}")
    for row in report["results"]:
        lines.extend(["", f"## {row['skill']} / {row['profile']}: {row['status'].upper()}", "",
                      "| Requirement (OR within a row) | Tools | Evidence | Needed permission | Unblock owner / action |",
                      "|---|---|---|---|---|"])
        for req in row["requirements"]:
            alternatives = req["any_of"]
            names = " OR ".join(c["id"] for c in alternatives)
            tools, evidence, permissions, remedies = [], [], [], []
            for cap in alternatives:
                tools.append(cap["id"] + ": " + ", ".join(
                    f"{tool} ({'found' if present else 'MISSING'})" for tool, present in cap["tools"].items())
                    if cap["tools"] else cap["id"] + ": agent/runtime check (not a PATH executable)")
                evidence.append(f"{cap['id']}: {cap['access']['status']} ({cap['access']['reason']})"
                                + (f"; identity fingerprint: {cap['access']['identity']}"
                                   if cap["access"]["identity"] else ""))
                permissions.append(cap["permission"])
                remedies.append(f"{cap['owner']}: {cap['remediation']} Approval: {cap['execution_approval']}")
                if cap["runtime_requirements"]:
                    remedies.append("Unverified runtime: " + "; ".join(cap["runtime_requirements"]))
            cells = [names, "; ".join(tools), "; ".join(evidence), "; ".join(permissions), "; ".join(remedies)]
            lines.append("| " + " | ".join(cell.replace("|", "\\|").replace("\n", " ") for cell in cells) + " |")
        lines.extend(["", "Evidence sources: " + ", ".join(f"`{p}`" for p in row["sources"])])
        if row["undeclared_tool_hints"]:
            lines.append("Additional documentation hints to review (not proven requirements): "
                         + ", ".join(f"{tool} ({'found' if row['tool_hint_presence'][tool] else 'not found'})"
                                     for tool in row["undeclared_tool_hints"]))
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    argparser = parser()
    options = argparser.parse_args(argv)
    if not 1 <= options.timeout <= 30:
        argparser.error("--timeout must be 1-30")
    if options.live and (not options.skill or options.validate_catalog):
        argparser.error("--live requires an explicitly selected --skill; catalog validation is offline")
    if (options.live or options.validate_catalog) and not options.catalog:
        argparser.error("--live and --validate-catalog require a target-local --catalog")
    if options.github_org and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", options.github_org):
        argparser.error("Invalid GitHub organization slug")
    if options.aws_account and not re.fullmatch(r"\d{12}", options.aws_account):
        argparser.error("AWS account must have 12 digits")
    if options.gitlab_host and not re.fullmatch(r"[A-Za-z0-9.-]+", options.gitlab_host):
        argparser.error("Expected GitLab host must not include credentials, paths or a port")
    try:
        root = options.repo_root.resolve()
        if not root.is_dir():
            raise CatalogError("Target repository does not exist")
        skill_dirs = discover_skills(root, options.skills_dir)
        catalog = (load_catalog(root, root / options.catalog, skill_dirs) if options.catalog
                   else unreviewed_catalog(root, skill_dirs))
        if options.validate_catalog:
            print(json.dumps({"catalog": "valid", "skills": len(catalog["skills"]),
                              "capabilities": len(catalog["capabilities"])}))
            return 0
        unknown = set(options.skill or []) - catalog["skills"].keys()
        if unknown:
            raise CatalogError("Unknown skills: " + ", ".join(sorted(unknown)))
        report = diagnose(root, catalog, options, skill_dirs=skill_dirs)
        report["catalog_mode"] = "curated" if options.catalog else "unreviewed-inventory"
    except CatalogError as error:
        print(f"skills-doctor: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2) if options.format == "json" else markdown(report), end="\n")
    return 2 if report["summary"]["blocked"] else 3 if report["summary"]["unverified"] else 0
