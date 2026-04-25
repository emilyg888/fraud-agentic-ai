from __future__ import annotations

from airlab_fraud_agentic_ai.data.contracts import AlertRecord, CustomerRecord, TransactionRecord


def test_alert_contract_parses_sample_record() -> None:
    record = AlertRecord(
        alert_id="A-1001",
        customer_id="C-1001",
        model_score=0.91,
        threshold=0.75,
        triggered_features="device_change_count_24h|new_payee_count_24h",
        alert_time="2026-04-24T09:00:00Z",
        status="open",
        analyst_request="Investigate alert A-1001",
    )
    assert record.alert_id == "A-1001"


def test_customer_contract_parses_sample_record() -> None:
    record = CustomerRecord(
        customer_id="C-1001",
        age_band="25-34",
        tenure=2,
        segment="digital_only",
        geography="Sydney",
        risk_rating="medium",
    )
    assert record.segment == "digital_only"


def test_transaction_contract_casts_boolean() -> None:
    record = TransactionRecord(
        transaction_id="T-1",
        customer_id="C-1",
        timestamp="2026-04-24T07:10:00Z",
        amount=100.0,
        merchant="transfer",
        channel="app",
        device_id="D-1",
        payee_id="P-1",
        location="Sydney",
        is_new_payee=True,
    )
    assert record.is_new_payee is True
