from __future__ import annotations

import json

from airlab_fraud_agentic_ai.agents.llm_factory import get_llm
from airlab_fraud_agentic_ai.config import get_settings
from airlab_fraud_agentic_ai.dashboard.view_models import build_case_overview, build_run_summary
from airlab_fraud_agentic_ai.data.bb_adapter import BBDatasetAdapter
from airlab_fraud_agentic_ai.evaluation.regression_tests import run_registry_regression_suite
from airlab_fraud_agentic_ai.graph.persistence import load_run_trace
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


def run_investigation(
    case_id: str,
    llm_backend: str | None = None,
    require_human_review: bool = True,
    llm_provider: str | None = None,
) -> dict:
    selected_backend = llm_provider or llm_backend or get_settings().llm_backend
    workflow = FraudInvestigationWorkflow()
    state = workflow.run_case(case_id=case_id, llm_backend=selected_backend, require_human_review=require_human_review)
    return build_run_summary(state)


def get_run_state(run_id: str) -> dict:
    workflow = FraudInvestigationWorkflow()
    return workflow.get_state(run_id)


def ask_case_question(run_id: str, question: str) -> dict:
    state = get_run_state(run_id)
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

    if state.get("llm_backend", state.get("llm_provider")) == "ollama":
        prompt = f"""
Answer the analyst question using only the current case JSON. Do not use outside facts.
Do not make a final fraud decision or approve/reject a signal. Cite the available
evidence references by path when relevant, mention governance caveats, and state
limitations if the current evidence does not answer the question.

Question:
{question}

Deterministic baseline answer:
{answer}

Current case JSON:
{json.dumps({
    "case_id": state.get("case_id"),
    "case_type": state.get("case_type"),
    "risk_level": state.get("risk_level"),
    "alert": state.get("alert"),
    "evidence_summary": state.get("evidence_summary"),
    "retrieved_typologies": state.get("retrieved_typologies", []),
    "retrieved_policies": state.get("retrieved_policies", []),
    "retrieved_data_definitions": state.get("retrieved_data_definitions", []),
    "signal_candidates": state.get("signal_candidates", []),
    "signal_evaluations": state.get("signal_evaluations", []),
    "governance_findings": state.get("governance_findings", {}),
    "human_review_status": state.get("human_review_status"),
}, indent=2)}
""".strip()
        answer = get_llm(backend="ollama").invoke(prompt).strip()

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
    state = get_run_state(run_id)
    return state.get("final_case_report", "")


def get_audit_trace(run_id: str) -> dict:
    state = get_run_state(run_id)
    return {"run_id": run_id, "audit_log": state.get("audit_log", [])}


def list_signal_registry_entries(status: str | None = None) -> list[dict]:
    return list_registry_entries(status=status)


def get_signal_monitoring_summary() -> list[dict]:
    return monitoring_summary()


def list_signal_registry(status: str | None = None) -> list[dict]:
    return list_signal_registry_entries(status=status)


def export_run_trace(run_id: str) -> str:
    try:
        state = get_run_state(run_id)
    except FileNotFoundError:
        state = load_run_trace(run_id)
    return json.dumps(state, indent=2)


def get_signal_regression_summary() -> dict:
    return run_registry_regression_suite()
