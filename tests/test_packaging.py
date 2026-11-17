"""Vercel's Python build reads pyproject.toml before requirements.txt: the
runtime dependencies must be identical in both, or production loses FastAPI."""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_dependencies_match():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["dependencies"]
    lines = [x.strip() for x in (ROOT / "requirements.txt").read_text().splitlines()]
    requirements = [x for x in lines if x and not x.startswith("#")]
    assert sorted(project) == sorted(requirements)
