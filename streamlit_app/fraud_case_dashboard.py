from __future__ import annotations

import json

import streamlit as st

from airlab_fraud_agentic_ai.config import get_settings
from airlab_fraud_agentic_ai.dashboard.service import (
    ask_case_question,
    export_run_trace,
    get_audit_trace,
    get_case_overview,
    get_signal_regression_summary,
    get_report,
    get_run_state,
    get_signal_monitoring_summary,
    list_case_queue,
    list_signal_registry_entries,
    run_investigation,
    submit_signal_decision,
)


st.set_page_config(page_title="Fraud Case Investigation Workflow", layout="wide")
st.title("Fraud Case Investigation Workflow")
st.caption("Business analyst workspace over the workflow service layer.")

if "run_id" not in st.session_state:
    st.session_state.run_id = None
if "run_id_input" not in st.session_state:
    st.session_state.run_id_input = ""
if "pending_run_id_input" not in st.session_state:
    st.session_state.pending_run_id_input = None

if st.session_state.pending_run_id_input is not None:
    st.session_state.run_id_input = st.session_state.pending_run_id_input
    st.session_state.pending_run_id_input = None

queue = list_case_queue()
settings = get_settings()
case_options = [item["alert_id"] for item in queue]
selected_case = st.sidebar.selectbox("Case Queue", options=case_options)
require_human_review = st.sidebar.toggle("Require human review", value=True)
llm_backend = st.sidebar.selectbox(
    "LLM Backend",
    options=["ollama", "fake"],
    index=0 if settings.llm_backend == "ollama" else 1,
)
st.sidebar.caption(f"Model: {settings.model_name}")

st.sidebar.divider()
st.sidebar.subheader("Run Loader")
st.sidebar.text_input("Load run by ID", key="run_id_input")
if st.sidebar.button("Load Run", use_container_width=True):
    requested_run_id = st.session_state.run_id_input.strip()
    if not requested_run_id:
        st.sidebar.warning("Enter a run ID first.")
    else:
        try:
            get_run_state(requested_run_id)
        except FileNotFoundError:
            st.sidebar.error(f"Run not found: {requested_run_id}")
        else:
            st.session_state.run_id = requested_run_id
            st.sidebar.success(f"Loaded run {requested_run_id}")

current_state = None
if st.session_state.run_id:
    try:
        current_state = get_run_state(st.session_state.run_id)
    except FileNotFoundError:
        st.session_state.run_id = None
        st.sidebar.error("Previously selected run could not be loaded.")
    else:
        st.sidebar.caption(
            f"Loaded run: {st.session_state.run_id} | status: {current_state.get('human_review_status', 'unknown')}"
        )

tabs = st.tabs(
    [
        "Case Queue",
        "Investigation Workspace",
        "Evidence Explorer",
        "Case Copilot",
        "Signal Review",
        "Governance & Audit",
        "Report & Export",
        "Signal Layer Monitor",
    ]
)

with tabs[0]:
    st.dataframe(queue, use_container_width=True)
    overview = get_case_overview(selected_case)
    st.json(overview)
    st.info(overview["threshold_summary"])

with tabs[1]:
    if st.button("Run Investigation", use_container_width=True):
        try:
            summary = run_investigation(
                selected_case,
                llm_backend=llm_backend,
                require_human_review=require_human_review,
            )
        except RuntimeError as exc:
            st.error(str(exc))
        else:
            st.session_state.run_id = summary["run_id"]
            st.session_state.pending_run_id_input = summary["run_id"]
            current_state = get_run_state(st.session_state.run_id)
    if current_state:
        cols = st.columns(3)
        cols[0].metric("Run ID", current_state["run_id"])
        cols[1].metric("Risk Level", current_state.get("risk_level", "unknown"))
        cols[2].metric("Human Review", current_state.get("human_review_status", "unknown"))
        st.json(current_state["audit_log"])
    else:
        st.info("Run an investigation or load an existing run to continue.")

with tabs[2]:
    if current_state:
        state = current_state
        st.subheader("Evidence Summary")
        st.write(state.get("evidence_summary", "Run an investigation first."))
        st.subheader("Retrieved Typologies")
        st.json(state.get("retrieved_typologies", []))
        st.subheader("Policies")
        st.json(state.get("retrieved_policies", []))
        st.subheader("Data Tool Results")
        st.json(
            {
                "customer_profile": state.get("customer_profile"),
                "transaction_summary": state.get("transaction_summary"),
                "behavioural_summary": state.get("behavioural_summary"),
                "feature_summary": state.get("feature_summary"),
            }
        )

