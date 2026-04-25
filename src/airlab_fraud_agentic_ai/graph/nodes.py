from __future__ import annotations

from airlab_fraud_agentic_ai.agents.case_report_writer import render_case_report
from airlab_fraud_agentic_ai.agents.classifier import classify_case_type
from airlab_fraud_agentic_ai.agents.evidence_summariser import summarise_evidence
from airlab_fraud_agentic_ai.agents.planner import plan_investigation
from airlab_fraud_agentic_ai.agents.signal_hypothesis import generate_signal_hypotheses
from airlab_fraud_agentic_ai.tools.alert_tools import get_alert
from airlab_fraud_agentic_ai.tools.bb_dataset_tools import query_case_data
from airlab_fraud_agentic_ai.tools.governance_tools import aggregate_governance_checks
from airlab_fraud_agentic_ai.tools.retrieval_tools import retrieve_case_knowledge
from airlab_fraud_agentic_ai.tools.signal_eval_tools import evaluate_signals


def intake_case(case_id: str) -> dict:
    return get_alert(case_id)


def classify(alert: dict) -> dict:
    return classify_case_type(alert)


def plan(alert: dict, classification: dict) -> dict:
    return plan_investigation(alert=alert, case_type=classification["case_type"], risk_level=classification["risk_level"])


def retrieve(alert: dict, classification: dict) -> dict:
    return retrieve_case_knowledge(f"{classification['case_type']} {alert['triggered_features']}")


def query(alert: dict) -> dict:
    return query_case_data(alert)


def summarise(alert: dict, retrieved: dict, case_data: dict) -> str:
    return summarise_evidence(alert=alert, retrieved=retrieved, case_data=case_data)


def hypothesise(alert: dict, classification: dict, case_data: dict) -> list[dict]:
    return generate_signal_hypotheses(alert=alert, case_type=classification["case_type"], case_data=case_data)


def evaluate(signal_candidates: list[dict]) -> list[dict]:
    return evaluate_signals(signal_candidates)


def govern(case_data: dict, signal_candidates: list[dict]) -> dict:
    return aggregate_governance_checks(case_data=case_data, signal_candidates=signal_candidates)


def write_report(state: dict) -> str:
    return render_case_report(state)
