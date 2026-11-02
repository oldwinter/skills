from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

MAX_OUTPUT = 512_000


@dataclass(frozen=True)
class Result:
    code: int
    stdout: str = ""
    stderr: str = ""
    failure: str = ""


@dataclass(frozen=True)
class Check:
    status: str
    reason: str
    identity: str = ""


def run_command(argv: list[str], root: Path, timeout: int, env: dict[str, str]) -> Result:
    # Raw CLI responses can contain credentials. Never forward them to a report.
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        try:
            result = subprocess.run(
                argv, cwd=root, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                timeout=timeout, env=env, check=False,
            )
        except subprocess.TimeoutExpired:
            return Result(-1, failure="timeout")
        except OSError:
            return Result(-1, failure="cannot-execute")
        out.seek(0)
        err.seek(0)
        stdout, stderr = out.read(MAX_OUTPUT + 1), err.read(MAX_OUTPUT + 1)
    if len(stdout) > MAX_OUTPUT or len(stderr) > MAX_OUTPUT:
        return Result(-1, failure="output-limit")
    return Result(result.returncode, stdout.decode(errors="replace"), stderr.decode(errors="replace"))


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:12]


def hostname(value) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        return urlsplit(value).hostname
    except ValueError:
        return None


def failed(result: Result) -> Check:
    if result.failure:
        return Check("unverified", result.failure)
    denied = re.search(r"\b(401|403|AccessDenied|Unauthorized|Forbidden)\b", result.stderr, re.I)
    try:
        envelope = json.loads(result.stderr)
        error = envelope.get("error") if isinstance(envelope, dict) else None
        denied = denied or (isinstance(error, dict) and error.get("type") in ("authentication", "authorization"))
    except ValueError:
        pass
    return Check("denied" if denied else "unverified",
                 "authentication-or-authorization-rejected" if denied else "command-failed")


