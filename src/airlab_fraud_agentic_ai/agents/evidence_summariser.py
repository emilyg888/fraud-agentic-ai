from __future__ import annotations

from airlab_fraud_agentic_ai.dashboard.view_models import describe_threshold_status


def summarise_evidence(alert: dict, retrieved: dict, case_data: dict) -> str:
    typology_titles = ", ".join(item["title"] for item in retrieved["fraud_typologies"]) or "none"
    policy_titles = ", ".join(item["title"] for item in retrieved["policies"]) or "none"
    transaction_count = case_data["transaction_summary"]["transaction_count"]
    new_payee_count = case_data["new_payee_activity"]["new_payee_count"]
    device_changes = case_data["behavioural_summary"]["device_change_count"]
    threshold_summary = describe_threshold_status(
        model_score=float(alert["model_score"]),
        threshold=float(alert["threshold"]),
    )["threshold_summary"]
    return (
        f"Alert {alert['alert_id']}: {threshold_summary} "
        f"Retrieved typologies: {typology_titles}. Policies reviewed: {policy_titles}. "
        f"Observed {transaction_count} recent transactions, {new_payee_count} new payees, and "
        f"{device_changes} device changes for customer {alert['customer_id']}."
    )
