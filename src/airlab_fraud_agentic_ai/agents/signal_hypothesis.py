from __future__ import annotations

import json

from airlab_fraud_agentic_ai.agents.llm_factory import get_llm


def _parse_json_object(raw: str) -> dict:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.removeprefix("json").strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end >= start:
        cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)


def _rewrite_hypothesis_wording(candidate: dict, alert: dict, case_data: dict, llm_backend: str) -> dict:
    if llm_backend != "ollama":
        return candidate

    prompt = f"""
You are helping phrase a candidate fraud signal for analyst review. Rewrite only the
description and hypothesis fields. Keep the meaning, do not change signal IDs, feature
names, expected direction, case type, or imply approval/promotion. Ground the wording
only in the provided JSON and keep each rewritten field under 35 words.

Return JSON only with keys "description" and "hypothesis".

Candidate JSON:
{json.dumps(candidate, indent=2)}

Alert JSON:
{json.dumps(alert, indent=2)}

Case data summary JSON:
{json.dumps(case_data, indent=2)}
""".strip()
    raw = get_llm(backend=llm_backend).invoke(prompt).strip()
    try:
        rewritten = _parse_json_object(raw)
    except (json.JSONDecodeError, TypeError):
        return candidate
    return {
        **candidate,
        "description": str(rewritten.get("description", candidate["description"])),
        "hypothesis": str(rewritten.get("hypothesis", candidate["hypothesis"])),
    }


def generate_signal_hypotheses(alert: dict, case_type: str, case_data: dict, llm_backend: str = "fake") -> list[dict]:
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

    return [
        _rewrite_hypothesis_wording(candidate, alert=alert, case_data=case_data, llm_backend=llm_backend)
        for candidate in candidates
    ]
