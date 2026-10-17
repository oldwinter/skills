"""Tests for scripts/count_words.py.

Run: python3 -m unittest discover -s longform-fiction/tests -q
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "count_words.py"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class CountWordsTests(unittest.TestCase):
    def test_mixed_chinese_and_latin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            chapter = Path(directory) / "chapter-01.md"
            chapter.write_text("你好世界 hello world", encoding="utf-8")
            result = run("--json", str(chapter))
            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads(result.stdout)["files"][0]
            self.assertEqual(row["cjk_chars"], 4)
            self.assertEqual(row["latin_words"], 2)
            self.assertEqual(row["count"], 6)

    def test_directory_total_and_skipped_suffixes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "chapter-01.md").write_text("甲乙丙", encoding="utf-8")
            (root / "chapter-02.txt").write_text("丁戊", encoding="utf-8")
            (root / "cover.png").write_bytes(b"not text")
            result = run("--json", directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["total"]["files"], 2)
            self.assertEqual(report["total"]["cjk_chars"], 5)
            self.assertEqual(report["total"]["count"], 5)

    def test_table_output_has_rows_and_total(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            chapter = Path(directory) / "chapter-01.md"
            chapter.write_text("hello there", encoding="utf-8")
            result = run(str(chapter))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("chapter-01.md", result.stdout)
            self.assertIn("TOTAL", result.stdout)

    def test_missing_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run(str(Path(directory) / "missing.md"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("count_words:", result.stderr)

    def test_empty_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run(directory)
            self.assertEqual(result.returncode, 2)
            self.assertIn("no manuscript files", result.stderr)


if __name__ == "__main__":
    unittest.main()
