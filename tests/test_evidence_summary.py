from __future__ import annotations

from airlab_fraud_agentic_ai.agents.evidence_summariser import summarise_evidence
from airlab_fraud_agentic_ai.dashboard.view_models import build_case_overview


def test_case_overview_marks_below_threshold_alerts_correctly() -> None:
    overview = build_case_overview(
        {
            "alert_id": "A-1002",
            "customer_id": "C-1002",
            "model_score": 0.67,
            "threshold": 0.70,
            "triggered_features": "payee_concentration_7d|velocity_24h",
            "analyst_request": "Investigate alert A-1002.",
        }
    )

    assert overview["threshold_status"] == "below_threshold"
    assert overview["threshold_summary"] == "Score 0.67 did not exceed threshold 0.70."


def test_evidence_summary_uses_threshold_comparison_instead_of_always_exceeded() -> None:
    summary = summarise_evidence(
        alert={
            "alert_id": "A-1002",
            "customer_id": "C-1002",
            "model_score": 0.67,
            "threshold": 0.70,
        },
        retrieved={
            "fraud_typologies": [{"title": "Scam Payment"}, {"title": "Mule Account"}],
            "policies": [],
        },
        case_data={
            "transaction_summary": {"transaction_count": 2},
            "new_payee_activity": {"new_payee_count": 1},
            "behavioural_summary": {"device_change_count": 0},
        },
    )

    assert "did not exceed threshold 0.70" in summary
    assert "Retrieved typologies: Scam Payment, Mule Account. Policies reviewed: none." in summary
