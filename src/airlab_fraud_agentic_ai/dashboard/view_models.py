from __future__ import annotations


def describe_threshold_status(model_score: float, threshold: float) -> dict:
    exceeded = model_score >= threshold
    return {
        "threshold_status": "exceeded" if exceeded else "below_threshold",
        "threshold_gap": round(model_score - threshold, 4),
        "threshold_summary": (
            f"Score {model_score:.2f} exceeded threshold {threshold:.2f}."
            if exceeded
            else f"Score {model_score:.2f} did not exceed threshold {threshold:.2f}."
        ),
    }


def build_run_summary(state: dict) -> dict:
    return {
        "run_id": state["run_id"],
        "case_id": state["case_id"],
        "case_type": state.get("case_type"),
        "risk_level": state.get("risk_level"),
        "human_review_status": state.get("human_review_status"),
        "candidate_signals": state.get("signal_candidates", []),
        "governance_findings": state.get("governance_findings", {}),
        "audit_log": state.get("audit_log", []),
    }


def build_case_overview(alert: dict) -> dict:
    threshold_view = describe_threshold_status(
        model_score=float(alert["model_score"]),
        threshold=float(alert["threshold"]),
    )
    return {
        "case_id": alert["alert_id"],
        "customer_id": alert["customer_id"],
        "model_score": alert["model_score"],
        "threshold": alert["threshold"],
        "triggered_features": alert["triggered_features"].split("|"),
        "analyst_request": alert["analyst_request"],
        **threshold_view,
    }