class Probes:
    def __init__(self, root: Path, options, runner=run_command):
        self.root, self.options, self.runner = root, options, runner
        self.cache: dict[tuple[str, ...], Result] = {}
        self.env = dict(os.environ)
        self.env.update(
            AWS_PAGER="", GH_PROMPT_DISABLED="1", GIT_TERMINAL_PROMPT="0",
            LARKSUITE_CLI_NO_UPDATE_NOTIFIER="1", LARKSUITE_CLI_NO_SKILLS_NOTIFIER="1",
        )
        if options.aws_profile:
            for key in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "AWS_SECURITY_TOKEN"):
                self.env.pop(key, None)

    def command(self, *argv: str) -> Result:
        key = tuple(argv)
        if key not in self.cache:
            self.cache[key] = self.runner(list(argv), self.root, self.options.timeout, self.env)
        return self.cache[key]

    def json_command(self, *argv: str) -> tuple[dict | None, Check | None]:
        result = self.command(*argv)
        if result.code:
            return None, failed(result)
        try:
            data = json.loads(result.stdout)
        except (ValueError, TypeError):
            return None, Check("unverified", "invalid-json-response")
        if not isinstance(data, dict):
            return None, Check("unverified", "unexpected-response-shape")
        return data, None

    def check(self, probe: str) -> Check:
        if probe == "local":
            return Check("verified", "local-tool-discovery-only")
        if probe == "manual":
            return Check("unverified", "requires-target-specific-access-review")
        family = probe.split("-")[0]
        if family not in self.options.live:
            return Check("unverified", "live-probe-not-selected")
        if family == "lark":
            return self.lark(probe)
        if family == "gitlab":
            return self.gitlab(probe)
        if family == "github":
            return self.github()
        if family == "aws":
            return self.aws()
        if family == "kube":
            return self.kube(probe)
        return Check("unverified", "unsupported-probe")

    def lark(self, probe: str) -> Check:
        data, error = self.json_command("lark-cli", "auth", "status", "--json", "--verify")
        if error:
            return error
        identities = data.get("identities")
        user = identities.get("user") if isinstance(identities, dict) else None
        if not isinstance(user, dict):
            return Check("unverified", "lark-user-response-shape-unrecognized")
        if user.get("status") != "ready" or user.get("tokenStatus") != "valid":
            return Check("denied", "lark-user-login-not-ready")
        if user.get("verified") is not True or not isinstance(user.get("openId"), str) or not user["openId"]:
            return Check("unverified", "lark-user-identity-not-verified")
        scope = user.get("scope")
        if not isinstance(scope, str):
            return Check("unverified", "lark-user-scopes-unrecognized")
        scopes = set(scope.split())
        required = {
            "lark-contact": {"contact:user:search"},
            "lark-send": {"im:message", "im:message.send_as_user"},
            "lark-groups": {"im:chat:read", "im:chat.members:read", "im:chat.members:write_only"},
        }[probe]
        identity = fingerprint(user["openId"])
        missing = sorted(required - scopes)
        if missing:
            return Check("denied", "missing-user-scopes: " + ", ".join(missing), identity)
        return Check("verified", "user-identity-and-scopes-verified; resource-access-separate", identity)

    def gitlab(self, probe: str) -> Check:
        expected = self.options.gitlab_host
        if not expected:
            return Check("unverified", "supply-expected-gitlab-host")
        remote = self.command("git", "remote", "get-url", "origin")
        if remote.code:
            return failed(remote)
        value = remote.stdout.strip()
        host = hostname(value) if "://" in value else value.split("@")[-1].split(":")[0]
        if host != expected:
            return Check("denied", "gitlab-repository-target-mismatch")
        user, error = self.json_command("glab", "api", "user")
        if error:
            return error
        if hostname(user.get("web_url")) != expected:
            return Check("denied", "gitlab-api-target-mismatch")
        if user.get("state") != "active" or type(user.get("id")) is not int:
            return Check("denied", "gitlab-user-not-active")
        identity = fingerprint(str(user["id"]) + "@" + expected)
        if probe == "gitlab-read":
            return Check("unverified", "identity-verified; project-role-and-token-scope-not-checked", identity)
        _, error = self.json_command("glab", "api", "application/settings")
        if error:
            return Check(error.status, "gitlab-admin-check: " + error.reason, identity)
        token, error = self.json_command("glab", "api", "personal_access_tokens/self")
        if error or token.get("active") is not True or token.get("revoked") is not False:
            return Check("unverified", "admin-read-verified; token-write-scope-unverified", identity)
        if type(token.get("user_id")) is not int or token["user_id"] != user["id"]:
            return Check("unverified", "admin-read-verified; token-owner-unverified", identity)
        if not isinstance(token.get("scopes"), list) or "api" not in token["scopes"]:
            return Check("unverified", "admin-read-verified; api-scope-not-proven", identity)
        return Check("verified", "admin-read-and-api-scope-verified; no-user-created", identity)

    def github(self) -> Check:
        org = self.options.github_org
        if not org:
            return Check("unverified", "supply-expected-github-organization")
        user, error = self.json_command("gh", "api", "--hostname", "github.com", "user")
        if error:
            return error
        if type(user.get("id")) is not int:
            return Check("unverified", "github-user-identity-missing")
        identity = fingerprint(str(user["id"]) + "@github")
        member, error = self.json_command(
            "gh", "api", "--hostname", "github.com", f"user/memberships/orgs/{org}"
        )
        if error:
            return Check(error.status, error.reason, identity)
        organization = member.get("organization")
        if not isinstance(organization, dict) or not isinstance(organization.get("login"), str):
            return Check("unverified", "github-membership-response-shape-unrecognized", identity)
        if organization["login"].lower() != org.lower():
            return Check("denied", "github-organization-mismatch", identity)
        if member.get("state") != "active" or member.get("role") != "admin":
            return Check("denied", "github-active-organization-owner-required", identity)
        response = self.command("gh", "api", "--hostname", "github.com", "--include", "user")
        if response.code:
            return Check("unverified", "organization-role-verified; token-scope-unverified", identity)
        headers = response.stdout.split("\r\n\r\n", 1)[0].split("\n\n", 1)[0]
        match = re.search(r"^x-oauth-scopes:\s*(.*)$", headers, re.I | re.M)
        scopes = {s.strip() for s in match.group(1).split(",")} if match else set()
        if "admin:org" not in scopes:
            return Check("unverified", "owner-role-verified; token-members-write-permission-unverified", identity)
        return Check("verified", "owner-role-and-org-write-scope-verified; no-invitation-sent", identity)

    def aws(self) -> Check:
        if not self.options.aws_profile or not self.options.aws_account:
            return Check("unverified", "supply-aws-profile-and-expected-account")
        data, error = self.json_command(
            "aws", "sts", "get-caller-identity", "--profile", self.options.aws_profile, "--output", "json"
        )
        if error:
            return error
        if data.get("Account") != self.options.aws_account:
            return Check("denied", "aws-account-mismatch")
        if not isinstance(data.get("Arn"), str) or not data["Arn"]:
            return Check("unverified", "aws-identity-missing")
        return Check("unverified", "account-and-identity-verified; action-permissions-not-tested",
                     fingerprint(data["Arn"]))

    def kube(self, probe: str) -> Check:
        context, namespace = self.options.kube_context, self.options.namespace
        if not context or not namespace:
            return Check("unverified", "supply-explicit-kube-context-and-namespace")
        checks = [("get", "pods"), ("list", "deployments.apps"), ("get", "pods", "--subresource=log")]
        if probe == "kube-write":
            checks = [("patch", "deployments.apps"), ("create", "configmaps"), ("patch", "configmaps")]
        for verb, resource, *flags in checks:
            result = self.command(
                "kubectl", f"--context={context}", f"--namespace={namespace}", "--request-timeout=5s",
                "auth", "can-i", verb, resource, *flags,
            )
            answer = result.stdout.strip()
            if answer == "no":
                return Check("denied", "kubernetes-rbac-denied: " + " ".join((verb, resource, *flags)))
            if result.code or answer != "yes":
                return Check("unverified", "kubernetes-authorization-check-inconclusive")
        return Check("verified", "listed-rbac-actions-allowed; admission-and-execution-approval-separate")
