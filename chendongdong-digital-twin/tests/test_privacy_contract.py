import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER = SKILL_ROOT / "scripts" / "privacy_check.py"
EXPECTED_POLICY = {
    "human_override": True,
    "identity_claim": "simulation",
    "incomplete_refresh_policy": "tentative_only",
    "irreversible_default": "escalate",
    "one_off_approval_is_precedent": False,
    "outbound_default": "draft",
    "raw_content_stored": False,
    "scheduled_refresh_external_actions": "escalate",
}


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

    def test_detects_raw_markdown_and_profile_pii(self) -> None:
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
            (references / "unsafe.md").write_text(
                'Raw export: {"type": "userMessage"}\nContact: person@example.com\n',
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
        self.assertTrue(any("raw conversation pattern" in item for item in findings))
        self.assertTrue(any("email address" in item for item in findings))

    def test_rejects_unsafe_or_incomplete_autonomy_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            references = root / "references"
            references.mkdir()
            (references / "autonomy-policy.json").write_text(
                json.dumps(
                    {
                        "identity_claim": "person",
                        "outbound_default": "act",
                        "irreversible_default": "act",
                        "human_override": False,
                        "raw_content_stored": True,
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
        self.assertTrue(any("identity_claim" in item for item in findings))
        self.assertTrue(any("outbound_default" in item for item in findings))
        self.assertTrue(any("human_override" in item for item in findings))

    def test_detects_yaml_raw_fields_phone_id_and_home_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            references = root / "references"
            references.mkdir()
            (references / "autonomy-policy.json").write_text(
                json.dumps(EXPECTED_POLICY), encoding="utf-8"
            )
            (references / "unsafe.yaml").write_text(
                "raw_content: private transcript\n"
                "phone: 13800138000\n"
                "identity: 11010519491231002X\n"
                "path: /Users/example\n",
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
        self.assertTrue(any("raw conversation pattern" in item for item in findings))
        self.assertTrue(any("mobile number" in item for item in findings))
        self.assertTrue(any("identity number" in item for item in findings))
        self.assertTrue(any("absolute home path" in item for item in findings))

    def test_non_utf8_file_requires_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            references = root / "references"
            references.mkdir()
            (references / "autonomy-policy.json").write_text(
                json.dumps(EXPECTED_POLICY), encoding="utf-8"
            )
            (references / "binary.txt").write_bytes(b"\xff\xfeprivate")
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(root)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        findings = json.loads(result.stdout)["findings"]
        self.assertTrue(any("non-UTF-8" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
