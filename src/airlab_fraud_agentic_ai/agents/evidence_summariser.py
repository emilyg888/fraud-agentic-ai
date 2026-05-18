from __future__ import annotations

import json

from airlab_fraud_agentic_ai.agents.llm_factory import get_llm
from airlab_fraud_agentic_ai.dashboard.view_models import describe_threshold_status


def _deterministic_evidence_summary(alert: dict, retrieved: dict, case_data: dict) -> str:
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


def summarise_evidence(alert: dict, retrieved: dict, case_data: dict, llm_backend: str = "fake") -> str:
    baseline = _deterministic_evidence_summary(alert, retrieved, case_data)
    if llm_backend != "ollama":
        return baseline

    prompt = f"""
You are assisting a fraud analyst. Rewrite the evidence into a concise analyst-facing
narrative grounded only in the provided JSON. Do not make a final fraud decision. Do
not invent facts, source names, counts, or policy findings. Include source references
by title or path where available and call out limitations or caveats.

Baseline summary:
{baseline}

Evidence JSON:
{json.dumps({"alert": alert, "retrieved": retrieved, "case_data": case_data}, indent=2)}
""".strip()
    return get_llm(backend=llm_backend).invoke(prompt).strip()
