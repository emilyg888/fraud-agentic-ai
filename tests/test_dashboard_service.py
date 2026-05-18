from __future__ import annotations

from airlab_fraud_agentic_ai.dashboard.service import (
    ask_case_question,
    get_audit_trace,
    get_case_overview,
    get_report,
    get_signal_regression_summary,
    get_signal_monitoring_summary,
    list_case_queue,
    list_signal_registry,
    run_investigation,
    submit_signal_decision,
)


def test_dashboard_service_runs_case_and_answers_question() -> None:
    queue = list_case_queue()
    assert queue
    overview = get_case_overview("A-1001")
    assert overview["case_id"] == "A-1001"

    run = run_investigation("A-1001", llm_backend="fake", require_human_review=True)
    answer = ask_case_question(run["run_id"], "Why was this case flagged?")
    report = get_report(run["run_id"])
    assert "evidence" in answer["limitations"].lower()
    assert report.startswith("# Case Report")


def test_dashboard_service_can_submit_decision_and_expose_artifacts() -> None:
    run = run_investigation("A-1001", llm_backend="fake", require_human_review=True)
    signal_id = run["candidate_signals"][0]["signal_id"]
    submit_signal_decision(run["run_id"], signal_id, "approve", "reviewer_1", "approved for demo")
    report = get_report(run["run_id"])
    audit = get_audit_trace(run["run_id"])
    registry = list_signal_registry("approved")
    monitoring = get_signal_monitoring_summary()

    assert report.startswith("# Case Report")
    assert audit["audit_log"]
    assert registry
    assert monitoring
    assert monitoring[0]["signal_decay_score"] >= 0
    assert monitoring[0]["proxy_note"].startswith("Sample-data proxy metrics")
    assert get_signal_regression_summary()["overall_status"] in {"pass", "warning", "fail"}
