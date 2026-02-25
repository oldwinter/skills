from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("skills_profiles_tests", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load test module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TEST_PATH = (
    Path(__file__).resolve().parent
    / "system-skills"
    / "sync-skills-manager"
    / "scripts"
    / "test_skills_profiles.py"
)
_TEST_MODULE = _load(TEST_PATH)


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str):  # noqa: D401
    return loader.loadTestsFromModule(_TEST_MODULE)
