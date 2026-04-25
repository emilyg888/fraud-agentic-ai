from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(autouse=True)
def isolated_runtime(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    runs_dir = tmp_path / "runs"
    reports_dir = tmp_path / "reports"
    registry_dir = tmp_path / "signal_registry"
    runs_dir.mkdir()
    reports_dir.mkdir()
    registry_dir.mkdir()

    for status in ("candidate", "approved", "rejected"):
        (registry_dir / f"{status}_signals.yaml").write_text("[]\n", encoding="utf-8")

    monkeypatch.setenv("AIRLAB_RUNS_DIR", str(runs_dir))
    monkeypatch.setenv("AIRLAB_REPORTS_DIR", str(reports_dir))
    monkeypatch.setenv("AIRLAB_REGISTRY_DIR", str(registry_dir))
