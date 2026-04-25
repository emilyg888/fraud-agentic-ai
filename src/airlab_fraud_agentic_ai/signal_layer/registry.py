from __future__ import annotations

from pathlib import Path

import yaml

from airlab_fraud_agentic_ai.config import get_settings


class SignalRegistry:
    def __init__(self, registry_dir: Path | None = None) -> None:
        self.registry_dir = registry_dir or get_settings().registry_dir
        self.registry_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, status: str) -> Path:
        return self.registry_dir / f"{status}_signals.yaml"

    def _read(self, status: str) -> list[dict]:
        path = self._path(status)
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or []
        return list(data)

    def _write(self, status: str, items: list[dict]) -> None:
        path = self._path(status)
        with path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(items, handle, sort_keys=False)

    def list(self, status: str | None = None) -> list[dict]:
        if status:
            return self._read(status)
        records: list[dict] = []
        for key in ("candidate", "approved", "rejected"):
            records.extend(self._read(key))
        return records

    def register_candidates(self, entries: list[dict]) -> None:
        current = self._read("candidate")
        ids = {entry["signal"]["signal_id"] for entry in current}
        for entry in entries:
            if entry["signal"]["signal_id"] not in ids:
                current.append(entry)
        self._write("candidate", current)

    def _move(self, signal_id: str, target_status: str, reviewer: str, comments: str) -> dict:
        candidates = self._read("candidate")
        remaining: list[dict] = []
        moved: dict | None = None
        for entry in candidates:
            if entry["signal"]["signal_id"] == signal_id:
                entry["status"] = target_status
                entry["reviewer"] = reviewer
                entry["comments"] = comments
                moved = entry
            else:
                remaining.append(entry)
        if moved is None:
            raise KeyError(f"Unknown signal_id: {signal_id}")
        self._write("candidate", remaining)
        target_entries = self._read(target_status)
        target_entries.append(moved)
        self._write(target_status, target_entries)
        return moved

    def approve(self, signal_id: str, reviewer: str, comments: str = "") -> dict:
        return self._move(signal_id=signal_id, target_status="approved", reviewer=reviewer, comments=comments)

    def reject(self, signal_id: str, reviewer: str, comments: str = "") -> dict:
        return self._move(signal_id=signal_id, target_status="rejected", reviewer=reviewer, comments=comments)
