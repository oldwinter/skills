import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER = SKILL_ROOT / "scripts" / "privacy_check.py"


class PrivacyContractTests(unittest.TestCase):
    def test_installed_skill_has_fail_closed_privacy_contract(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(SKILL_ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["outbound_default"], "draft")
        self.assertEqual(payload["irreversible_default"], "escalate")
        self.assertEqual(payload["identity_claim"], "simulation")
        self.assertFalse(payload["raw_content_stored"])
        self.assertEqual(payload["findings"], [])

    def test_detects_raw_fields_and_credential_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            references = root / "references"
            references.mkdir()
            (references / "autonomy-policy.json").write_text(
                json.dumps(
                    {
                        "identity_claim": "simulation",
                        "outbound_default": "draft",
                        "irreversible_default": "escalate",
                        "human_override": True,
                        "raw_content_stored": False,
                    }
                ),
                encoding="utf-8",
            )
            (references / "unsafe.json").write_text(
                json.dumps(
                    {
                        "raw_content": "private colleague message",
                        "access_token": "glpat-example-not-a-real-token",
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(root)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        findings = json.loads(result.stdout)["findings"]
        self.assertTrue(any("forbidden field: raw_content" in item for item in findings))
        self.assertTrue(any("credential pattern" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
