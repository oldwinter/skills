"""find_gitops_root() discovery checks shared by the sync-env scripts."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compare_configs
import sync_images

MODULES = [compare_configs, sync_images]


class FindGitopsRootTests(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp(prefix="sync-env-test-")).resolve()
        self.repo = self.base / "simplex-gitops"
        (self.repo / "kubernetes" / "overlays").mkdir(parents=True)
        self.elsewhere = self.base / "elsewhere"
        self.elsewhere.mkdir()

        self._cwd = Path.cwd()
        self._saved = {k: os.environ.get(k) for k in ("SIMPLEX_GITOPS_ROOT", "HOME")}
        os.environ.pop("SIMPLEX_GITOPS_ROOT", None)
        os.chdir(self.elsewhere)

    def tearDown(self):
        os.chdir(self._cwd)
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_env_var_points_to_repo(self):
        os.environ["SIMPLEX_GITOPS_ROOT"] = str(self.repo)
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(module.find_gitops_root(), self.repo)

    def test_finds_repo_from_repo_root_cwd(self):
        os.chdir(self.repo)
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(module.find_gitops_root(), self.repo)

    def test_finds_repo_from_nested_cwd(self):
        nested = self.repo / "kubernetes" / "overlays" / "aws-ci"
        nested.mkdir()
        os.chdir(nested)
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(module.find_gitops_root(), self.repo)

    def test_no_hardcoded_home_fallback(self):
        legacy_dir = "-".join(["all", "code", "in", "mba"])
        trap = self.base / "fakehome" / "Code" / legacy_dir / "simplex-gitops"
        (trap / "kubernetes" / "overlays").mkdir(parents=True)
        os.environ["HOME"] = str(self.base / "fakehome")
        for module in MODULES:
            with self.subTest(module=module.__name__):
                with self.assertRaises(FileNotFoundError):
                    module.find_gitops_root()

    def test_missing_repo_raises(self):
        for module in MODULES:
            with self.subTest(module=module.__name__):
                with self.assertRaises(FileNotFoundError):
                    module.find_gitops_root()


if __name__ == "__main__":
    unittest.main()
