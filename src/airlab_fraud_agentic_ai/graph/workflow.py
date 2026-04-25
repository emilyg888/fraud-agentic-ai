from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from airlab_fraud_agentic_ai.config import get_settings
from airlab_fraud_agentic_ai.graph import nodes
from airlab_fraud_agentic_ai.graph.persistence import load_run_trace, save_run_artifacts
from airlab_fraud_agentic_ai.graph.routing import should_pause_for_human_review
from airlab_fraud_agentic_ai.graph.state import FraudInvestigationState
from airlab_fraud_agentic_ai.tools.registry_tools import (
    approve_signal,
    register_candidate_signals,
    reject_signal,
)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _audit_entry(step: str, status: str, **details: object) -> dict:
    return {
        "step": step,
        "status": status,
        "timestamp": _timestamp(),
        "details": details,
    }


def _append_audit(state: FraudInvestigationState, *entries: dict) -> list[dict]:
    return [*state.get("audit_log", []), *entries]


def _serialize_interrupts(snapshot: object) -> list[dict]:
    interrupts: list[dict] = []
    for task in getattr(snapshot, "tasks", ()) or ():
        for item in getattr(task, "interrupts", ()) or ():
            interrupts.append(
                {
                    "id": getattr(item, "id", None),
                    "value": getattr(item, "value", None),
                }
            )
    return interrupts


