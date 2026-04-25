from __future__ import annotations


def plan_investigation(alert: dict, case_type: str, risk_level: str) -> dict:
    evidence_needed = [
        "customer profile",
        "recent transaction velocity",
        "new payee activity",
        "device change history",
        "feature values",
        "data quality status",
        "lineage status",
    ]
    if case_type == "synthetic_identity":
        evidence_needed.append("identity-related governance checks")
    return {
        "case_type": case_type,
        "risk_level": risk_level,
        "requires_human_review": risk_level in {"high", "medium"},
        "evidence_needed": evidence_needed,
        "rationale": f"Alert {alert['alert_id']} requires governed review of typology, behaviour, and policy evidence.",
    }
