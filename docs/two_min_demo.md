# Two-Minute Demo

Use this when you need a fast portfolio walkthrough, stakeholder intro, or recorded
screen demo. It is designed to show the core architecture decisions without turning
into a full product tour.

## Goal

Show how Air-lab Fraud Agentic AI investigates a flagged fraud alert while keeping
data access, governance, signal promotion, and audit artifacts under deterministic
control.

## Setup

Start the dashboard before the demo:

```bash
streamlit run streamlit_app/fraud_case_dashboard.py --server.port 8890
```

Use case `A-1001` for the main path.

## 0:00-0:20 - Frame The Problem

Say:

> This is an enterprise AI architecture lab for fraud investigation. The goal is not
> to let an LLM make a fraud decision. The goal is to help an analyst investigate a
> model-flagged alert, retrieve evidence, propose a candidate signal, enforce
> governance checks, and require human approval before anything is promoted.

Show:

- `README.md` architecture diagram, or the dashboard home view
- the case queue with `A-1001`

## 0:20-0:50 - Run The Investigation

In the dashboard:

1. Select `A-1001`.
2. Run the investigation.
3. Point to the score, evidence, retrieved policy or typology context, and candidate
   signal.

Say:

> The dashboard is only a thin analyst workspace. It calls the service layer, which
> runs the workflow. The LLM can summarize and reason over approved evidence, but it
> never reads raw datasets directly and never executes unrestricted SQL.

## 0:50-1:20 - Show Governance And Human Review

Open the signal review and governance/audit sections.

Say:

> The system separates signal generation from signal promotion. Deterministic tools
> evaluate the candidate signal, run governance checks, and write audit evidence.
> The analyst still has to approve or reject the signal.

Then approve `A-1001-SIG-1` as `fraud_analyst_demo`.

Show:

- the approval result
- the audit trace entry for the analyst action
- approved signal registry state if visible

## 1:20-1:45 - Show Report And Trace

Open the report/export view.

Say:

> Every run produces a case report and JSON trace. That gives architecture reviewers
> evidence, source references, governance status, and an audit trail instead of a
> black-box answer.

Show:

- markdown report
- JSON run trace download or persisted run artifact

## 1:45-2:00 - Close With Enterprise Mapping

Say:

> Locally, this uses sample CSVs, markdown knowledge, a YAML signal registry, and a
> Streamlit dashboard. In an enterprise deployment, those boundaries map to governed
> data services, a feature or signal registry, an internal analyst portal, managed
> orchestration, and audit storage. The important design point is the control
> separation: the LLM assists investigation, but deterministic services and human
> reviewers control decisions.

## CLI Fallback

If the dashboard is unavailable, run:

```bash
python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001
python -m airlab_fraud_agentic_ai.cli review \
  --run-id <run_id> \
  --signal-id A-1001-SIG-1 \
  --decision approve \
  --reviewer fraud_analyst_demo
python -m airlab_fraud_agentic_ai.cli report --run-id <run_id>
python -m airlab_fraud_agentic_ai.cli monitor-signals
```

## What Not To Claim

- Do not describe sample monitoring proxies as production fraud validation.
- Do not imply the LLM has direct raw-data access.
- Do not imply the LLM makes final fraud decisions.
- Do not imply signal promotion can happen without analyst approval.
