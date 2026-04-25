from __future__ import annotations

from airlab_fraud_agentic_ai.tools.alert_tools import get_alert
from airlab_fraud_agentic_ai.tools.bb_dataset_tools import (
    get_customer_profile,
    get_device_change_summary,
    get_feature_values,
    get_new_payee_activity,
    get_transaction_velocity,
    query_case_data,
)


def test_get_alert_returns_expected_case() -> None:
    alert = get_alert("A-1001")
    assert alert["customer_id"] == "C-1001"


def test_bb_dataset_tools_produce_deterministic_summaries() -> None:
    assert get_customer_profile("C-1001")["risk_rating"] == "medium"
    assert get_transaction_velocity("C-1001")["transaction_count"] == 3
    assert get_new_payee_activity("C-1001")["new_payee_count"] == 2
    assert get_device_change_summary("C-1001")["device_change_count"] >= 1
    assert len(get_feature_values("A-1001")["features"]) == 3


def test_query_case_data_returns_all_sections() -> None:
    alert = get_alert("A-1001")
    case_data = query_case_data(alert)
    assert "customer_profile" in case_data
    assert "lineage" in case_data
