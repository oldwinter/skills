"""Windows fixture checks. Artifacts are retained in a newly created temp folder."""

import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import scan_storage

SCANNER = Path(__file__).with_name("scan_storage.py")


@unittest.skipUnless(os.name == "nt", "Windows filesystem tests")
class ScanTests(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp(prefix="windows-storage-audit-test-"))
        self.root = self.base / "source"
        self.root.mkdir()

    def invoke(self, *extra, output=None, roots=None):
        target = output or self.base / "report"
        command = [sys.executable, str(SCANNER), "--output", str(target), "--large-mib", "0"]
        for root in roots or [self.root]:
            command.extend(["--root", str(root)])
        result = subprocess.run(command + list(extra), capture_output=True, text=True, encoding="utf-8", errors="replace")
        return result, target

    def summary(self, output):
        return json.loads((output / "summary.json").read_text(encoding="utf-8"))

    def test_hardlinks_count_once_and_output_is_excluded(self):
        data = self.root / "data.bin"
        data.write_bytes(b"x" * 8192)
        os.link(data, self.root / "alias.bin")
        result, output = self.invoke(output=self.root / "report")
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = self.summary(output)
        totals = summary["roots"][str(self.root)]
        self.assertEqual(totals["files"], 2)
        self.assertEqual(totals["logical"], 16384)
        self.assertEqual(totals["allocated_entries"], 2 * totals["allocated_unique"])
        self.assertEqual(summary["counts"]["duplicate_hardlinks"], 1)
        self.assertEqual(data.read_bytes(), b"x" * 8192)

    def test_existing_report_is_not_overwritten(self):
        output = self.base / "report"
        output.mkdir()
        marker = output / "summary.json"
        marker.write_text("keep me", encoding="utf-8")
        result, _ = self.invoke(output=output)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep me")
        self.assertEqual(list(output.iterdir()), [marker])

    def test_overlapping_roots_are_rejected_before_output(self):
        child = self.root / "child"
        child.mkdir()
        result, output = self.invoke(roots=[self.root, child])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def make_junction(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "keep.bin").write_bytes(b"outside data")
        junction = self.root / "redirect"
        result = subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(outside)], capture_output=True)
        if result.returncode:
            self.skipTest("Junction creation not available")
        return junction, outside

    def test_junction_target_is_not_traversed(self):
        _, outside = self.make_junction()
        result, output = self.invoke()
        self.assertEqual(result.returncode, 2, result.stderr)
        summary = self.summary(output)
        self.assertTrue(summary["partial"])
        self.assertEqual(summary["counts"]["files"], 0)
        self.assertEqual(summary["counts"]["skipped_entries"], 1)
        self.assertEqual((outside / "keep.bin").read_bytes(), b"outside data")

    def test_redirected_root_and_output_ancestor_are_rejected(self):
        junction, _ = self.make_junction()
        result, output = self.invoke(roots=[junction])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())
        result, output = self.invoke(output=junction / "report")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def test_sparse_file_does_not_count_its_logical_length_as_allocation(self):
        data = self.root / "sparse.bin"
        data.touch()
        flag = subprocess.run(["fsutil.exe", "sparse", "setflag", str(data)], capture_output=True)
        if flag.returncode:
            self.skipTest("Sparse files unavailable on this volume")
        with data.open("r+b") as stream:
            stream.truncate(64 * 1024 * 1024)
        result, output = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        totals = self.summary(output)["roots"][str(self.root)]
        self.assertEqual(totals["logical"], 64 * 1024 * 1024)
        self.assertLess(totals["allocated_unique"], 1024 * 1024)
        self.assertEqual(totals["estimated_bytes"], 0)

    def test_compressed_allocation_and_unicode_paths(self):
        data = self.root / "資料 [one].bin"
        data.write_bytes(b"compressible\n" * 100000)
        flag = subprocess.run(["compact.exe", "/C", str(data)], capture_output=True)
        if flag.returncode:
            self.skipTest("NTFS compression unavailable on this volume")
        result, output = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        totals = self.summary(output)["roots"][str(self.root)]
        self.assertLess(totals["allocated_unique"], totals["logical"] / 2)
        with (output / "large-files.csv").open(encoding="utf-8-sig", newline="") as stream:
            self.assertEqual(next(csv.DictReader(stream))["path"], str(data))

    def test_allocation_failure_keeps_explicit_estimate_and_partial_exit(self):
        (self.root / "data.bin").write_bytes(b"a" * 8192)
        output = self.base / "report"
        argv = [str(SCANNER), "--root", str(self.root), "--output", str(output)]
        with mock.patch.object(scan_storage.WindowsAllocation, "read", side_effect=PermissionError(5, "fixture denied")), mock.patch.object(sys, "argv", argv):
            self.assertEqual(scan_storage.main(), 2)
        totals = self.summary(output)["roots"][str(self.root)]
        self.assertEqual(totals["logical"], 8192)
        self.assertEqual(totals["estimated_bytes"], 8192)
        self.assertIn("allocation-estimated-from-logical", (output / "errors.csv").read_text(encoding="utf-8-sig"))

    def test_unreadable_directory_preserves_readable_totals(self):
        (self.root / "visible.bin").write_bytes(b"a" * 8192)
        blocked = self.root / "blocked"
        blocked.mkdir()
        (blocked / "unreadable.bin").write_bytes(b"b" * 4096)
        output = self.base / "report"
        argv = [str(SCANNER), "--root", str(self.root), "--output", str(output)]
        original = os.scandir

        def enumerate_with_denial(path):
            if os.fspath(path) == scan_storage.io_path(str(blocked)):
                raise PermissionError(5, "fixture denied")
            return original(path)

        with mock.patch.object(scan_storage.os, "scandir", side_effect=enumerate_with_denial), mock.patch.object(sys, "argv", argv):
            self.assertEqual(scan_storage.main(), 2)
        summary = self.summary(output)
        self.assertEqual(summary["roots"][str(self.root)]["logical"], 8192)
        self.assertEqual(summary["counts"]["errors"], 1)
        self.assertIn(str(blocked), (output / "errors.csv").read_text(encoding="utf-8-sig"))

    def test_deep_long_path_is_enumerated(self):
        deep = self.root
        for number in range(12):
            deep = deep / ("directory-with-long-name-" + str(number))
        os.makedirs(scan_storage.io_path(str(deep)))
        with open(scan_storage.io_path(str(deep / "data.bin")), "wb") as stream:
            stream.write(b"data")
        result, output = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.summary(output)["counts"]["files"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
