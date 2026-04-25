from __future__ import annotations

from airlab_fraud_agentic_ai.governance.data_quality_check import run_data_quality_check
from airlab_fraud_agentic_ai.governance.explainability_check import run_explainability_check
from airlab_fraud_agentic_ai.governance.lineage_check import run_lineage_check
from airlab_fraud_agentic_ai.governance.privacy_check import run_privacy_check


def aggregate_governance_checks(case_data: dict, signal_candidates: list[dict]) -> dict:
    lineage = run_lineage_check(case_data["lineage"])
    data_quality = run_data_quality_check(case_data["data_quality"])
    privacy = run_privacy_check(signal_candidates, case_data["lineage"])
    explainability = run_explainability_check(signal_candidates)

    statuses = [lineage["status"], data_quality["status"], privacy["status"], explainability["status"]]
    if "fail" in statuses:
        overall = "fail"
    elif "conditional_pass" in statuses:
        overall = "conditional_pass"
    else:
        overall = "pass"

    comments = lineage["issues"] + data_quality["issues"] + privacy["issues"] + explainability["issues"]
    return {
        "governance_status": overall,
        "lineage_status": lineage["status"],
        "data_quality_status": data_quality["status"],
        "privacy_status": privacy["status"],
        "explainability_status": explainability["status"],
        "approval_required": True,
        "comments": comments,
    }
