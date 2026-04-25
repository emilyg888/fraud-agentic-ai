from __future__ import annotations

from airlab_fraud_agentic_ai.signal_layer.monitoring import get_signal_monitoring_summary
from airlab_fraud_agentic_ai.signal_layer.registry import SignalRegistry


def list_signal_registry(status: str | None = None) -> list[dict]:
    return SignalRegistry().list(status=status)


def register_candidate_signals(entries: list[dict]) -> None:
    SignalRegistry().register_candidates(entries)


def approve_signal(signal_id: str, reviewer: str, comments: str = "") -> dict:
    return SignalRegistry().approve(signal_id=signal_id, reviewer=reviewer, comments=comments)


def reject_signal(signal_id: str, reviewer: str, comments: str = "") -> dict:
    return SignalRegistry().reject(signal_id=signal_id, reviewer=reviewer, comments=comments)


def monitoring_summary() -> list[dict]:
    return get_signal_monitoring_summary()
