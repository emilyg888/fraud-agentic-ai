from __future__ import annotations

from math import ceil

from airlab_fraud_agentic_ai.data.bb_adapter import BBDatasetAdapter
from airlab_fraud_agentic_ai.signal_layer.registry import SignalRegistry


def _adapter(adapter: BBDatasetAdapter | None) -> BBDatasetAdapter:
    return adapter or BBDatasetAdapter.create()


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _chunk_frame(frame, parts: int) -> list:
    if len(frame) == 0:
        return [frame]
    chunk_size = max(1, ceil(len(frame) / parts))
    return [frame.iloc[index : index + chunk_size] for index in range(0, len(frame), chunk_size)]


def _history_metrics(signal_name: str, adapter: BBDatasetAdapter) -> dict:
    history = adapter.historical_cases().reset_index(drop=True)
    total_cases = max(len(history), 1)
    matching = history.loc[history["signal_name"] == signal_name]

    coverage_rate = round(len(matching) / total_cases, 2)
    confirmed_rate = float(matching["confirmed_fraud_flag"].astype(float).mean()) if not matching.empty else 0.0
    fraud_lift = round(1.0 + (confirmed_rate * 2.0), 2)

    coverage_series: list[float] = []
    fraud_lift_series: list[float] = []
    for window in _chunk_frame(history, parts=3):
        if window.empty:
            continue
        window_matching = window.loc[window["signal_name"] == signal_name]
        coverage_series.append(round(len(window_matching) / max(len(window), 1), 2))
        if window_matching.empty:
            fraud_lift_series.append(1.0)
        else:
            window_confirmed = float(window_matching["confirmed_fraud_flag"].astype(float).mean())
            fraud_lift_series.append(round(1.0 + (window_confirmed * 2.0), 2))

    if len(coverage_series) >= 2:
        delta = round(coverage_series[-1] - coverage_series[0], 2)
        if delta <= -0.15:
            coverage_trend = "declining"
        elif delta >= 0.15:
            coverage_trend = "rising"
        else:
            coverage_trend = "stable"
    else:
        coverage_trend = "stable"

    if len(fraud_lift_series) >= 2:
        fraud_delta = round(fraud_lift_series[-1] - fraud_lift_series[0], 2)
    else:
        fraud_delta = 0.0

    return {
        "coverage_rate": coverage_rate,
        "coverage_series": coverage_series,
        "coverage_trend_proxy": coverage_trend,
        "coverage_delta": delta if len(coverage_series) >= 2 else 0.0,
        "fraud_lift": fraud_lift,
        "fraud_lift_series": fraud_lift_series,
        "fraud_lift_delta": fraud_delta,
        "confirmed_fraud_rate": round(confirmed_rate, 2),
    }


def _source_quality_metrics(source_features: list[str], adapter: BBDatasetAdapter) -> dict:
    features = adapter.features()
    quality = adapter.data_quality()
    quality_by_dataset = {
        str(row["dataset_name"]): row
        for row in quality.to_dict(orient="records")
    }

    source_tables = sorted(
        {
            str(row["source_table"])
            for _, row in features.loc[features["feature_name"].isin(source_features)].iterrows()
        }
    )

    dataset_rows: list[dict] = []
    for table in source_tables or ["features"]:
        row = quality_by_dataset.get(table)
        if row is None:
            row = quality_by_dataset.get("features")
        if row is not None:
            dataset_rows.append(row)

    if not dataset_rows:
        return {
            "source_tables": source_tables or ["features"],
            "data_freshness_hours": 0,
            "dataset_status": "unknown",
            "anomaly_count": 0,
        }

    statuses = {str(row["status"]) for row in dataset_rows}
    if "fail" in statuses:
        dataset_status = "fail"
    elif "conditional_pass" in statuses:
        dataset_status = "conditional_pass"
    else:
        dataset_status = "pass"

    return {
        "source_tables": source_tables or ["features"],
        "data_freshness_hours": int(max(_safe_float(row["freshness_hours"]) for row in dataset_rows)),
        "dataset_status": dataset_status,
        "anomaly_count": int(sum(int(_safe_float(row["anomaly_count"])) for row in dataset_rows)),
    }


