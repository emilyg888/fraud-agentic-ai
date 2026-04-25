from __future__ import annotations

from airlab_fraud_agentic_ai.tools.alert_tools import get_alert
from airlab_fraud_agentic_ai.tools.bb_dataset_tools import query_case_data
from airlab_fraud_agentic_ai.tools.governance_tools import aggregate_governance_checks


def test_governance_flags_restricted_or_stale_inputs() -> None:
    alert = get_alert("A-1003")
    case_data = query_case_data(alert)
    signal_candidates = [
        {
            "signal_name": "synthetic_identity_stale_feature_conflict",
            "description": "test",
        }
    ]
    result = aggregate_governance_checks(case_data, signal_candidates)
    assert result["governance_status"] in {"conditional_pass", "fail"}
    assert result["approval_required"] is True
