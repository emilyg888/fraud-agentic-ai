from __future__ import annotations


def should_pause_for_human_review(state: dict, require_human_review: bool) -> bool:
    if not require_human_review:
        return False
    if not state.get("signal_candidates"):
        return False
    return state.get("governance_findings", {}).get("approval_required", False)