with tabs[3]:
    if current_state:
        question = st.text_input("Ask a bounded case question", value="Why was this case flagged?")
        if st.button("Ask", key="ask_case"):
            st.json(ask_case_question(st.session_state.run_id, question))

with tabs[4]:
    if current_state:
        state = current_state
        st.subheader("Signal Candidates")
        st.json(state.get("signal_candidates", []))
        st.caption(
            f"Run {state['run_id']} is currently `{state.get('human_review_status', 'unknown')}`."
        )
        if state.get("human_review_status") == "pending_human_review":
            signal_ids = [signal["signal_id"] for signal in state.get("signal_candidates", [])]
            st.success("Human review is required. Approve or reject the candidate signal below.")
            with st.form("signal_decision_form"):
                selected_signal = st.selectbox("Signal", options=signal_ids)
                reviewer = st.text_input("Reviewer", value="fraud_analyst_demo")
                comments = st.text_input("Comments", value="")
                approve_col, reject_col = st.columns(2)
                approve_clicked = approve_col.form_submit_button("Approve Signal", use_container_width=True)
                reject_clicked = reject_col.form_submit_button("Reject Signal", use_container_width=True)
            if approve_clicked or reject_clicked:
                decision = "approve" if approve_clicked else "reject"
                result = submit_signal_decision(
                    st.session_state.run_id,
                    selected_signal,
                    decision,
                    reviewer,
                    comments,
                )
                st.session_state.run_id = result["run_id"]
                st.session_state.pending_run_id_input = result["run_id"]
                current_state = get_run_state(result["run_id"])
                st.success(f"Decision recorded: {result['human_review_status']}")
        else:
            st.info("No pending human-review action is required for the loaded run.")
    else:
        st.info("Load a run or start a new investigation to review candidate signals.")

with tabs[5]:
    if current_state:
        st.json(get_audit_trace(st.session_state.run_id))

with tabs[6]:
    if current_state:
        report = get_report(st.session_state.run_id)
        st.markdown(report)
        st.download_button("Download report", report, file_name=f"{st.session_state.run_id}.md")
        trace = export_run_trace(st.session_state.run_id)
        st.download_button("Download run trace", trace, file_name=f"{st.session_state.run_id}.json")

with tabs[7]:
    st.info("Monitoring metrics below are deterministic sample-data proxies only, not production fraud validation.")

    approved_registry = list_signal_registry_entries(status="approved")
    candidate_registry = list_signal_registry_entries(status="candidate")
    rejected_registry = list_signal_registry_entries(status="rejected")
    monitoring_cards = get_signal_monitoring_summary()
    regression_summary = get_signal_regression_summary()

    counts = st.columns(3)
    counts[0].metric("Approved Signals", len(approved_registry))
    counts[1].metric("Candidate Signals", len(candidate_registry))
    counts[2].metric("Rejected Signals", len(rejected_registry))

    if monitoring_cards:
        status_cols = st.columns(3)
        status_cols[0].metric("Stable", regression_summary["stable_count"])
        status_cols[1].metric("Decaying", regression_summary["decaying_count"])
        status_cols[2].metric("Failing", regression_summary["failing_count"])
        st.caption(
            f"Regression suite status: {regression_summary['overall_status']} | "
            f"{regression_summary['proxy_note']}"
        )

        st.subheader("Approved Signal Monitoring")
        for card in monitoring_cards:
            with st.expander(f"{card['signal_name']} ({card['monitoring_status']})", expanded=True):
                top = st.columns(4)
                top[0].metric("Coverage", f"{round(card['coverage_rate'] * 100)}%")
                top[1].metric("Fraud Lift", f"{card['fraud_lift']}x")
                top[2].metric("Freshness", f"{card['data_freshness_hours']}h")
                top[3].metric("Decay Score", card["signal_decay_score"])

                st.write(
                    {
                        "review_status": card["review_status"],
                        "reviewer": card["reviewer"],
                        "coverage_trend_proxy": card["coverage_trend_proxy"],
                        "fraud_lift_series": card["fraud_lift_series"],
                        "coverage_series": card["coverage_series"],
                        "false_positive_proxy": card["false_positive_proxy"],
                        "drift_proxy": card["drift_proxy"],
                        "governance_status": card["governance_status"],
                        "dataset_status": card["dataset_status"],
                        "source_tables": card["source_tables"],
                        "next_review_recommendation": card["next_review_recommendation"],
                    }
                )
                st.caption(card["proxy_note"])
    else:
        st.info("No approved signals are available for monitoring yet.")

    st.subheader("Candidate Registry")
    st.json(candidate_registry)
    st.subheader("Rejected Registry")
    st.json(rejected_registry)
