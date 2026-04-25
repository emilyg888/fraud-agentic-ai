from __future__ import annotations


def render_case_report(state: dict) -> str:
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
