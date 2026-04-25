from __future__ import annotations

import json

from airlab_fraud_agentic_ai.agents.case_report_writer import render_case_report
from airlab_fraud_agentic_ai.config import get_settings
from airlab_fraud_agentic_ai.dashboard.view_models import build_case_overview, build_run_summary
from airlab_fraud_agentic_ai.data.bb_adapter import BBDatasetAdapter
from airlab_fraud_agentic_ai.evaluation.regression_tests import run_registry_regression_suite
from airlab_fraud_agentic_ai.graph.persistence import load_run_state, save_run_state
from airlab_fraud_agentic_ai.graph.workflow import FraudInvestigationWorkflow
from airlab_fraud_agentic_ai.tools.alert_tools import get_alert
from airlab_fraud_agentic_ai.tools.registry_tools import (
    list_signal_registry as list_registry_entries,
    monitoring_summary,
)


def list_case_queue() -> list[dict]:
    adapter = BBDatasetAdapter.create()
    rows = adapter.alerts().sort_values("model_score", ascending=False)
    return rows.to_dict(orient="records")


def get_case_overview(case_id: str) -> dict:
    alert = get_alert(case_id)
    return build_case_overview(alert)


def run_investigation(case_id: str, llm_provider: str = "fake", require_human_review: bool = True) -> dict:
    selected_provider = llm_provider or get_settings().llm_provider
    workflow = FraudInvestigationWorkflow()
    state = workflow.run_case(case_id=case_id, llm_provider=selected_provider, require_human_review=require_human_review)
    return build_run_summary(state)


def get_run_state(run_id: str) -> dict:
    return load_run_state(run_id)


def ask_case_question(run_id: str, question: str) -> dict:
    state = load_run_state(run_id)
    lowered = question.lower()
    evidence_refs = [item["path"] for item in state.get("retrieved_typologies", []) + state.get("retrieved_policies", [])]

    if "why" in lowered and "flagged" in lowered:
        answer = state["evidence_summary"]
    elif "typolog" in lowered:
        titles = [item["title"] for item in state.get("retrieved_typologies", [])]
        answer = f"Relevant typologies: {', '.join(titles) or 'none'}."
    elif "data quality" in lowered or "lineage" in lowered:
        answer = (
            f"Governance status is {state['governance_findings']['governance_status']}. "
            f"Comments: {', '.join(state['governance_findings']['comments']) or 'none'}."
        )
    else:
        answer = (
            "Bounded copilot answer: use current evidence summary, signal evaluation, and governance findings. "
            f"Current recommendation is {state.get('human_review_status', 'pending')}."
        )

    return {
        "question": question,
        "answer": answer,
        "evidence_references": evidence_refs,
        "limitations": "Answer uses current case evidence, retrieved knowledge, and local sample data only.",
    }


def submit_signal_decision(run_id: str, signal_id: str, decision: str, reviewer: str, comments: str = "") -> dict:
    workflow = FraudInvestigationWorkflow()
    state = workflow.submit_human_decision(
        run_id=run_id,
        signal_id=signal_id,
        decision=decision,
        reviewer=reviewer,
        comments=comments,
    )
    return build_run_summary(state)


def get_report(run_id: str) -> str:
    state = load_run_state(run_id)
    report = state.get("final_case_report", "")
    if report:
        if not state.get("report_path") or not state.get("run_trace_path"):
            save_run_state(run_id, state)
        return report

    backfilled_report = render_case_report(state)
    state["final_case_report"] = backfilled_report
    save_run_state(run_id, state)
    return backfilled_report


def get_audit_trace(run_id: str) -> dict:
    state = load_run_state(run_id)
    return {"run_id": run_id, "audit_log": state.get("audit_log", [])}


def list_signal_registry_entries(status: str | None = None) -> list[dict]:
    return list_registry_entries(status=status)


def get_signal_monitoring_summary() -> list[dict]:
    return monitoring_summary()


def list_signal_registry(status: str | None = None) -> list[dict]:
    return list_signal_registry_entries(status=status)


def export_run_trace(run_id: str) -> str:
    return json.dumps(load_run_state(run_id), indent=2)


def get_signal_regression_summary() -> dict:
    return run_registry_regression_suite()
