from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CandidateSignal(BaseModel):
    signal_id: str
    signal_name: str
    description: str
    source_features: list[str]
    hypothesis: str
    expected_direction: str
    case_type: str


class SignalEvaluation(BaseModel):
    signal_name: str
    coverage_rate: float
    fraud_lift: float
    confirmed_fraud_rate: float
    false_positive_risk: str
    data_quality_status: str
    explainability_score: int
    recommendation: str


class GovernanceFinding(BaseModel):
    governance_status: str
    lineage_status: str
    data_quality_status: str
    privacy_status: str
    explainability_status: str
    approval_required: bool
    comments: list[str] = Field(default_factory=list)


class RegistryEntry(BaseModel):
    run_id: str
    case_id: str
    status: str
    reviewer: str | None = None
    comments: str = ""
    signal: dict[str, Any]
    evaluation: dict[str, Any] | None = None
    governance: dict[str, Any] | None = None
