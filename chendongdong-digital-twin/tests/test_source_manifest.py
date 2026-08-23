import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_source_manifest.py"
EXPECTED_WINDOW = {
    "start": "2026-02-10",
    "end": "2026-08-10",
    "timezone": "Asia/Shanghai",
}


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

    def test_accepts_partial_refresh_with_classified_aggregate_counts(self) -> None:
        manifest = {
            "profile_subject": "self",
            "window": {
                "start": "2026-02-10",
                "end": "2026-08-10",
                "timezone": "Asia/Shanghai",
            },
            "raw_content_stored": False,
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
            "latest_refresh": {
                "run_at": "2026-08-23T08:00:00+08:00",
                "status": "partial",
                "raw_content_stored": False,
                "window": {
                    "start": "2026-08-16T08:00:00+08:00",
                    "end": "2026-08-23T08:00:00+08:00",
                    "timezone": "Asia/Shanghai",
                },
                "inventory": {
                    "visible_tasks": 10,
                    "manual_codex_tasks": 4,
                    "chatgpt_conversations": 1,
                    "automation_runs": 4,
                    "delegated_tasks": 1,
                    "read_errors": 0,
                },
                "coverage": {
                    "visible_hosts": 4,
                    "archived_pagination_complete_to_window": True,
                    "active_list_limit": 50,
                    "active_list_saturated": True,
                    "active_list_reached_window_start": False,
                    "promotion_policy": "reinforce_or_tentative_only",
                },
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

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_complete_refresh_with_capped_active_coverage(self) -> None:
        manifest = {
            "profile_subject": "self",
            "window": {
                "start": "2026-02-10",
                "end": "2026-08-10",
                "timezone": "Asia/Shanghai",
            },
            "raw_content_stored": False,
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
            "latest_refresh": {
                "run_at": "2026-08-23T08:00:00+08:00",
                "status": "complete",
                "raw_content_stored": False,
                "window": {
                    "start": "2026-08-16T08:00:00+08:00",
                    "end": "2026-08-23T08:00:00+08:00",
                    "timezone": "Asia/Shanghai",
                },
                "inventory": {
                    "visible_tasks": 4,
                    "manual_codex_tasks": 1,
                    "chatgpt_conversations": 0,
                    "automation_runs": 3,
                    "delegated_tasks": 0,
                    "read_errors": 0,
                },
                "coverage": {
                    "visible_hosts": 4,
                    "archived_pagination_complete_to_window": True,
                    "active_list_limit": 50,
                    "active_list_saturated": True,
                    "active_list_reached_window_start": False,
                    "promotion_policy": "full_model_update",
                },
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
        self.assertIn("saturated active listing cannot be complete", result.stdout)

    def test_rejects_invalid_refresh_time_and_missing_coverage_contract(self) -> None:
        manifest = {
            "profile_subject": "self",
            "window": EXPECTED_WINDOW,
            "raw_content_stored": False,
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
            "latest_refresh": {
                "run_at": "2026-08-23T09:00:00+08:00",
                "status": "partial",
                "raw_content_stored": False,
                "window": {
                    "start": "not-a-date",
                    "end": "2026-08-23T08:00:00+08:00",
                    "timezone": "Asia/Shanghai",
                },
                "inventory": {
                    "visible_tasks": 1,
                    "manual_codex_tasks": 1,
                    "chatgpt_conversations": 0,
                    "automation_runs": 0,
                    "delegated_tasks": 0,
                    "read_errors": 0,
                },
                "coverage": {},
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
        errors = json.loads(result.stdout)["errors"]
        self.assertIn("latest_refresh window start must be a valid ISO-8601 datetime", errors)
        self.assertIn("latest_refresh run_at must equal the half-open window end", errors)
        self.assertTrue(any("coverage field" in error for error in errors))

    def test_rejects_non_shanghai_offset_and_non_weekly_window(self) -> None:
        manifest = {
            "profile_subject": "self",
            "window": EXPECTED_WINDOW,
            "raw_content_stored": False,
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
            "latest_refresh": {
                "run_at": "2026-08-23T08:00:00+00:00",
                "status": "partial",
                "raw_content_stored": False,
                "window": {
                    "start": "2026-08-23T07:00:00+00:00",
                    "end": "2026-08-23T08:00:00+00:00",
                    "timezone": "Asia/Shanghai",
                },
                "inventory": {
                    "visible_tasks": 1,
                    "manual_codex_tasks": 1,
                    "chatgpt_conversations": 0,
                    "automation_runs": 0,
                    "delegated_tasks": 0,
                    "read_errors": 0,
                },
                "coverage": {
                    "visible_hosts": 1,
                    "archived_pagination_complete_to_window": True,
                    "active_list_limit": 50,
                    "active_list_saturated": True,
                    "active_list_reached_window_start": False,
                    "promotion_policy": "reinforce_or_tentative_only",
                },
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
        errors = json.loads(result.stdout)["errors"]
        self.assertIn("latest_refresh window start offset must match Asia/Shanghai", errors)
        self.assertIn("latest_refresh window end offset must match Asia/Shanghai", errors)
        self.assertIn("latest_refresh run_at offset must match Asia/Shanghai", errors)
        self.assertIn("latest_refresh half-open window must span exactly seven days", errors)

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
