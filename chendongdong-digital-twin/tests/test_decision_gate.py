import json
import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
