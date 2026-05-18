from __future__ import annotations

import json

from airlab_fraud_agentic_ai.agents.llm_factory import get_llm


def _deterministic_case_report(state: dict) -> str:
    sources = []
    for section in ("retrieved_typologies", "retrieved_policies", "retrieved_data_definitions"):
        sources.extend(item["path"] for item in state.get(section, []))

    signal_names = ", ".join(signal["signal_name"] for signal in state.get("signal_candidates", [])) or "None"
    promoted = ", ".join(signal["signal_name"] for signal in state.get("promoted_signals", [])) or "None"
    governance_status = state.get("governance_findings", {}).get("governance_status", "not_run")
    audit_lines = "\n".join(
        f"- {item['timestamp']} | {item['step']} | {item['status']}"
        for item in state.get("audit_log", [])
    )

    return f"""# Case Report: {state['case_id']}

## Executive Summary
{state.get('evidence_summary', 'No evidence summary available.')}

## Alert Details
- Case type: {state.get('case_type', 'unknown')}
- Risk level: {state.get('risk_level', 'unknown')}
- Model score: {state['alert']['model_score']}
- Threshold: {state['alert']['threshold']}

## Likely Fraud Typology
{state.get('case_type', 'unknown')}

## Evidence Reviewed
- Customer profile reviewed
- Transaction, behavioural, feature, lineage, and quality summaries reviewed

## Retrieved Knowledge Sources
{chr(10).join(f"- {path}" for path in sources) or "- None"}

## Candidate Signals
{signal_names}

## Signal Evaluation
{state.get('signal_evaluations', [])}

## Governance Findings
{governance_status}

## Human Review Decision
{state.get('human_review_status', 'not_required')}

## Recommendation
Promoted signals: {promoted}

## Audit Trail
{audit_lines}

## Limitations
This report uses local sample data only and is not a production fraud decision artifact.
"""


def render_case_report(state: dict) -> str:
    baseline = _deterministic_case_report(state)
    if state.get("llm_backend", state.get("llm_provider")) != "ollama":
        return baseline

    report_context = {
        "case_id": state.get("case_id"),
        "case_type": state.get("case_type"),
        "risk_level": state.get("risk_level"),
        "alert": state.get("alert"),
        "evidence_summary": state.get("evidence_summary"),
        "retrieved_sources": {
            "typologies": state.get("retrieved_typologies", []),
            "policies": state.get("retrieved_policies", []),
            "data_definitions": state.get("retrieved_data_definitions", []),
        },
        "signal_candidates": state.get("signal_candidates", []),
        "signal_evaluations": state.get("signal_evaluations", []),
        "governance_findings": state.get("governance_findings", {}),
        "human_review_status": state.get("human_review_status"),
        "promoted_signals": state.get("promoted_signals", []),
        "audit_log": state.get("audit_log", []),
    }
    prompt = f"""
Draft a professional markdown fraud analyst case report grounded only in the provided
JSON. Do not make a final fraud decision. Preserve source paths, governance findings,
human-review status, and audit trail entries. Include a limitations section stating
that this uses local sample data and is not a production fraud decision artifact.

If evidence is incomplete, say so. Keep the report concise and analyst-facing.

Baseline report:
{baseline}

Grounding JSON:
{json.dumps(report_context, indent=2)}
""".strip()
    return get_llm(backend="ollama").invoke(prompt).strip()
