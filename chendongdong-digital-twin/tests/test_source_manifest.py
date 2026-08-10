import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_source_manifest.py"


class SourceManifestTests(unittest.TestCase):
    def test_accepts_aggregate_only_manifest(self) -> None:
        manifest = {
            "profile_subject": "self",
            "window": {
                "start": "2026-02-10",
                "end": "2026-08-10",
                "timezone": "Asia/Shanghai",
            },
            "raw_content_stored": False,
            "sources": {
                "notes": {"items_processed": 8649, "status": "processed"},
                "gitlab": {"items_processed": 120, "status": "processed"},
                "lark_im": {"items_processed": 5000, "status": "processed"},
            },
            "research_dimensions": {
                "writings": 1,
                "conversations": 1,
                "expression_dna": 1,
                "external_views": 1,
                "decisions": 1,
                "timeline": 1,
            },
            "excluded_sources": [],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "source-manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(manifest_path)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"ok": True, "errors": []})

    def test_rejects_manifest_that_stores_raw_content(self) -> None:
        manifest = {
            "profile_subject": "self",
            "window": {
                "start": "2026-02-10",
                "end": "2026-08-10",
                "timezone": "Asia/Shanghai",
            },
            "raw_content_stored": True,
            "sources": {
                "notes": {"items_processed": 1, "status": "processed"},
                "gitlab": {"items_processed": 1, "status": "processed"},
                "lark_im": {"items_processed": 1, "status": "processed"},
            },
            "research_dimensions": {
                "writings": 1,
                "conversations": 1,
                "expression_dna": 1,
                "external_views": 1,
                "decisions": 1,
                "timeline": 1,
            },
            "excluded_sources": [],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "source-manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(manifest_path)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("raw_content_stored must be false", result.stdout)

    def test_requires_window_sources_and_nonempty_research_dimensions(self) -> None:
        manifest = {
            "profile_subject": "self",
            "window": {"start": "2026-02-11", "end": "2026-08-10"},
            "raw_content_stored": False,
            "sources": {"notes": {"items_processed": 1, "status": "processed"}},
            "research_dimensions": {"writings": 0},
            "excluded_sources": [],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "source-manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(manifest_path)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        errors = json.loads(result.stdout)["errors"]
        self.assertIn("window must be 2026-02-10..2026-08-10 Asia/Shanghai", errors)
        self.assertIn("missing required source: gitlab", errors)
        self.assertIn("missing required source: lark_im", errors)
        self.assertIn("research dimension must be nonempty: writings", errors)
        self.assertIn("missing research dimension: timeline", errors)


if __name__ == "__main__":
    unittest.main()
