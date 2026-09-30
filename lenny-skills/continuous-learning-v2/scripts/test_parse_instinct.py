"""Tests for parse_instinct_file() — verifies content after frontmatter is preserved."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = os.path.join(os.path.dirname(__file__), "instinct-cli.py")

# Load instinct-cli.py (hyphenated filename requires importlib)
_spec = importlib.util.spec_from_file_location("instinct_cli", SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
parse_instinct_file = _mod.parse_instinct_file


MULTI_SECTION = """\
---
id: instinct-a
trigger: "when coding"
confidence: 0.9
domain: general
---

## Action
Do thing A.

## Examples
- Example A1

---
id: instinct-b
trigger: "when testing"
confidence: 0.7
domain: testing
---

## Action
Do thing B.
"""


class ParseInstinctFileTest(unittest.TestCase):
    def test_multiple_instincts_preserve_content(self):
        result = parse_instinct_file(MULTI_SECTION)
        assert len(result) == 2
        assert "Do thing A." in result[0]["content"]
        assert "Example A1" in result[0]["content"]
        assert "Do thing B." in result[1]["content"]

    def test_single_instinct_preserves_content(self):
        content = """\
---
id: solo
trigger: "when reviewing"
confidence: 0.8
domain: review
---

## Action
Check for security issues.

## Evidence
Prevents vulnerabilities.
"""
        result = parse_instinct_file(content)
        assert len(result) == 1
        assert "Check for security issues." in result[0]["content"]
        assert "Prevents vulnerabilities." in result[0]["content"]

    def test_empty_content_no_error(self):
        content = """\
---
id: empty
trigger: "placeholder"
confidence: 0.5
domain: general
---
"""
        result = parse_instinct_file(content)
        assert len(result) == 1
        assert result[0]["content"] == ""


class ImportSideEffectsTest(unittest.TestCase):
    def test_import_creates_no_directories(self):
        """Importing instinct-cli.py must not touch the filesystem."""
        with tempfile.TemporaryDirectory() as tmp_home:
            env = dict(os.environ, HOME=tmp_home)
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "import importlib.util, sys; "
                    "s = importlib.util.spec_from_file_location('instinct_cli', sys.argv[1]); "
                    "m = importlib.util.module_from_spec(s); "
                    "s.loader.exec_module(m)",
                    SCRIPT,
                ],
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((Path(tmp_home) / ".claude").exists())


if __name__ == "__main__":
    unittest.main()
