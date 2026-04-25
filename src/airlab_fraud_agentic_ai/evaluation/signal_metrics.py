from __future__ import annotations

from airlab_fraud_agentic_ai.data.bb_adapter import BBDatasetAdapter


def evaluate_signal_candidates(signal_candidates: list[dict], adapter: BBDatasetAdapter | None = None) -> list[dict]:
    adapter = adapter or BBDatasetAdapter.create()
    history = adapter.historical_cases()
    total_cases = max(len(history), 1)
    evaluations: list[dict] = []

    for signal in signal_candidates:
        matching = history.loc[history["signal_name"] == signal["signal_name"]]
        confirmed_rate = float(matching["confirmed_fraud_flag"].mean()) if not matching.empty else 0.0
        coverage_rate = round(len(matching) / total_cases, 2)
        fraud_lift = round(1.0 + (confirmed_rate * 2.0), 2)
        evaluations.append(
            {
                "signal_name": signal["signal_name"],
                "coverage_rate": coverage_rate,
                "fraud_lift": fraud_lift,
                "confirmed_fraud_rate": round(confirmed_rate, 2),
                "false_positive_risk": "medium" if confirmed_rate < 0.75 else "low",
                "data_quality_status": "pass",
                "explainability_score": 4 if signal.get("description") else 1,
                "recommendation": "candidate_for_human_review" if fraud_lift >= 2.0 else "monitor",
            }
        )
    return evaluations
