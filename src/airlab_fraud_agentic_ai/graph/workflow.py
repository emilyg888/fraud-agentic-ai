from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from airlab_fraud_agentic_ai.config import get_settings
from airlab_fraud_agentic_ai.graph import nodes
from airlab_fraud_agentic_ai.graph.persistence import load_run_state, save_run_state
from airlab_fraud_agentic_ai.graph.routing import should_pause_for_human_review
from airlab_fraud_agentic_ai.tools.registry_tools import (
    approve_signal,
    register_candidate_signals,
    reject_signal,
)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


class FraudInvestigationWorkflow:
    def _audit(self, state: dict, step: str, status: str, **details: object) -> None:
        state.setdefault("audit_log", []).append(
            {
                "step": step,
                "status": status,
                "timestamp": _timestamp(),
                "details": details,
            }
        )

    def run_case(self, case_id: str, llm_provider: str = "fake", require_human_review: bool = True) -> dict:
        run_id = uuid4().hex[:12]
        settings = get_settings()
        state: dict = {
            "run_id": run_id,
            "case_id": case_id,
            "promoted_signals": [],
            "audit_log": [],
            "human_review_status": "not_required",
            "human_review_comments": None,
            "llm_provider": llm_provider,
            "model_name": settings.model_name,
        }

        alert = nodes.intake_case(case_id)
        state["alert"] = alert
        state["analyst_request"] = alert["analyst_request"]
        self._audit(state, "intake_case", "completed", case_id=case_id)

        classification = nodes.classify(alert)
        state.update(classification)
        self._audit(state, "classify_case_type", "completed", classification=classification)

        plan = nodes.plan(alert, classification)
        state["investigation_plan"] = [
            {"evidence_needed": item} for item in plan["evidence_needed"]
        ]
        self._audit(state, "plan_investigation", "completed", plan=plan)

        retrieved = nodes.retrieve(alert, classification)
        state["retrieved_typologies"] = retrieved["fraud_typologies"]
        state["retrieved_policies"] = retrieved["policies"]
        state["retrieved_data_definitions"] = retrieved["data_dictionary"]
        self._audit(state, "retrieve_knowledge", "completed", retrieved_counts={k: len(v) for k, v in retrieved.items()})

        case_data = nodes.query(alert)
        state.update(case_data)
        self._audit(state, "query_case_data", "completed")

        state["evidence_summary"] = nodes.summarise(alert, retrieved, case_data)
        self._audit(state, "summarise_evidence", "completed")

        state["signal_candidates"] = nodes.hypothesise(alert, classification, case_data)
        self._audit(state, "generate_signal_hypotheses", "completed", candidate_count=len(state["signal_candidates"]))

        state["signal_evaluations"] = nodes.evaluate(state["signal_candidates"])
        self._audit(state, "evaluate_signals", "completed", evaluation_count=len(state["signal_evaluations"]))

        state["governance_findings"] = nodes.govern(case_data, state["signal_candidates"])
        self._audit(state, "governance_check", "completed", governance=state["governance_findings"])

        candidate_entries = [
            {
                "run_id": run_id,
                "case_id": case_id,
                "status": "candidate",
                "reviewer": None,
                "comments": "",
                "signal": signal,
                "evaluation": next(
                    (item for item in state["signal_evaluations"] if item["signal_name"] == signal["signal_name"]),
                    None,
                ),
                "governance": state["governance_findings"],
            }
            for signal in state["signal_candidates"]
        ]
        if candidate_entries:
            register_candidate_signals(candidate_entries)

        if should_pause_for_human_review(state, require_human_review=require_human_review):
            state["human_review_status"] = "pending_human_review"
            self._audit(state, "human_review", "paused")
            state["final_case_report"] = nodes.write_report(state)
            self._audit(state, "generate_case_report", "completed")
            save_run_state(run_id, state)
            return state

        if candidate_entries:
            approved_entries = [
                approve_signal(entry["signal"]["signal_id"], reviewer="system_auto", comments="Auto-approved for local demo.")
                for entry in candidate_entries
            ]
            state["promoted_signals"] = [entry["signal"] for entry in approved_entries]
            state["human_review_status"] = "auto_approved"
            self._audit(state, "promote_signal", "completed", promoted_count=len(approved_entries))

        state["final_case_report"] = nodes.write_report(state)
        self._audit(state, "generate_case_report", "completed")
        save_run_state(run_id, state)
        return state

    def submit_human_decision(
        self,
        run_id: str,
        signal_id: str,
        decision: str,
        reviewer: str,
        comments: str = "",
    ) -> dict:
        state = load_run_state(run_id)
        if state.get("human_review_status") != "pending_human_review":
            raise ValueError("Run is not waiting for human review.")

        if decision == "approve":
            moved = approve_signal(signal_id=signal_id, reviewer=reviewer, comments=comments)
            state.setdefault("promoted_signals", []).append(moved["signal"])
            state["human_review_status"] = "approved"
        elif decision == "reject":
            reject_signal(signal_id=signal_id, reviewer=reviewer, comments=comments)
            state["human_review_status"] = "rejected"
        else:
            raise ValueError("decision must be 'approve' or 'reject'")

        state["human_review_comments"] = comments
        self._audit(state, "human_review", "completed", decision=decision, reviewer=reviewer, signal_id=signal_id)
        if decision == "approve":
            self._audit(state, "promote_signal", "completed", signal_id=signal_id)
        state["final_case_report"] = nodes.write_report(state)
        self._audit(state, "generate_case_report", "completed")
        save_run_state(run_id, state)
        return state