class FraudInvestigationWorkflow:
    def __init__(self) -> None:
        settings = get_settings()
        settings.runs_dir.mkdir(parents=True, exist_ok=True)
        settings.reports_dir.mkdir(parents=True, exist_ok=True)
        settings.checkpoint_db_path.parent.mkdir(parents=True, exist_ok=True)

        self._connection = sqlite3.connect(settings.checkpoint_db_path, check_same_thread=False)
        self._graph = self._build_graph(SqliteSaver(self._connection))

    def _config(self, run_id: str) -> dict:
        return {"configurable": {"thread_id": run_id}}

    def _build_graph(self, checkpointer: SqliteSaver):
        builder = StateGraph(FraudInvestigationState)

        builder.add_node("intake_case", self._intake_case)
        builder.add_node("classify_case_type", self._classify_case_type)
        builder.add_node("plan_investigation", self._plan_investigation)
        builder.add_node("retrieve_knowledge", self._retrieve_knowledge)
        builder.add_node("query_case_data", self._query_case_data)
        builder.add_node("summarise_evidence", self._summarise_evidence)
        builder.add_node("generate_signal_hypotheses", self._generate_signal_hypotheses)
        builder.add_node("evaluate_signals", self._evaluate_signals)
        builder.add_node("governance_check", self._governance_check)
        builder.add_node("register_candidates", self._register_candidates)
        builder.add_node("prepare_human_review", self._prepare_human_review)
        builder.add_node("human_review", self._human_review)
        builder.add_node("promote_signal", self._promote_signal)
        builder.add_node("generate_case_report", self._generate_case_report)

        builder.add_edge(START, "intake_case")
        builder.add_edge("intake_case", "classify_case_type")
        builder.add_edge("classify_case_type", "plan_investigation")
        builder.add_edge("plan_investigation", "retrieve_knowledge")
        builder.add_edge("retrieve_knowledge", "query_case_data")
        builder.add_edge("query_case_data", "summarise_evidence")
        builder.add_edge("summarise_evidence", "generate_signal_hypotheses")
        builder.add_edge("generate_signal_hypotheses", "evaluate_signals")
        builder.add_edge("evaluate_signals", "governance_check")
        builder.add_edge("governance_check", "register_candidates")
        builder.add_conditional_edges(
            "register_candidates",
            self._route_after_candidates,
            {
                "prepare_human_review": "prepare_human_review",
                "promote_signal": "promote_signal",
                "generate_case_report": "generate_case_report",
            },
        )
        builder.add_edge("prepare_human_review", "human_review")
        builder.add_edge("human_review", "generate_case_report")
        builder.add_edge("promote_signal", "generate_case_report")
        builder.add_edge("generate_case_report", END)
        return builder.compile(checkpointer=checkpointer)

    def _snapshot_state(self, run_id: str) -> dict:
        snapshot = self._graph.get_state(self._config(run_id))
        values = dict(getattr(snapshot, "values", {}) or {})
        if not values:
            trace = load_run_trace(run_id)
            return trace

        values["run_id"] = values.get("run_id", run_id)
        checkpoint_snapshot = {
            "next": list(getattr(snapshot, "next", ()) or ()),
            "config": getattr(snapshot, "config", {}),
            "interrupts": _serialize_interrupts(snapshot),
        }
        return save_run_artifacts(run_id, values, checkpoint_snapshot=checkpoint_snapshot)

    def _intake_case(self, state: FraudInvestigationState) -> dict:
        alert = nodes.intake_case(state["case_id"])
        return {
            "alert": alert,
            "analyst_request": alert["analyst_request"],
            "audit_log": _append_audit(
                state,
                _audit_entry("intake_case", "completed", case_id=state["case_id"]),
            ),
        }

    def _classify_case_type(self, state: FraudInvestigationState) -> dict:
        classification = nodes.classify(state["alert"])
        return {
            **classification,
            "audit_log": _append_audit(
                state,
                _audit_entry("classify_case_type", "completed", classification=classification),
            ),
        }

    def _plan_investigation(self, state: FraudInvestigationState) -> dict:
        plan = nodes.plan(state["alert"], {"case_type": state["case_type"], "risk_level": state["risk_level"]})
        return {
            "investigation_plan": [{"evidence_needed": item} for item in plan["evidence_needed"]],
            "audit_log": _append_audit(
                state,
                _audit_entry("plan_investigation", "completed", plan=plan),
            ),
        }

    def _retrieve_knowledge(self, state: FraudInvestigationState) -> dict:
        retrieved = nodes.retrieve(state["alert"], {"case_type": state["case_type"]})
        return {
            "retrieved_typologies": retrieved["fraud_typologies"],
            "retrieved_policies": retrieved["policies"],
            "retrieved_data_definitions": retrieved["data_dictionary"],
            "audit_log": _append_audit(
                state,
                _audit_entry(
                    "retrieve_knowledge",
                    "completed",
                    retrieved_counts={key: len(value) for key, value in retrieved.items()},
                ),
            ),
        }

    def _query_case_data(self, state: FraudInvestigationState) -> dict:
        case_data = nodes.query(state["alert"])
        return {
            **case_data,
            "audit_log": _append_audit(state, _audit_entry("query_case_data", "completed")),
        }

    def _summarise_evidence(self, state: FraudInvestigationState) -> dict:
        retrieved = {
            "fraud_typologies": state.get("retrieved_typologies", []),
            "policies": state.get("retrieved_policies", []),
            "data_dictionary": state.get("retrieved_data_definitions", []),
        }
        case_data = {
            "customer_profile": state.get("customer_profile"),
            "account_summary": state.get("account_summary"),
            "transaction_summary": state.get("transaction_summary"),
            "new_payee_activity": state.get("new_payee_activity"),
            "behavioural_summary": state.get("behavioural_summary"),
            "feature_summary": state.get("feature_summary"),
            "data_quality": state.get("data_quality"),
            "lineage": state.get("lineage"),
        }
        return {
            "evidence_summary": nodes.summarise(state["alert"], retrieved, case_data),
            "audit_log": _append_audit(state, _audit_entry("summarise_evidence", "completed")),
        }

    def _generate_signal_hypotheses(self, state: FraudInvestigationState) -> dict:
        case_data = {
            "customer_profile": state.get("customer_profile"),
            "account_summary": state.get("account_summary"),
            "transaction_summary": state.get("transaction_summary"),
            "new_payee_activity": state.get("new_payee_activity"),
            "behavioural_summary": state.get("behavioural_summary"),
            "feature_summary": state.get("feature_summary"),
            "data_quality": state.get("data_quality"),
            "lineage": state.get("lineage"),
        }
        candidates = nodes.hypothesise(
            state["alert"],
            {"case_type": state["case_type"], "risk_level": state["risk_level"]},
            case_data,
        )
        return {
            "signal_candidates": candidates,
            "audit_log": _append_audit(
                state,
                _audit_entry("generate_signal_hypotheses", "completed", candidate_count=len(candidates)),
            ),
        }

    def _evaluate_signals(self, state: FraudInvestigationState) -> dict:
        evaluations = nodes.evaluate(state.get("signal_candidates", []))
        return {
            "signal_evaluations": evaluations,
            "audit_log": _append_audit(
                state,
                _audit_entry("evaluate_signals", "completed", evaluation_count=len(evaluations)),
            ),
        }

    def _governance_check(self, state: FraudInvestigationState) -> dict:
        case_data = {
            "customer_profile": state.get("customer_profile"),
            "account_summary": state.get("account_summary"),
            "transaction_summary": state.get("transaction_summary"),
            "new_payee_activity": state.get("new_payee_activity"),
            "behavioural_summary": state.get("behavioural_summary"),
            "feature_summary": state.get("feature_summary"),
            "data_quality": state.get("data_quality"),
            "lineage": state.get("lineage"),
        }
        governance = nodes.govern(case_data, state.get("signal_candidates", []))
        return {
            "governance_findings": governance,
            "audit_log": _append_audit(
                state,
                _audit_entry("governance_check", "completed", governance=governance),
            ),
        }

    def _register_candidates(self, state: FraudInvestigationState) -> dict:
        candidate_entries = [
            {
                "run_id": state["run_id"],
                "case_id": state["case_id"],
                "status": "candidate",
                "reviewer": None,
                "comments": "",
                "signal": signal,
                "evaluation": next(
                    (item for item in state.get("signal_evaluations", []) if item["signal_name"] == signal["signal_name"]),
                    None,
                ),
                "governance": state.get("governance_findings", {}),
            }
            for signal in state.get("signal_candidates", [])
        ]
        if candidate_entries:
            register_candidate_signals(candidate_entries)
        return {}

    def _route_after_candidates(self, state: FraudInvestigationState) -> str:
        if should_pause_for_human_review(state, require_human_review=bool(state.get("require_human_review", True))):
            return "prepare_human_review"
        if state.get("signal_candidates"):
            return "promote_signal"
        return "generate_case_report"

    def _prepare_human_review(self, state: FraudInvestigationState) -> dict:
        request = {
            "instruction": "Review candidate signal and decide whether to approve or reject promotion.",
            "run_id": state["run_id"],
            "case_id": state["case_id"],
            "governance_status": state.get("governance_findings", {}).get("governance_status"),
            "candidate_signals": [
                {
                    "signal_id": signal["signal_id"],
                    "signal_name": signal["signal_name"],
                    "description": signal["description"],
                }
                for signal in state.get("signal_candidates", [])
            ],
        }
        draft_state = dict(state)
        draft_state["human_review_status"] = "pending_human_review"
        draft_state["human_review_request"] = request
        draft_report = nodes.write_report(draft_state)
        return {
            "human_review_status": "pending_human_review",
            "human_review_request": request,
            "final_case_report": draft_report,
            "audit_log": _append_audit(
                state,
                _audit_entry("human_review", "paused"),
                _audit_entry("generate_case_report", "completed", mode="draft"),
            ),
        }

    def _human_review(self, state: FraudInvestigationState) -> dict:
        decision = interrupt(state["human_review_request"])
        if not isinstance(decision, dict):
            raise ValueError("Human review resume payload must be a dictionary.")

        signal_id = str(decision.get("signal_id", "")).strip()
        action = str(decision.get("decision", "")).strip().lower()
        reviewer = str(decision.get("reviewer", "")).strip()
        comments = str(decision.get("comments", ""))

        candidate_ids = {signal["signal_id"] for signal in state.get("signal_candidates", [])}
        if signal_id not in candidate_ids:
            raise ValueError(f"Unknown signal_id: {signal_id}")
        if action not in {"approve", "reject"}:
            raise ValueError("decision must be 'approve' or 'reject'")
        if not reviewer:
            raise ValueError("reviewer is required")

        updates: dict = {
            "human_review_comments": comments,
            "audit_log": _append_audit(
                state,
                _audit_entry(
                    "human_review",
                    "completed",
                    decision=action,
                    reviewer=reviewer,
                    signal_id=signal_id,
                ),
            ),
        }

        if action == "approve":
            moved = approve_signal(signal_id=signal_id, reviewer=reviewer, comments=comments)
            updates["promoted_signals"] = [*state.get("promoted_signals", []), moved["signal"]]
            updates["human_review_status"] = "approved"
            updates["audit_log"] = _append_audit(
                state,
                _audit_entry(
                    "human_review",
                    "completed",
                    decision=action,
                    reviewer=reviewer,
                    signal_id=signal_id,
                ),
                _audit_entry("promote_signal", "completed", signal_id=signal_id),
            )
        else:
            reject_signal(signal_id=signal_id, reviewer=reviewer, comments=comments)
            updates["human_review_status"] = "rejected"

        return updates

    def _promote_signal(self, state: FraudInvestigationState) -> dict:
        approved_entries = [
            approve_signal(
                entry["signal"]["signal_id"],
                reviewer="system_auto",
                comments="Auto-approved for local demo.",
            )
            for entry in [
                {
                    "signal": signal,
                }
                for signal in state.get("signal_candidates", [])
            ]
        ]
        return {
            "promoted_signals": [entry["signal"] for entry in approved_entries],
            "human_review_status": "auto_approved" if approved_entries else state.get("human_review_status", "not_required"),
            "audit_log": _append_audit(
                state,
                _audit_entry("promote_signal", "completed", promoted_count=len(approved_entries)),
            ),
        }

    def _generate_case_report(self, state: FraudInvestigationState) -> dict:
        report = nodes.write_report(state)
        return {
            "final_case_report": report,
            "audit_log": _append_audit(state, _audit_entry("generate_case_report", "completed")),
        }

    def run_case(self, case_id: str, llm_provider: str = "fake", require_human_review: bool = True) -> dict:
        run_id = uuid4().hex[:12]
        settings = get_settings()
        initial_state: FraudInvestigationState = {
            "run_id": run_id,
            "case_id": case_id,
            "promoted_signals": [],
            "audit_log": [],
            "human_review_status": "not_required",
            "human_review_comments": None,
            "llm_provider": llm_provider,
            "model_name": settings.model_name,
            "require_human_review": require_human_review,
        }
        self._graph.invoke(initial_state, config=self._config(run_id))
        return self._snapshot_state(run_id)

    def submit_human_decision(
        self,
        run_id: str,
        signal_id: str,
        decision: str,
        reviewer: str,
        comments: str = "",
    ) -> dict:
        state = self.get_state(run_id)
        if state.get("human_review_status") != "pending_human_review":
            raise ValueError("Run is not waiting for human review.")

        self._graph.invoke(
            Command(
                resume={
                    "signal_id": signal_id,
                    "decision": decision,
                    "reviewer": reviewer,
                    "comments": comments,
                }
            ),
            config=self._config(run_id),
        )
        return self._snapshot_state(run_id)

    def get_state(self, run_id: str) -> dict:
        return self._snapshot_state(run_id)
