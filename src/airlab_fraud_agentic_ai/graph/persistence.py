from __future__ import annotations

import json
from pathlib import Path

from airlab_fraud_agentic_ai.config import get_settings


def _runs_dir() -> Path:
    runs_dir = get_settings().runs_dir
    runs_dir.mkdir(parents=True, exist_ok=True)
    return runs_dir


def _reports_dir() -> Path:
    reports_dir = get_settings().reports_dir
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir


def _report_path(run_id: str) -> Path:
    return _reports_dir() / f"{run_id}.md"


def save_run_state(run_id: str, state: dict) -> Path:
    report = state.get("final_case_report", "")
    if report:
        report_path = _report_path(run_id)
        report_path.write_text(report, encoding="utf-8")
        state["report_path"] = str(report_path)

    path = _runs_dir() / f"{run_id}.json"
    state["run_trace_path"] = str(path)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
    return path


def load_run_state(run_id: str) -> dict:
    path = _runs_dir() / f"{run_id}.json"
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
