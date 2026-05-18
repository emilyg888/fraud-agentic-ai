from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AlertRecord(BaseModel):
    alert_id: str
    customer_id: str
    model_score: float
    threshold: float
    triggered_features: str
    alert_time: str
    status: str
    analyst_request: str


class CustomerRecord(BaseModel):
    customer_id: str
    age_band: str
    tenure: int
    segment: str
    geography: str
    risk_rating: str


class AccountRecord(BaseModel):
    account_id: str
    customer_id: str
    product_type: str
    open_date: str
    status: str


class TransactionRecord(BaseModel):
    transaction_id: str
    customer_id: str
    timestamp: str
    amount: float
    merchant: str
    channel: str
    device_id: str
    payee_id: str
    location: str
    is_new_payee: bool


class BehaviouralEventRecord(BaseModel):
    event_id: str
    customer_id: str
    login_time: str
    device_id: str
    device_changed: bool
    failed_login_count: int
    channel: str
    session_duration: int
    geolocation_anomaly: bool


class FeatureRecord(BaseModel):
    feature_record_id: str
    alert_id: str
    feature_name: str
    feature_value: float
    window: str
    source_table: str
    calculation_logic: str


class HistoricalCaseRecord(BaseModel):
    case_id: str
    case_type: str
    confirmed_fraud_flag: bool
    investigation_outcome: str
    loss_amount: float
    signal_name: str


class DataQualityRecord(BaseModel):
    dataset_name: str
    freshness_hours: int
    null_rate: float
    anomaly_count: int
    status: str


class LineageRecord(BaseModel):
    field_name: str
    source_system: str
    owner: str
    sensitivity: str
    certification_status: str


class CaseEvidenceRecord(BaseModel):
    evidence_id: str
    case_id: str
    alert_id: str
    run_id: str | None = None
    customer_id: str | None = None
    evidence_type: str
    source_tool: str | None = None
    source_document: str | None = None
    source_path: str | None = None
    source_record_id: str | None = None
    retrieval_timestamp: str
    workflow_step: str
    summary: str
    raw_reference: dict[str, Any]
    confidence_score: float | None = Field(default=None, ge=0.0, le=1.0)
    quality_notes: list[str] = Field(default_factory=list)
    policy_sensitivity: str
    sensitivity_rationale: str | None = None
    lineage_references: list[str] = Field(default_factory=list)
    audit_event_ids: list[str] = Field(default_factory=list)
    supporting_hypothesis_ids: list[str] = Field(default_factory=list)
    supporting_claim_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuditEntry(BaseModel):
    step: str
    status: str
    timestamp: str
    details: dict[str, Any] = Field(default_factory=dict)
