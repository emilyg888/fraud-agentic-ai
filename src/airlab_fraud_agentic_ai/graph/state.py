from __future__ import annotations

from typing import Any, TypedDict


class FraudInvestigationState(TypedDict, total=False):
    run_id: str
    case_id: str
    analyst_request: str
    alert: dict[str, Any]
    case_type: str
    risk_level: str
    investigation_plan: list[dict[str, Any]]
    retrieved_typologies: list[dict[str, Any]]
    retrieved_policies: list[dict[str, Any]]
    retrieved_data_definitions: list[dict[str, Any]]
    similar_cases: list[dict[str, Any]]
    customer_profile: dict[str, Any]
    account_summary: dict[str, Any]
    transaction_summary: dict[str, Any]
    new_payee_activity: dict[str, Any]
    behavioural_summary: dict[str, Any]
    feature_summary: dict[str, Any]
    data_quality: dict[str, Any]
    lineage: dict[str, Any]
    evidence_summary: str
    signal_candidates: list[dict[str, Any]]
    signal_evaluations: list[dict[str, Any]]
    governance_findings: dict[str, Any]
    human_review_status: str
    human_review_comments: str | None
    promoted_signals: list[dict[str, Any]]
    final_case_report: str
    audit_log: list[dict[str, Any]]
