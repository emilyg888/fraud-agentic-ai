from __future__ import annotations

from airlab_fraud_agentic_ai.evaluation.signal_metrics import evaluate_signal_candidates


def evaluate_signals(signal_candidates: list[dict]) -> list[dict]:
    return evaluate_signal_candidates(signal_candidates)
