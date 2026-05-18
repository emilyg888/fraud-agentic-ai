# Demo Script

This script is designed for a short portfolio demo, architecture walkthrough, or user
testing session.

## 1. Business Problem

Explain the setup:

- A fraud model has flagged a case.
- The analyst needs more than a score.
- The system should retrieve evidence, query approved tools, propose a candidate signal,
  enforce governance, and require human approval before promotion.

## 2. Architecture Walkthrough

Open:

- `README.md`
- `docs/architecture_overview.md`
- `docs/langgraph_workflow.md`

Highlight:

- dashboard -> service layer -> workflow -> tools/registry/report
- deterministic tools own data access
- signal promotion is separated from signal generation

## 3. Start The Dashboard

```bash
streamlit run streamlit_app/fraud_case_dashboard.py --server.port 8890
```

## 4. Investigate A High-Risk Case

Use `A-1001`.

Show:

- case queue
- model score vs threshold
- evidence summary
- retrieved typologies
- signal candidate

## 5. Demonstrate Human Approval

In `Signal Review`:

- approve `A-1001-SIG-1`
- note that the dashboard is not promoting signals automatically
- show that the decision appears in the audit trail

## 6. Show The Report And Run Trace

Open `Report & Export` and show:

- markdown case report
- JSON run trace download
- persisted artifacts under `reports/` and `runs/`

## 7. Demonstrate A Governance-Sensitive Case

Use `A-1003`.

Explain:

- strong synthetic identity hypothesis
- governance caveat from stale/restricted feature evidence
- reviewer can reject instead of promote

## 8. Show Monitoring

Run:

```bash
python -m airlab_fraud_agentic_ai.cli monitor-signals
```

Explain:

- coverage and fraud-lift proxies
- drift proxy
- signal decay score
- monitoring recommendation

## 9. Explain Limitations

Be explicit:

- sample data only
- no production authentication or entitlements
- deterministic proxy monitoring
- enterprise-inspired architecture, not production infrastructure

## 10. Close With Enterprise Mapping

Open `docs/enterprise_mapping.md` and summarize:

- local components are placeholders for enterprise boundaries
- the value of the project is in the design decisions and control separation
- the repo is useful for architecture discussion, not just a UI demo