def build_monitoring_card(entry: dict, adapter: BBDatasetAdapter | None = None) -> dict:
    runtime_adapter = _adapter(adapter)
    evaluation = entry.get("evaluation", {})
    governance = entry.get("governance", {})
    signal = entry.get("signal", {})

    history_metrics = _history_metrics(signal.get("signal_name", ""), runtime_adapter)
    quality_metrics = _source_quality_metrics(signal.get("source_features", []), runtime_adapter)

    false_positive_proxy = evaluation.get("false_positive_risk", "unknown")
    governance_status = governance.get("governance_status", "unknown")

    decay_score = 0
    if history_metrics["coverage_trend_proxy"] == "declining":
        decay_score += 30
    elif history_metrics["coverage_trend_proxy"] == "rising":
        decay_score -= 10

    if history_metrics["fraud_lift"] < 2.0:
        decay_score += 25
    elif history_metrics["fraud_lift_delta"] < 0:
        decay_score += 10

    if false_positive_proxy == "high":
        decay_score += 25
    elif false_positive_proxy == "medium":
        decay_score += 10

    freshness_hours = quality_metrics["data_freshness_hours"]
    if freshness_hours >= 48:
        decay_score += 30
    elif freshness_hours >= 24:
        decay_score += 15

    if quality_metrics["anomaly_count"] > 0:
        decay_score += 10

    if governance_status == "fail":
        decay_score += 35
    elif governance_status == "conditional_pass":
        decay_score += 20

    decay_score = max(0, min(100, decay_score))

    if governance_status == "fail" or freshness_hours >= 48 or false_positive_proxy == "high":
        drift_proxy = "elevated"
    elif history_metrics["coverage_trend_proxy"] == "declining" or quality_metrics["anomaly_count"] > 0:
        drift_proxy = "watch"
    else:
        drift_proxy = "stable"

    if decay_score >= 70 or governance_status == "fail":
        monitoring_status = "failing"
        next_review_recommendation = "revalidate immediately"
    elif decay_score >= 35 or governance_status == "conditional_pass" or drift_proxy != "stable":
        monitoring_status = "decaying"
        next_review_recommendation = "review soon"
    else:
        monitoring_status = "stable"
        next_review_recommendation = "continue monitoring"

    return {
        "signal_id": signal.get("signal_id"),
        "signal_name": signal.get("signal_name"),
        "case_type": signal.get("case_type"),
        "review_status": entry.get("status", "unknown"),
        "reviewer": entry.get("reviewer"),
        "coverage_rate": history_metrics["coverage_rate"],
        "coverage_series": history_metrics["coverage_series"],
        "coverage_trend_proxy": history_metrics["coverage_trend_proxy"],
        "fraud_lift": history_metrics["fraud_lift"],
        "fraud_lift_series": history_metrics["fraud_lift_series"],
        "false_positive_proxy": false_positive_proxy,
        "data_freshness_hours": freshness_hours,
        "dataset_status": quality_metrics["dataset_status"],
        "drift_proxy": drift_proxy,
        "signal_decay_score": decay_score,
        "monitoring_status": monitoring_status,
        "next_review_recommendation": next_review_recommendation,
        "governance_status": governance_status,
        "source_tables": quality_metrics["source_tables"],
        "proxy_note": "Sample-data proxy metrics only. Not production fraud validation.",
    }


def _latest_unique_entries(entries: list[dict]) -> list[dict]:
    latest_by_signal_id: dict[str, dict] = {}
    for entry in entries:
        signal = entry.get("signal", {})
        signal_id = str(signal.get("signal_id", ""))
        if not signal_id:
            continue
        latest_by_signal_id[signal_id] = entry
    return list(latest_by_signal_id.values())


def get_signal_monitoring_summary(
    entries: list[dict] | None = None,
    adapter: BBDatasetAdapter | None = None,
) -> list[dict]:
    registry_entries = entries
    if registry_entries is None:
        registry_entries = SignalRegistry().list("approved")
    return [build_monitoring_card(entry, adapter=adapter) for entry in _latest_unique_entries(registry_entries)]
