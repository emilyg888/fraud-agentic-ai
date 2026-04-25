from __future__ import annotations

from airlab_fraud_agentic_ai.graph.workflow import FraudInvestigationWorkflow


def test_human_review_approval_resumes_workflow() -> None:
    workflow = FraudInvestigationWorkflow()
    paused = workflow.run_case("A-1001", require_human_review=True)
    signal_id = paused["signal_candidates"][0]["signal_id"]

    resumed = workflow.submit_human_decision(
        run_id=paused["run_id"],
        signal_id=signal_id,
        decision="approve",
        reviewer="fraud_analyst_demo",
        comments="Strong supporting evidence.",
    )
    assert resumed["human_review_status"] == "approved"
    assert resumed["promoted_signals"][0]["signal_id"] == signal_id
