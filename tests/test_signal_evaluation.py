from __future__ import annotations

from airlab_fraud_agentic_ai.evaluation.signal_metrics import evaluate_signal_candidates


def test_signal_evaluation_returns_metrics() -> None:
    evaluations = evaluate_signal_candidates(
        [
            {
                "signal_name": "new_device_high_value_new_payee_velocity",
                "description": "test",
            }
        ]
    )
    assert evaluations[0]["fraud_lift"] >= 2.0
    assert evaluations[0]["recommendation"] == "candidate_for_human_review"
