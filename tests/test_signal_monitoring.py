from __future__ import annotations

import pandas as pd

from airlab_fraud_agentic_ai.signal_layer.monitoring import build_monitoring_card, get_signal_monitoring_summary


class FakeAdapter:
    def __init__(self, history_rows: list[dict], quality_rows: list[dict]) -> None:
        self._history = pd.DataFrame(history_rows)
        self._features = pd.DataFrame(
            [
                {
                    "feature_name": "device_change_count_24h",
                    "source_table": "behavioural_events",
                },
                {
                    "feature_name": "new_payee_count_24h",
                    "source_table": "transactions",
                },
                {
                    "feature_name": "transaction_amount_zscore_24h",
                    "source_table": "transactions",
                },
                {
                    "feature_name": "synthetic_identity_score",
                    "source_table": "features",
                },
            ]
        )
        self._quality = pd.DataFrame(quality_rows)

    def historical_cases(self) -> pd.DataFrame:
        return self._history

    def features(self) -> pd.DataFrame:
        return self._features

    def data_quality(self) -> pd.DataFrame:
        return self._quality


def _entry(signal_name: str, false_positive_risk: str = "low", governance_status: str = "pass") -> dict:
    return {
        "status": "approved",
        "reviewer": "tester",
        "signal": {
            "signal_id": f"{signal_name}-1",
            "signal_name": signal_name,
            "case_type": "account_takeover",
            "source_features": [
                "device_change_count_24h",
                "new_payee_count_24h",
                "transaction_amount_zscore_24h",
            ],
        },
        "evaluation": {
            "false_positive_risk": false_positive_risk,
        },
        "governance": {
            "governance_status": governance_status,
        },
    }


def test_monitoring_marks_stable_signal() -> None:
    adapter = FakeAdapter(
        history_rows=[
            {"signal_name": "sig_stable", "confirmed_fraud_flag": True},
            {"signal_name": "other", "confirmed_fraud_flag": False},
            {"signal_name": "sig_stable", "confirmed_fraud_flag": True},
            {"signal_name": "other", "confirmed_fraud_flag": False},
            {"signal_name": "sig_stable", "confirmed_fraud_flag": True},
            {"signal_name": "other", "confirmed_fraud_flag": False},
        ],
        quality_rows=[
            {"dataset_name": "transactions", "freshness_hours": 2, "anomaly_count": 0, "status": "pass"},
            {"dataset_name": "behavioural_events", "freshness_hours": 2, "anomaly_count": 0, "status": "pass"},
            {"dataset_name": "features", "freshness_hours": 4, "anomaly_count": 0, "status": "pass"},
        ],
    )

    card = build_monitoring_card(_entry("sig_stable"), adapter=adapter)

    assert card["monitoring_status"] == "stable"
    assert card["next_review_recommendation"] == "continue monitoring"
    assert card["drift_proxy"] == "stable"


def test_monitoring_marks_decaying_signal() -> None:
    adapter = FakeAdapter(
        history_rows=[
            {"signal_name": "sig_decay", "confirmed_fraud_flag": True},
            {"signal_name": "sig_decay", "confirmed_fraud_flag": True},
            {"signal_name": "sig_decay", "confirmed_fraud_flag": True},
            {"signal_name": "other", "confirmed_fraud_flag": False},
            {"signal_name": "other", "confirmed_fraud_flag": False},
            {"signal_name": "other", "confirmed_fraud_flag": False},
        ],
        quality_rows=[
            {"dataset_name": "transactions", "freshness_hours": 2, "anomaly_count": 0, "status": "pass"},
            {"dataset_name": "behavioural_events", "freshness_hours": 2, "anomaly_count": 0, "status": "pass"},
            {"dataset_name": "features", "freshness_hours": 4, "anomaly_count": 0, "status": "pass"},
        ],
    )

    card = build_monitoring_card(_entry("sig_decay"), adapter=adapter)

    assert card["monitoring_status"] == "decaying"
    assert card["coverage_trend_proxy"] == "declining"
    assert card["next_review_recommendation"] == "review soon"


def test_monitoring_marks_failing_signal() -> None:
    adapter = FakeAdapter(
        history_rows=[
            {"signal_name": "sig_fail", "confirmed_fraud_flag": False},
            {"signal_name": "other", "confirmed_fraud_flag": False},
            {"signal_name": "sig_fail", "confirmed_fraud_flag": False},
            {"signal_name": "other", "confirmed_fraud_flag": False},
        ],
        quality_rows=[
            {"dataset_name": "transactions", "freshness_hours": 72, "anomaly_count": 1, "status": "fail"},
            {"dataset_name": "behavioural_events", "freshness_hours": 72, "anomaly_count": 1, "status": "fail"},
            {"dataset_name": "features", "freshness_hours": 72, "anomaly_count": 1, "status": "fail"},
        ],
    )

    card = build_monitoring_card(
        _entry("sig_fail", false_positive_risk="high", governance_status="fail"),
        adapter=adapter,
    )

    assert card["monitoring_status"] == "failing"
    assert card["drift_proxy"] == "elevated"
    assert card["next_review_recommendation"] == "revalidate immediately"


def test_monitoring_deduplicates_repeated_signal_entries() -> None:
    adapter = FakeAdapter(
        history_rows=[
            {"signal_name": "sig_stable", "confirmed_fraud_flag": True},
            {"signal_name": "other", "confirmed_fraud_flag": False},
        ],
        quality_rows=[
            {"dataset_name": "transactions", "freshness_hours": 2, "anomaly_count": 0, "status": "pass"},
            {"dataset_name": "behavioural_events", "freshness_hours": 2, "anomaly_count": 0, "status": "pass"},
            {"dataset_name": "features", "freshness_hours": 4, "anomaly_count": 0, "status": "pass"},
        ],
    )

    entries = [_entry("sig_stable"), _entry("sig_stable")]

    cards = get_signal_monitoring_summary(entries=entries, adapter=adapter)

    assert len(cards) == 1
