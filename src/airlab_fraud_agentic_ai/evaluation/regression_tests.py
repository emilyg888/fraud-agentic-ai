from __future__ import annotations

from collections import Counter

from airlab_fraud_agentic_ai.data.bb_adapter import BBDatasetAdapter
from airlab_fraud_agentic_ai.signal_layer.monitoring import get_signal_monitoring_summary
from airlab_fraud_agentic_ai.signal_layer.registry import SignalRegistry


def run_signal_regression_suite(
    entries: list[dict] | None = None,
    adapter: BBDatasetAdapter | None = None,
) -> dict:
    monitored = get_signal_monitoring_summary(entries=entries, adapter=adapter)
    status_counts = Counter(item["monitoring_status"] for item in monitored)

    if status_counts["failing"]:
        overall_status = "fail"
    elif status_counts["decaying"]:
        overall_status = "warning"
    else:
        overall_status = "pass"

    return {
        "overall_status": overall_status,
        "total_signals": len(monitored),
        "stable_count": status_counts["stable"],
        "decaying_count": status_counts["decaying"],
        "failing_count": status_counts["failing"],
        "checks": [
            {
                "signal_name": item["signal_name"],
                "monitoring_status": item["monitoring_status"],
                "decay_score": item["signal_decay_score"],
                "recommendation": item["next_review_recommendation"],
            }
            for item in monitored
        ],
        "proxy_note": "Regression output uses deterministic sample-data monitoring proxies only.",
    }


def run_registry_regression_suite(adapter: BBDatasetAdapter | None = None) -> dict:
    approved_entries = SignalRegistry().list("approved")
    return run_signal_regression_suite(entries=approved_entries, adapter=adapter)
