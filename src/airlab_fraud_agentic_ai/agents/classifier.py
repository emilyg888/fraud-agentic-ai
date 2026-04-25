from __future__ import annotations


def classify_case_type(alert: dict) -> dict:
    features = alert["triggered_features"]
    score = float(alert["model_score"])

    if "synthetic_identity_score" in features:
        case_type = "synthetic_identity"
    elif "device_change_count_24h" in features or "new_payee_count_24h" in features:
        case_type = "account_takeover"
    elif "payee_concentration_7d" in features:
        case_type = "scam_payment"
    else:
        case_type = "generic_fraud_review"

    risk_level = "high" if score >= 0.8 else "medium" if score >= 0.7 else "low"
    return {"case_type": case_type, "risk_level": risk_level}
