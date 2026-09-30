"""Verify CI variable exports stay in the output file, out of logs."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("export_variables.sh").resolve()
SECRET = "SYNTHETIC_TOKEN=regression-test-secret"


class ExportVariablesTests(unittest.TestCase):
    def test_exports_without_logging_variables(self):
        scopes = (
            ([], "# Current Repo", []),
            (["--repo", "example/project"], "# Repo: example/project",
             ["-R", "example/project"]),
            (["--group", "example"], "# Group: example",
             ["--group", "example"]),
        )
        for scope, header, export_args in scopes:
            for filename in (None, "exported variables.env"):
                with self.subTest(scope=scope, filename=filename):
                    with tempfile.TemporaryDirectory(dir=SCRIPT.parent) as temp_dir:
                        workdir = Path(temp_dir)
                        glab = workdir / "glab"
                        glab.write_text(
                            "#!/bin/bash\n"
                            "printf '%s\\n' \"$@\" > \"$GLAB_ARGS_LOG\"\n"
                            f"printf '%s\\n' '{SECRET}'\n",
                            encoding="utf-8",
                        )
                        glab.chmod(0o700)
                        args_log = workdir / "glab-args.txt"
                        env = dict(os.environ,
                                   PATH=f"{workdir}{os.pathsep}{os.environ['PATH']}",
                                   GLAB_ARGS_LOG=str(args_log))
                        result = subprocess.run(
                            ["bash", str(SCRIPT), *scope,
                             *([filename] if filename else [])],
                            cwd=workdir, env=env, capture_output=True,
                            text=True, encoding="utf-8", timeout=10,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(
                            args_log.read_text(encoding="utf-8").splitlines(),
                            ["variable", "export", *export_args],
                        )
                        outputs = list(workdir.glob("*.env"))
                        self.assertEqual(len(outputs), 1)
                        output = outputs[0]
                        if filename:
                            self.assertEqual(output.name, filename)
                        else:
                            self.assertRegex(output.name, r"^variables_\d{8}_\d{6}\.env$")
                        contents = output.read_text(encoding="utf-8").splitlines()
                        self.assertEqual(contents[0], header)
                        self.assertTrue(contents[1].startswith("# Exported: "))
                        self.assertEqual(contents[2:], [SECRET])
                        self.assertNotIn(SECRET, result.stdout)
                        self.assertNotIn(SECRET, result.stderr)
                        self.assertIn(output.name, result.stdout)
                        self.assertIn("文件可能包含敏感信息", result.stdout)


if __name__ == "__main__":
    unittest.main()
