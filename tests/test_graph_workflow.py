from __future__ import annotations

from pathlib import Path

from airlab_fraud_agentic_ai.graph.workflow import FraudInvestigationWorkflow


def test_workflow_pauses_for_human_review() -> None:
    workflow = FraudInvestigationWorkflow()
    state = workflow.run_case("A-1001", require_human_review=True)
    assert state["human_review_status"] == "pending_human_review"
    assert state["signal_candidates"]
    assert state["retrieved_typologies"]
    assert state["final_case_report"].startswith("# Case Report")
    assert Path(state["report_path"]).read_text(encoding="utf-8").startswith("# Case Report")
    assert any(item["step"] == "human_review" and item["status"] == "paused" for item in state["audit_log"])
    assert state["audit_log"][-1]["step"] == "generate_case_report"


def test_workflow_can_complete_without_human_pause() -> None:
    workflow = FraudInvestigationWorkflow()
    state = workflow.run_case("A-1001", require_human_review=False)
    assert state["human_review_status"] == "auto_approved"
    assert state["final_case_report"].startswith("# Case Report")
    assert Path(state["report_path"]).read_text(encoding="utf-8").startswith("# Case Report")
