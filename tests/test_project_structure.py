from __future__ import annotations

from pathlib import Path


def test_required_top_level_paths_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    expected = [
        "AGENTS.md",
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        "docs",
        "data",
        "knowledge",
        "signal_registry",
        "reports",
        "runs",
        "src",
        "streamlit_app",
        "tests",
    ]
    for relative in expected:
        assert (root / relative).exists(), relative
