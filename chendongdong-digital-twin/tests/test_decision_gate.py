import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
GATE = SKILL_ROOT / "scripts" / "decision_gate.py"
FIXTURES = SKILL_ROOT / "tests" / "fixtures"


class DecisionGateTests(unittest.TestCase):
    def run_gate(self, fixture: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GATE), "--input", str(FIXTURES / fixture)],
            capture_output=True,
            text=True,
            check=False,
        )

    def run_payload(self, payload: dict[str, object]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            request_path = Path(tmp_dir) / "request.json"
            request_path.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(GATE), "--input", str(request_path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_allows_reversible_precedented_high_confidence_work(self) -> None:
        result = self.run_gate("low-risk.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "act")
        self.assertGreaterEqual(payload["confidence"], 0.85)
        self.assertTrue(payload["reason"])

    def test_drafts_outbound_message_without_current_send_authorization(self) -> None:
        result = self.run_gate("outbound-reply.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "draft")
        self.assertIn("send authorization", payload["reason"])

    def test_escalates_high_risk_action_despite_high_confidence(self) -> None:
        result = self.run_gate("high-risk.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("production", payload["reason"])
        self.assertIn("destructive", payload["reason"])

    def test_escalates_malformed_request_instead_of_crashing(self) -> None:
        result = self.run_gate("malformed.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("missing required fields", payload["reason"])

    def test_escalates_uncertain_unscoped_unprecedented_irreversible_work(self) -> None:
        result = self.run_gate("uncertain.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("confidence", payload["reason"])
        self.assertIn("scope", payload["reason"])
        self.assertIn("precedent", payload["reason"])
        self.assertIn("reversible", payload["reason"])

    def test_escalates_invalid_json_instead_of_crashing(self) -> None:
        result = self.run_gate("invalid-json.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("invalid JSON", payload["reason"])

    def test_escalates_non_object_json_instead_of_crashing(self) -> None:
        result = self.run_gate("non-object.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("object", payload["reason"])

    def test_escalates_invalid_field_types_instead_of_crashing(self) -> None:
        result = self.run_gate("invalid-types.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("invalid fields", payload["reason"])
        self.assertIn("confidence", payload["reason"])

    def test_escalates_unknown_risk_tags(self) -> None:
        result = self.run_gate("unknown-risk.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("unknown risk tags", payload["reason"])

    def test_escalates_explicit_ambiguity(self) -> None:
        result = self.run_gate("ambiguous.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("ambiguity", payload["reason"])

    def test_escalates_out_of_range_confidence(self) -> None:
        result = self.run_gate("out-of-range.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("confidence", payload["reason"])

    def test_escalates_out_of_range_precedent_counts(self) -> None:
        for fixture in ("negative-precedent.json", "oversized-precedent.json"):
            with self.subTest(fixture=fixture):
                result = self.run_gate(fixture)

                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["action"], "escalate")
                self.assertIn("precedent_count", payload["reason"])

    def test_fails_closed_for_undeclared_consequential_action_semantics(self) -> None:
        base = {
            "action_category": "local_reversible",
            "authorization_scope": "current task",
            "evidence_refs": ["current-request"],
            "reversible": True,
            "scope_confirmed": True,
            "target": "declared local target",
            "precedent_count": 3,
            "confidence": 0.99,
            "explicit_send_authorization": False,
            "ambiguity_present": False,
            "risk_tags": [],
        }
        action_types = (
            "send_email",
            "impersonate_user",
            "production_mutation",
            "delete_data",
        )
        for action_type in action_types:
            with self.subTest(action_type=action_type):
                payload = self.run_payload({**base, "action_type": action_type})
                self.assertNotEqual(payload["action"], "act")

    def test_escalates_unknown_safe_looking_action_type(self) -> None:
        payload = self.run_payload(
            {
                "action_category": "local_reversible",
                "action_type": "do_the_thing",
                "authorization_scope": "current task",
                "evidence_refs": ["current-request"],
                "reversible": True,
                "scope_confirmed": True,
                "target": "local file",
                "precedent_count": 3,
                "confidence": 0.99,
                "explicit_send_authorization": False,
                "ambiguity_present": False,
                "risk_tags": [],
            }
        )
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("allowlist", payload["reason"])

    def test_escalates_non_string_action_category_without_crashing(self) -> None:
        payload = self.run_payload(
            {
                "action_category": ["local_reversible"],
                "action_type": "local_code_edit",
                "authorization_scope": "current task",
                "evidence_refs": ["current-request"],
                "reversible": True,
                "scope_confirmed": True,
                "target": "local file",
                "precedent_count": 3,
                "confidence": 0.99,
                "explicit_send_authorization": False,
                "ambiguity_present": False,
                "risk_tags": [],
            }
        )
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("action_category", payload["reason"])

    def test_unknown_outbound_types_never_act_even_with_claimed_authorization(self) -> None:
        for action_type in ("send", "send_message", "email", "publish"):
            with self.subTest(action_type=action_type):
                payload = self.run_payload(
                    {
                        "action_category": "outbound",
                        "action_type": action_type,
                        "authorization_scope": "current request",
                        "evidence_refs": ["current-request"],
                        "reversible": True,
                        "scope_confirmed": True,
                        "target": "named colleague",
                        "precedent_count": 3,
                        "confidence": 0.99,
                        "explicit_send_authorization": True,
                        "ambiguity_present": False,
                        "risk_tags": [],
                    }
                )
                self.assertEqual(payload["action"], "escalate")

    def test_known_outbound_with_claimed_authorization_requires_live_review(self) -> None:
        payload = self.run_payload(
            {
                "action_category": "outbound",
                "action_type": "outbound_colleague_message",
                "authorization_scope": "current request",
                "evidence_refs": ["current-request"],
                "reversible": True,
                "scope_confirmed": True,
                "target": "named colleague",
                "precedent_count": 3,
                "confidence": 0.99,
                "explicit_send_authorization": True,
                "ambiguity_present": False,
                "risk_tags": [],
            }
        )
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("live human authorization", payload["reason"])

    def test_target_and_scope_semantics_can_escalate_local_action(self) -> None:
        payload = self.run_payload(
            {
                "action_category": "local_reversible",
                "action_type": "local_code_edit",
                "authorization_scope": "not actually granted",
                "evidence_refs": ["current-request"],
                "reversible": True,
                "scope_confirmed": True,
                "target": "production database / secret store",
                "precedent_count": 3,
                "confidence": 0.99,
                "explicit_send_authorization": False,
                "ambiguity_present": False,
                "risk_tags": [],
            }
        )
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("permissions", payload["reason"])
        self.assertIn("production", payload["reason"])
        self.assertIn("secrets", payload["reason"])

    def test_rejects_unresolvable_evidence_references(self) -> None:
        payload = self.run_payload(
            {
                "action_category": "local_reversible",
                "action_type": "local_code_edit",
                "authorization_scope": "current task",
                "evidence_refs": ["does-not-exist", "reference:../SKILL.md"],
                "reversible": True,
                "scope_confirmed": True,
                "target": "local file",
                "precedent_count": 3,
                "confidence": 0.99,
                "explicit_send_authorization": False,
                "ambiguity_present": False,
                "risk_tags": [],
            }
        )
        self.assertEqual(payload["action"], "escalate")
        self.assertIn("evidence_refs", payload["reason"])

    def test_local_mutation_requires_bounded_target_scope_and_reference(self) -> None:
        base = {
            "action_category": "local_reversible",
            "action_type": "local_code_edit",
            "authorization_scope": "current task",
            "evidence_refs": ["current-request", "reference:profile.md"],
            "reversible": True,
            "scope_confirmed": True,
            "target": "references/profile.md",
            "precedent_count": 3,
            "confidence": 0.99,
            "explicit_send_authorization": False,
            "ambiguity_present": False,
            "risk_tags": [],
        }
        adversarial = (
            {**base, "authorization_scope": "read only", "target": "local file"},
            {**base, "target": "send email to colleague"},
            {**base, "target": "drop table customer_records"},
            {**base, "target": "truncate customer table"},
            {**base, "target": "../outside.txt"},
            {**base, "evidence_refs": ["current-request"]},
        )
        for payload in adversarial:
            with self.subTest(payload=payload):
                result = self.run_payload(payload)
                self.assertEqual(result["action"], "escalate")

    def test_invalid_path_characters_fail_closed_without_crashing(self) -> None:
        base = {
            "action_category": "local_reversible",
            "action_type": "local_code_edit",
            "authorization_scope": "current task",
            "evidence_refs": ["current-request", "reference:profile.md"],
            "reversible": True,
            "scope_confirmed": True,
            "target": "references/profile.md",
            "precedent_count": 3,
            "confidence": 0.99,
            "explicit_send_authorization": False,
            "ambiguity_present": False,
            "risk_tags": [],
        }
        for payload in (
            {**base, "target": "\u0000"},
            {**base, "evidence_refs": ["reference:\u0000"]},
        ):
            with self.subTest(payload=payload):
                result = self.run_payload(payload)
                self.assertEqual(result["action"], "escalate")

    def test_protects_twin_gate_and_policy_files_from_autonomous_edits(self) -> None:
        for target in (
            "scripts/decision_gate.py",
            "scripts/privacy_check.py",
            "references/autonomy-policy.json",
        ):
            with self.subTest(target=target):
                payload = self.run_payload(
                    {
                        "action_category": "local_reversible",
                        "action_type": "local_code_edit",
                        "authorization_scope": "current task",
                        "evidence_refs": ["current-request", "reference:profile.md"],
                        "reversible": True,
                        "scope_confirmed": True,
                        "target": target,
                        "precedent_count": 3,
                        "confidence": 0.99,
                        "explicit_send_authorization": False,
                        "ambiguity_present": False,
                        "risk_tags": [],
                    }
                )
                self.assertEqual(payload["action"], "escalate")
                self.assertIn("safety gate or policy", payload["reason"])

    def test_read_only_action_rejects_mutating_target_language(self) -> None:
        for target in (
            "write references/profile.md",
            "edit references/profile.md",
            "mutate data",
            "create a file",
        ):
            with self.subTest(target=target):
                payload = self.run_payload(
                    {
                        "action_category": "read_only",
                        "action_type": "read_only_analysis",
                        "authorization_scope": "read only",
                        "evidence_refs": ["current-request"],
                        "reversible": True,
                        "scope_confirmed": True,
                        "target": target,
                        "precedent_count": 3,
                        "confidence": 0.99,
                        "explicit_send_authorization": False,
                        "ambiguity_present": False,
                        "risk_tags": [],
                    }
                )
                self.assertEqual(payload["action"], "escalate")


if __name__ == "__main__":
    unittest.main()
