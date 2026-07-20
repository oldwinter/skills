from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEW_WORKFLOW = ROOT / "scripts" / "new_workflow.py"
VERIFY_WORKFLOW = ROOT / "scripts" / "verify_workflow.py"
COLLECT_RESULTS = ROOT / "scripts" / "collect_results.py"
CODEX_WORKFLOW = ROOT / "scripts" / "codex_workflow.py"
EXAMPLE_WORKFLOW = ROOT / "examples" / "inspect-project.workflow.js"


class WorkflowScriptTests(unittest.TestCase):
    def run_script(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=check,
        )

    def test_new_workflow_scaffolds_auditable_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Smoke Workflow", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())

            self.assertTrue((workflow_dir / "plan.md").is_file())
            self.assertTrue((workflow_dir / "state.json").is_file())
            self.assertTrue((workflow_dir / "orchestration.md").is_file())
            self.assertTrue((workflow_dir / "integration.md").is_file())
            self.assertTrue((workflow_dir / "final-report.md").is_file())
            self.assertEqual(len(list((workflow_dir / "packets").glob("*.md"))), 3)

            state = json.loads((workflow_dir / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["slug"], "smoke-workflow")
            self.assertIn("budgets", state)
            self.assertEqual(len(state["packets"]), 3)

    def test_verify_fails_without_results_then_passes_with_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Verify Me", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())

            failed = self.run_script(str(VERIFY_WORKFLOW), str(workflow_dir), check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("No non-empty result files", failed.stdout)

            passed_empty = self.run_script(
                str(VERIFY_WORKFLOW),
                str(workflow_dir),
                "--allow-empty-results",
            )
            self.assertIn("Workflow verification passed", passed_empty.stdout)

            (workflow_dir / "results" / "01-discovery.md").write_text(
                "# Discovery\n\nAccepted: context mapped.\nVerification: inspected files.\n",
                encoding="utf-8",
            )
            passed = self.run_script(str(VERIFY_WORKFLOW), str(workflow_dir))
            self.assertIn("Workflow verification passed", passed.stdout)
            self.assertIn("Results: 1", passed.stdout)

    def test_collect_results_writes_integration_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Collect Me", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())
            result_file = workflow_dir / "results" / "01-discovery.md"
            result_file.write_text(
                "# Discovery\n\n- Accepted: repo layout found.\n- Risk: install command unverified.\n",
                encoding="utf-8",
            )
            output_file = workflow_dir / "integration.md"

            collected = self.run_script(
                str(COLLECT_RESULTS),
                str(workflow_dir),
                "--output",
                str(output_file),
            )

            self.assertEqual(collected.stdout, "")
            text = output_file.read_text(encoding="utf-8")
            self.assertIn("Integration Checklist", text)
            self.assertIn("Accepted: repo layout found", text)
            self.assertIn("Risk: install command unverified", text)

    def test_collect_results_groups_structured_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Collect Sections", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())
            (workflow_dir / "results" / "01-discovery.md").write_text(
                "# Discovery\n\n"
                "## Accepted\n\n"
                "- Repo layout mapped.\n\n"
                "## Risks\n\n"
                "- Install smoke not run.\n\n"
                "## Verification\n\n"
                "- `python3 -m unittest`: passed.\n",
                encoding="utf-8",
            )

            collected = self.run_script(str(COLLECT_RESULTS), str(workflow_dir))

            self.assertIn("## Accepted", collected.stdout)
            self.assertIn("- 01 Discovery: Repo layout mapped.", collected.stdout)
            self.assertIn("## Risks", collected.stdout)
            self.assertIn("- 01 Discovery: Install smoke not run.", collected.stdout)
            self.assertIn("## Verification Evidence", collected.stdout)
            self.assertIn("- 01 Discovery: `python3 -m unittest`: passed.", collected.stdout)

    def test_collect_results_groups_colon_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Collect Colon Sections", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())
            (workflow_dir / "results" / "01-discovery.md").write_text(
                "# Discovery\n\n"
                "Accepted:\n"
                "- Repo layout mapped.\n"
                "Risk:\n"
                "- Install smoke not run.\n"
                "Verification:\n"
                "- Tests passed.\n",
                encoding="utf-8",
            )

            collected = self.run_script(str(COLLECT_RESULTS), str(workflow_dir))

            self.assertIn("- 01 Discovery: Repo layout mapped.", collected.stdout)
            self.assertIn("- 01 Discovery: Install smoke not run.", collected.stdout)
            self.assertIn("- 01 Discovery: Tests passed.", collected.stdout)

    def test_codex_workflow_adapter_parses_and_writes_packets(self) -> None:
        parsed = self.run_script(str(CODEX_WORKFLOW), str(EXAMPLE_WORKFLOW), "--json")
        data = json.loads(parsed.stdout)
        self.assertEqual(data["meta"]["name"], "inspect_project")
        self.assertEqual(data["phases"], ["Scan", "Analyze"])
        self.assertEqual([agent["label"] for agent in data["agents"]], ["repo inventory", "module summary"])

        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(CODEX_WORKFLOW), str(EXAMPLE_WORKFLOW), "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())
            self.assertTrue((workflow_dir / "packets" / "01-repo-inventory.md").is_file())
            self.assertTrue((workflow_dir / "packets" / "02-module-summary.md").is_file())
            self.assertIn("repo inventory", (workflow_dir / "state.json").read_text(encoding="utf-8"))

    def test_codex_workflow_adapter_rejects_nondeterminism(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            script = Path(temp_dir) / "bad.workflow.js"
            script.write_text(
                "export const meta = { name: 'bad', description: 'bad' }\n"
                "phase('Bad')\n"
                "await agent('now ' + Date.now(), { label: 'bad' })\n",
                encoding="utf-8",
            )
            failed = self.run_script(str(CODEX_WORKFLOW), str(script), "--json", check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("must be deterministic", failed.stderr)

    def test_codex_workflow_adapter_preserves_keywords_inside_strings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            script = Path(temp_dir) / "keywords.workflow.js"
            script.write_text(
                "export const meta = {\n"
                "  name: 'keywords',\n"
                "  description: 'Keep true false null as words',\n"
                "  enabled: true,\n"
                "  missing: null\n"
                "}\n"
                "phase(`Scan`)\n"
                "await agent(`Report true false null literally.`, { label: `literal keywords` })\n",
                encoding="utf-8",
            )
            parsed = self.run_script(str(CODEX_WORKFLOW), str(script), "--json")
            data = json.loads(parsed.stdout)

            self.assertEqual(data["meta"]["description"], "Keep true false null as words")
            self.assertIs(data["meta"]["enabled"], True)
            self.assertIsNone(data["meta"]["missing"])
            self.assertEqual(data["phases"], ["Scan"])
            self.assertEqual(data["agents"][0]["prompt"], "Report true false null literally.")

    def test_codex_workflow_adapter_rejects_template_interpolation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            script = Path(temp_dir) / "interpolation.workflow.js"
            script.write_text(
                "export const meta = { name: 'bad_template', description: 'bad template' }\n"
                "await agent(`Inspect ${cwd}`, { label: 'bad' })\n",
                encoding="utf-8",
            )
            failed = self.run_script(str(CODEX_WORKFLOW), str(script), "--json", check=False)

            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("template interpolation is not allowed", failed.stderr)

    def test_codex_workflow_adapter_rejects_template_interpolation_in_phase_and_label(self) -> None:
        cases = [
            ("phase(`Scan ${cwd}`)\nawait agent('Inspect.', { label: 'ok' })\n", "phase titles"),
            ("await agent('Inspect.', { label: `bad ${cwd}` })\n", "agent labels"),
        ]
        for body, expected_context in cases:
            with self.subTest(expected_context=expected_context):
                with tempfile.TemporaryDirectory() as temp_dir:
                    script = Path(temp_dir) / "bad-template.workflow.js"
                    script.write_text(
                        "export const meta = { name: 'bad_template', description: 'bad template' }\n" + body,
                        encoding="utf-8",
                    )
                    failed = self.run_script(str(CODEX_WORKFLOW), str(script), "--json", check=False)

                    self.assertNotEqual(failed.returncode, 0)
                    self.assertIn(expected_context, failed.stderr)
                    self.assertIn("template interpolation is not allowed", failed.stderr)

    def test_codex_workflow_adapter_requires_force_to_overwrite_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first = self.run_script(str(CODEX_WORKFLOW), str(EXAMPLE_WORKFLOW), "--root", temp_dir)
            workflow_dir = Path(first.stdout.strip())
            marker = workflow_dir / "results" / "keep.md"
            marker.write_text("do not overwrite\n", encoding="utf-8")

            failed = self.run_script(str(CODEX_WORKFLOW), str(EXAMPLE_WORKFLOW), "--root", temp_dir, check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("pass --force to overwrite", failed.stderr)
            self.assertTrue(marker.is_file())

            forced = self.run_script(str(CODEX_WORKFLOW), str(EXAMPLE_WORKFLOW), "--root", temp_dir, "--force")
            self.assertEqual(Path(forced.stdout.strip()), workflow_dir)
            self.assertFalse(marker.exists())

    def test_codex_workflow_adapter_refuses_to_force_non_artifact_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "inspect-project"
            target.mkdir()
            keep = target / "keep.txt"
            keep.write_text("not a workflow artifact\n", encoding="utf-8")

            failed = self.run_script(str(CODEX_WORKFLOW), str(EXAMPLE_WORKFLOW), "--root", temp_dir, "--force", check=False)

            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("refusing to overwrite non-workflow directory", failed.stderr)
            self.assertTrue(keep.is_file())

    def test_verify_can_require_every_packet_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Strict Verify", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())
            (workflow_dir / "results" / "01-discovery.md").write_text("done\n", encoding="utf-8")

            failed = self.run_script(str(VERIFY_WORKFLOW), str(workflow_dir), "--require-all-results", check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("Missing result for packet: 02-execution", failed.stdout)
            self.assertIn("Missing result for packet: 03-verification", failed.stdout)

    def test_verify_state_schema_catches_slug_and_duplicate_packet_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Schema Verify", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())
            state_path = workflow_dir / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["slug"] = "wrong-slug"
            state["packets"][1]["id"] = state["packets"][0]["id"]
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (workflow_dir / "results" / "01-discovery.md").write_text("done\n", encoding="utf-8")

            failed = self.run_script(str(VERIFY_WORKFLOW), str(workflow_dir), check=False)

            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("state.slug must match workflow directory name", failed.stdout)
            self.assertIn("Duplicate packet id: 01-discovery", failed.stdout)

    def test_verify_state_schema_catches_missing_packet_file_and_result_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Result Mismatch", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())
            (workflow_dir / "packets" / "02-execution.md").unlink()
            (workflow_dir / "results" / "02-custom.md").write_text("done\n", encoding="utf-8")
            state_path = workflow_dir / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["packets"][1]["status"] = "complete"
            state["packets"][1]["result"] = "results/02-custom.md"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            failed = self.run_script(str(VERIFY_WORKFLOW), str(workflow_dir), "--require-all-results", check=False)

            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("Missing packet file for state packet: 02-execution", failed.stdout)
            self.assertIn("Result file stem must match packet id for 02-execution", failed.stdout)
            self.assertIn("Missing result for packet: 02-execution", failed.stdout)

    def test_verify_state_schema_catches_bad_status_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(str(NEW_WORKFLOW), "Bad Status", "--root", temp_dir)
            workflow_dir = Path(result.stdout.strip())
            state_path = workflow_dir / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["status"] = "almost_done"
            state["packets"][0]["status"] = "maybe"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (workflow_dir / "results" / "01-discovery.md").write_text("done\n", encoding="utf-8")

            failed = self.run_script(str(VERIFY_WORKFLOW), str(workflow_dir), check=False)

            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("state.status has invalid value: almost_done", failed.stdout)
            self.assertIn("packet 01-discovery status has invalid value: maybe", failed.stdout)


if __name__ == "__main__":
    unittest.main()
