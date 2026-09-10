import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_canvas.py"
BASE = {
    "nodes": [
        {"id": "a", "type": "text", "x": 0, "y": 0, "width": 320, "height": 180, "text": "Input"},
        {"id": "b", "type": "text", "x": 440, "y": 0, "width": 320, "height": 180, "text": "Output"},
    ],
    "edges": [{"id": "e", "fromNode": "a", "toNode": "b"}],
}


class CanvasCheckTests(unittest.TestCase):
    def test_validation_results_and_read_only_behavior(self):
        cases = [("valid", copy.deepcopy(BASE), True)]
        for name, key, value in (
            ("duplicate-id", "id", "a"),
            ("negative-size", "width", -1),
            ("nonfinite-coordinate", "x", float("nan")),
            ("oversized-coordinate", "x", 10 ** 400),
            ("invalid-type", "type", []),
        ):
            data = copy.deepcopy(BASE)
            data["nodes"][1][key] = value
            cases.append((name, data, False))
        for name, key, value in (
            ("dangling-edge", "toNode", "missing"),
            ("invalid-side", "fromSide", []),
        ):
            data = copy.deepcopy(BASE)
            data["edges"][0][key] = value
            cases.append((name, data, False))
        for name, fields, expected in (
            ("missing-link", {"text": "[[missing.canvas]]"}, False),
            ("outside-vault", {"type": "file", "file": "../outside.canvas"}, False),
            ("nul-reference", {"type": "file", "file": "bad\0.canvas"}, False),
            ("embed-cycle", {"type": "file", "file": "check.canvas"}, False),
            ("navigation-cycle", {"text": "[[check.canvas|Return]]"}, True),
        ):
            data = copy.deepcopy(BASE)
            data["nodes"][0].update(fields)
            cases.append((name, data, expected))
        for value in (float("nan"), float("inf"), float("-inf")):
            data = copy.deepcopy(BASE)
            data["metadata"] = {"nested": [value]}
            cases.append((f"nonstandard-json-{value}", data, False))
        for name, data, expected in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                canvas = root / "check.canvas"
                original = json.dumps(data).encode()
                canvas.write_bytes(original)
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "--vault", directory, "check.canvas"],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0 if expected else 1, result.stderr)
                self.assertEqual(json.loads(result.stdout)["valid"], expected)
                self.assertEqual(canvas.read_bytes(), original)
                self.assertEqual(list(root.iterdir()), [canvas])

    def test_nested_file_reference_with_return_navigation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "maps").mkdir()
            parent = copy.deepcopy(BASE)
            parent["nodes"][0].update(type="file", file="maps/child.canvas")
            child = copy.deepcopy(BASE)
            child["nodes"][0]["text"] = "[[maps/parent.canvas|Return]]"
            (root / "maps" / "parent.canvas").write_text(json.dumps(parent))
            (root / "maps" / "child.canvas").write_text(json.dumps(child))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--vault", directory, "maps/parent.canvas"],
                capture_output=True, text=True, check=True,
            )
            report = json.loads(result.stdout)
            self.assertTrue(report["valid"])
            self.assertEqual(report["canvases"], 2)
            self.assertEqual(report["references"], 2)


if __name__ == "__main__":
    unittest.main()
