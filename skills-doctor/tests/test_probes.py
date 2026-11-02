from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from skills_doctor.cli import diagnose, markdown, parser
from skills_doctor.probes import Probes, Result


def options(*args):
    return parser().parse_args(args)


def response(data):
    return Result(0, json.dumps(data))


def fixture(root):
    entry = root / ".claude/skills/example/SKILL.md"
    entry.parent.mkdir(parents=True)
    entry.write_text("# Example\nUse `lark-cli`.", encoding="utf-8")
    return {
        "version": 1,
        "capabilities": {
            "lark": {
                "tools": ["lark-cli"], "permission": "Fixture scope", "owner": "Operator",
                "remediation": "Obtain scoped access", "probe": "lark-contact",
                "approval": "No business action", "runtime": [],
            }
        },
        "skills": {"example": {
            "sources": [".claude/skills/example/SKILL.md"],
            "profiles": {"default": ["lark"]},
        }},
    }


class Recorder:
    def __init__(self, *results):
        self.results = list(results)
        self.calls = []
        self.envs = []

    def __call__(self, argv, root, timeout, env):
        self.calls.append(argv)
        self.envs.append(env.copy())
        if not self.results:
            raise AssertionError("Unexpected command: " + repr(argv))
        return self.results.pop(0)


class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.catalog = fixture(self.root)

    def run_probe(self, name, *results, args=()):
        recorder = Recorder(*results)
        probe = Probes(self.root, options("--live", name.split("-")[0], *args), recorder)
        return probe.check(name), recorder

    def test_unselected_family_has_no_commands(self):
        recorder = Recorder()
        probe = Probes(self.root, options(), recorder)
        self.assertEqual(probe.check("github-org").status, "unverified")
        self.assertEqual(recorder.calls, [])

    def test_live_family_without_target_has_no_commands(self):
        for name in ("github-org", "gitlab-admin", "aws-identity", "kube-read"):
            check, recorder = self.run_probe(name)
            self.assertEqual(check.status, "unverified")
            self.assertEqual(recorder.calls, [])

    def lark(self, **overrides):
        user = {
            "status": "ready", "tokenStatus": "valid", "verified": True, "openId": "fixture-user",
            "scope": "contact:user:search im:message im:message.send_as_user "
                     "im:chat:read im:chat.members:read im:chat.members:write_only",
        }
        user.update(overrides)
        return response({"verified": True, "identities": {"user": user, "bot": {"status": "ready"}}})

    def test_lark_checks_user_not_bot_and_caches_auth_probe(self):
        recorder = Recorder(self.lark())
        probe = Probes(self.root, options("--live", "lark"), recorder)
        for name in ("lark-contact", "lark-send", "lark-groups"):
            self.assertEqual(probe.check(name).status, "verified")
        self.assertEqual(len(recorder.calls), 1)
        for payload in (self.lark(status="not_ready"), self.lark(scope="contact:user:search")):
            check, _ = self.run_probe("lark-send", payload)
            self.assertEqual(check.status, "denied")

    def test_lark_shape_and_unverified_user_are_not_green(self):
        for payload in (response({"identities": []}), self.lark(scope=[]), self.lark(verified=False)):
            self.assertEqual(self.run_probe("lark-contact", payload)[0].status, "unverified")

    def gitlab(self, *tail):
        return self.run_probe(
            "gitlab-admin", Result(0, "git@example.invalid:group/repo.git"),
            response({"id": 1, "state": "active", "web_url": "https://example.invalid/u"}),
            *tail, args=("--gitlab-host", "example.invalid"),
        )

    def test_gitlab_instance_admin_is_not_group_developer(self):
        check, recorder = self.gitlab(Result(1, stderr="HTTP 403 Forbidden fixture-only"))
        self.assertEqual(check.status, "denied")
        self.assertEqual(recorder.calls[-1], ["glab", "api", "application/settings"])
        self.assertEqual(len(recorder.calls), 3)

    def test_gitlab_admin_needs_own_active_write_scoped_token(self):
        token = {"active": True, "revoked": False, "user_id": 1, "scopes": ["api"]}
        self.assertEqual(self.gitlab(response({}), response(token))[0].status, "verified")
        for changes in ({"scopes": ["read_api"]}, {"scopes": "api"}, {"user_id": 2}, {"revoked": True}):
            self.assertEqual(self.gitlab(response({}), response(dict(token, **changes)))[0].status, "unverified")

    def test_gitlab_wrong_target_stops_before_admin_query(self):
        check, recorder = self.run_probe("gitlab-admin", Result(0, "git@other.invalid:g/r"),
                                         args=("--gitlab-host", "example.invalid"))
        self.assertEqual(check.status, "denied")
        self.assertEqual(len(recorder.calls), 1)

    def github(self, member=None, headers="x-oauth-scopes: admin:org"):
        if member is None:
            member = {"organization": {"login": "example"}, "state": "active", "role": "admin"}
        return self.run_probe(
            "github-org", response({"id": 1}), response(member),
            Result(0, "HTTP/2.0 200 OK\n" + headers + "\n\n{}"),
            args=("--github-org", "example"),
        )

    def test_github_owner_and_write_scope(self):
        self.assertEqual(self.github()[0].status, "verified")
        self.assertEqual(self.github(headers="x-oauth-scopes: read:org")[0].status, "unverified")
        self.assertEqual(self.github(headers="server: fixture")[0].status, "unverified")
        for role, org in (("member", "example"), ("admin", "other")):
            member = {"organization": {"login": org}, "state": "active", "role": role}
            self.assertEqual(self.github(member)[0].status, "denied")
        self.assertEqual(self.github({"organization": None})[0].status, "unverified")

    def test_aws_sts_never_proves_iam_or_billing_permissions(self):
        args = ("--aws-profile", "fixture", "--aws-account", "000000000000")
        with patch.dict(os.environ, AWS_ACCESS_KEY_ID="fixture-not-secret", AWS_SECRET_ACCESS_KEY="fixture-not-secret"):
            check, recorder = self.run_probe(
                "aws-identity", response({"Account": "000000000000", "Arn": "fixture-identity"}), args=args)
        self.assertEqual(check.status, "unverified")
        self.assertTrue(check.identity)
        self.assertNotIn("AWS_ACCESS_KEY_ID", recorder.envs[0])
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", recorder.envs[0])
        self.assertIn("--profile", recorder.calls[0])
        wrong, _ = self.run_probe("aws-identity", response({"Account": "111111111111"}), args=args)
        self.assertEqual(wrong.status, "denied")

    def test_kube_denial_in_zero_exit_is_still_denied(self):
        args = ("--kube-context", "fixture", "--namespace", "example")
        check, recorder = self.run_probe("kube-read", Result(0, "no\n"), args=args)
        self.assertEqual(check.status, "denied")
        self.assertEqual(len(recorder.calls), 1)

    def test_kube_only_reviews_exact_actions_and_correct_log_subresource(self):
        args = ("--kube-context", "fixture", "--namespace", "example")
        for name in ("kube-read", "kube-write"):
            check, recorder = self.run_probe(name, *[Result(0, "yes\n")] * 3, args=args)
            self.assertEqual(check.status, "verified")
            for command in recorder.calls:
                self.assertEqual(command[:5], [
                    "kubectl", "--context=fixture", "--namespace=example", "--request-timeout=5s", "auth"])
                self.assertEqual(command[5], "can-i")
            if name == "kube-read":
                self.assertEqual(recorder.calls[-1][-3:], ["get", "pods", "--subresource=log"])

    def test_malformed_json_and_raw_errors_stay_redacted(self):
        secret = "FIXTURE-SENSITIVE-MARKER"
        for result in (Result(0, secret), Result(1, secret, "403 " + secret),
                       Result(-1, secret, secret, "timeout"), response([secret])):
            check, _ = self.run_probe("lark-contact", result)
            self.assertNotEqual(check.status, "verified")
            self.assertNotIn(secret, repr(check))
        args = options("--skill", "example", "--profile", "default", "--live", "lark")
        probes = Probes(self.root, args, Recorder(Result(1, secret, "403 " + secret)))
        report = diagnose(self.root, self.catalog, args, probes, which=lambda _: "/fake")
        self.assertNotIn(secret, json.dumps(report) + markdown(report))

    def test_structured_lark_authorization_error_is_known_denial(self):
        failure = Result(1, stderr=json.dumps({"error": {"type": "authorization", "subtype": "missing_scope"}}))
        self.assertEqual(self.run_probe("lark-contact", failure)[0].status, "denied")
