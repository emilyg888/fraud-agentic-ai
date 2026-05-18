from __future__ import annotations

from airlab_fraud_agentic_ai.agents import case_report_writer, evidence_summariser, signal_hypothesis
from airlab_fraud_agentic_ai.dashboard import service


class StubLLM:
    def __init__(self, response: str) -> None:
        self.response = response

    def invoke(self, prompt: str) -> str:
        return self.response


def test_ollama_backend_rewrites_evidence_summary_without_network(monkeypatch) -> None:
    monkeypatch.setattr(evidence_summariser, "get_llm", lambda **kwargs: StubLLM("Analyst narrative."))

    summary = evidence_summariser.summarise_evidence(
        alert={"alert_id": "A-1001", "customer_id": "C-1001", "model_score": 0.91, "threshold": 0.75},
        retrieved={"fraud_typologies": [{"title": "Account Takeover"}], "policies": []},
        case_data={
            "transaction_summary": {"transaction_count": 3},
            "new_payee_activity": {"new_payee_count": 2},
            "behavioural_summary": {"device_change_count": 1},
        },
        llm_backend="ollama",
    )

    assert summary == "Analyst narrative."


def test_ollama_backend_rewrites_only_signal_wording(monkeypatch) -> None:
    monkeypatch.setattr(
        signal_hypothesis,
        "get_llm",
        lambda **kwargs: StubLLM(
            '{"description": "Analyst-facing signal description.", "hypothesis": "Analyst-facing hypothesis."}'
        ),
    )

    candidates = signal_hypothesis.generate_signal_hypotheses(
        alert={"alert_id": "A-1001"},
        case_type="account_takeover",
        case_data={
            "feature_summary": {
                "features": [
                    {"feature_name": "device_change_count_24h"},
                    {"feature_name": "new_payee_count_24h"},
                    {"feature_name": "transaction_amount_zscore_24h"},
                ]
            }
        },
        llm_backend="ollama",
    )

    assert candidates[0]["signal_id"] == "A-1001-SIG-1"
    assert candidates[0]["source_features"] == [
        "device_change_count_24h",
        "new_payee_count_24h",
        "transaction_amount_zscore_24h",
    ]
    assert candidates[0]["description"] == "Analyst-facing signal description."
    assert candidates[0]["hypothesis"] == "Analyst-facing hypothesis."


def test_ollama_backend_drafts_case_report_without_network(monkeypatch) -> None:
    monkeypatch.setattr(case_report_writer, "get_llm", lambda **kwargs: StubLLM("# Case Report\n\nLocal Qwen draft."))

    report = case_report_writer.render_case_report(
        {
            "llm_backend": "ollama",
            "case_id": "A-1001",
            "case_type": "account_takeover",
            "risk_level": "high",
            "alert": {"model_score": 0.91, "threshold": 0.75},
            "audit_log": [],
        }
    )

    assert report == "# Case Report\n\nLocal Qwen draft."


def test_ollama_backend_answers_case_copilot_without_network(monkeypatch) -> None:
    monkeypatch.setattr(service, "get_llm", lambda **kwargs: StubLLM("Grounded copilot answer."))
    monkeypatch.setattr(
        service,
        "get_run_state",
        lambda run_id: {
            "case_id": "A-1001",
            "case_type": "account_takeover",
            "risk_level": "high",
            "llm_backend": "ollama",
            "alert": {"alert_id": "A-1001"},
            "evidence_summary": "Baseline evidence.",
            "retrieved_typologies": [{"path": "knowledge/fraud_typologies/account_takeover.md"}],
            "retrieved_policies": [],
            "retrieved_data_definitions": [],
            "signal_candidates": [],
            "signal_evaluations": [],
            "governance_findings": {"governance_status": "pass", "comments": []},
            "human_review_status": "pending_human_review",
        },
    )

    answer = service.ask_case_question("run-123", "Why was this case flagged?")

    assert answer["answer"] == "Grounded copilot answer."
    assert answer["evidence_references"] == ["knowledge/fraud_typologies/account_takeover.md"]
