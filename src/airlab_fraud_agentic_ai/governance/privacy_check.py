from __future__ import annotations


def run_privacy_check(signal_candidates: list[dict], lineage: dict) -> dict:
    sensitivities = {record["sensitivity"] for record in lineage.get("records", [])}
    restricted = "restricted" in sensitivities
    return {
        "status": "conditional_pass" if restricted else "pass",
        "issues": ["Restricted source feature requires reviewer attention."] if restricted else [],
        "approval_required": True,
    }
