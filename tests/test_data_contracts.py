from __future__ import annotations

from airlab_fraud_agentic_ai.data.contracts import (
    AlertRecord,
    CaseEvidenceRecord,
    CustomerRecord,
    TransactionRecord,
)


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


def test_case_evidence_record_schema_links_claims_to_source_evidence() -> None:
    record = CaseEvidenceRecord(
        evidence_id="EV-A-1001-001",
        case_id="A-1001",
        alert_id="A-1001",
        run_id="run-123",
        customer_id="C-1001",
        evidence_type="transaction_summary",
        source_tool="query_case_data",
        source_document=None,
        source_path="data/sample/transactions.csv",
        source_record_id="T-1",
        retrieval_timestamp="2026-04-24T09:02:00Z",
        workflow_step="query_case_data",
        summary="Recent payment velocity increased after a new payee was added.",
        raw_reference={
            "dataset": "transactions",
            "record_ids": ["T-1", "T-2"],
            "fields": ["timestamp", "amount", "payee_id", "is_new_payee"],
        },
        confidence_score=0.86,
        quality_notes=["Data freshness check passed."],
        policy_sensitivity="internal",
        sensitivity_rationale="Uses synthetic customer and transaction identifiers only.",
        lineage_references=["transaction_id", "payee_id"],
        audit_event_ids=["audit-query-case-data"],
        supporting_hypothesis_ids=["HYP-A-1001-001"],
        supporting_claim_ids=["CLAIM-A-1001-001"],
        metadata={"source_system": "sample_csv"},
    )

    assert record.evidence_id == "EV-A-1001-001"
    assert record.raw_reference["record_ids"] == ["T-1", "T-2"]
    assert record.supporting_claim_ids == ["CLAIM-A-1001-001"]
