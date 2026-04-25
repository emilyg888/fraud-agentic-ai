from __future__ import annotations


def generate_signal_hypotheses(alert: dict, case_type: str, case_data: dict) -> list[dict]:
    candidates: list[dict] = []
    feature_names = {
        item["feature_name"] for item in case_data["feature_summary"]["features"]
    }

    if {
        "device_change_count_24h",
        "new_payee_count_24h",
        "transaction_amount_zscore_24h",
    }.issubset(feature_names):
        candidates.append(
            {
                "signal_id": f"{alert['alert_id']}-SIG-1",
                "signal_name": "new_device_high_value_new_payee_velocity",
                "description": "New device activity followed by high-value transfers to new payees.",
                "source_features": sorted(feature_names),
                "hypothesis": "May indicate account takeover or scam-induced payment.",
                "expected_direction": "higher values increase risk",
                "case_type": case_type,
            }
        )

    if "synthetic_identity_score" in feature_names:
        candidates.append(
            {
                "signal_id": f"{alert['alert_id']}-SIG-2",
                "signal_name": "synthetic_identity_stale_feature_conflict",
                "description": "Synthetic identity score is elevated while supporting features have freshness concerns.",
                "source_features": sorted(feature_names),
                "hypothesis": "May indicate weak identity integrity or unusable supporting features.",
                "expected_direction": "higher values increase review priority",
                "case_type": case_type,
            }
        )

    return candidates
