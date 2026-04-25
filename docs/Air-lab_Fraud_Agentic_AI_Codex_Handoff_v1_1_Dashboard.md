# Air-lab Fraud Agentic AI — Phased Codex Handoff

**Project type:** Agentic fraud investigation and signal-discovery ecosystem  
**Primary tools:** Python, LangChain, LangGraph, governed RAG, BB_Datasets, deterministic data tools, human-in-the-loop approval, Streamlit business analyst dashboard  
**Target positioning:** Enterprise GenAI / ML platform architecture, AI-ready data platforms, semantic/feature/signal layers, governance-led AI for regulated enterprises  
**Version:** 1.1 — dashboard-enhanced  
**Prepared for:** Emily Gao  

---

## 0. Why this handoff exists

The original concept design is strong, but it is too broad to hand to Codex as one task. Codex will produce better work if the build is broken into sequenced, testable phases with clear context, constraints, and completion criteria.

Use this document as the **implementation handoff** for Codex. Each phase includes:

- Objective
- Files to create or modify
- Concrete implementation tasks
- Acceptance criteria
- Suggested Codex prompt
- Phase gate before moving to the next phase
- Dashboard requirements where the business analyst needs to interact with the system

This project should be built as a **portfolio-grade enterprise AI architecture lab**, not as a production fraud system.

---

## 1. Business objective

Build an agentic fraud investigation and signal-discovery assistant that helps a fraud analyst investigate an ML-flagged case by orchestrating:

1. ML alert intake
2. investigation planning
3. retrieval over fraud typologies, policy documents, data definitions, and historical case notes
4. approved data-tool queries over BB_Datasets
5. evidence summarisation
6. candidate fraud signal generation
7. signal evaluation
8. governance checks
9. human-in-the-loop approval
10. signal promotion into a governed Signal Layer
11. monitoring of signal drift, false positives, and signal decay

### MVP business scenario

An ML model flags an alert:

> Investigate alert A-1001. Explain why the case was flagged, compare it to known fraud typologies, check behavioural and transaction signals, and recommend whether the case should be escalated, closed, or monitored.

### Enterprise-safe design principle

> The LLM reasons and explains, but deterministic tools retrieve, query, evaluate, govern, and promote.

This is the most important architecture rule in the project.

---

## 2. What this project should prove

This project is designed to prove that you can architect an **Agentic AI ecosystem**, not merely build a chatbot.

| Capability | Evidence in this project |
|---|---|
| LangChain | Tool definitions, retriever integration, prompt orchestration, structured outputs |
| LangGraph | StateGraph, nodes, edges, conditional routing, persistence, human interrupts |
| Agentic RAG | Agent retrieves knowledge only when needed and grounds outputs in retrieved context |
| Governed data access | LLM cannot access raw data or write arbitrary SQL |
| Signal Layer | Candidate fraud signals are evaluated, governed, approved, and promoted |
| Responsible AI | Privacy, lineage, data quality, explainability, auditability, and human approval |
| Enterprise architecture | Local-first build maps to AWS Bedrock, Lambda, API Gateway, Snowflake, SageMaker Feature Store, model monitoring, and enterprise observability |

---

## 3. Recommended repository name

```text
airlab-fraud-agentic-ai
```

Alternative:

```text
air-lab-fraud-agentic-ai
```

Use one repository for this project. Keep it focused and polished.

---

## 4. Codex operating instructions

### 4.1 Do not ask Codex to build the whole project in one pass

Use one phase at a time.

Bad prompt:

```text
Build the whole Air-lab Fraud Agentic AI project.
```

Better prompt:

```text
Read AGENTS.md and Air-lab_Fraud_Agentic_AI_Codex_Handoff.md. Implement Phase 1 only. Do not start Phase 2. Create tests and run them before finishing.
```

### 4.2 Recommended Codex prompt structure

For every task, give Codex:

1. **Goal** — what to build
2. **Context** — which files and phase matter
3. **Constraints** — architecture and safety rules
4. **Done when** — tests, demo output, files created

### 4.3 Use Plan Mode for complex phases

For Phase 3 onward, ask Codex to plan first before coding:

```text
Before editing code, produce a short implementation plan for this phase. Wait for review if the plan reveals ambiguity. Then implement only this phase.
```

### 4.4 Keep human approval between phases

After each phase:

- inspect the diff
- run tests
- run the demo command for that phase
- update README if needed
- commit changes
- only then start the next phase

---

## 5. Repository-level AGENTS.md for Codex

Create this file at repository root in Phase 0.

```markdown
# AGENTS.md

## Project identity

This repository is an enterprise AI architecture lab called Air-lab Fraud Agentic AI.
It demonstrates agentic fraud investigation, governed RAG, deterministic data tools,
signal evaluation, governance checks, human-in-the-loop approval, signal promotion, and a business analyst dashboard.

## Core architecture rules

1. The LLM must never directly access raw datasets.
2. The LLM must never generate or execute unrestricted SQL.
3. The LLM must never make final fraud decisions.
4. The LLM must never promote signals without human approval.
5. Deterministic tools enforce data access, evaluation, governance, and registry writes.
6. Use fake/sample data only. Do not use real customer PII.
7. All outputs must include evidence, source references, and audit trace.
8. Tests must not require paid API keys.
9. Any LLM-dependent code must have a fake/test implementation.
10. Keep the project local-first but document enterprise mappings to AWS/Snowflake.
11. Dashboard code must call workflow/service functions only; it must not duplicate investigation, governance, or registry logic.
12. Every analyst action in the dashboard, especially approve/reject/edit, must be captured in the audit trace.

## Engineering conventions

- Use Python 3.11+.
- Prefer small, typed modules.
- Use Pydantic models for contracts and validation.
- Use pytest for unit and workflow tests.
- Keep CLI demos working after every phase.
- Update README.md when adding major capability.
- Avoid overbuilding production infrastructure.

## Definition of done for every Codex task

- Relevant tests are added or updated.
- `pytest` passes.
- The phase demo command works.
- No secrets or real PII are committed.
- README or docs are updated if behaviour changes.
- The task stays within the requested phase.
```

---

## 6. Target repository structure

Build toward this structure progressively. Do not create all implementation files empty; create them as each phase requires.

```text
airlab-fraud-agentic-ai/
  AGENTS.md
  README.md
  pyproject.toml
  requirements.txt
  .env.example
  .gitignore

  docs/
    architecture_overview.md
    langgraph_workflow.md
    governance_model.md
    signal_layer_design.md
    enterprise_mapping.md
    codex_handoff.md

  data/
    README.md
    sample/
      alerts.csv
      customers.csv
      accounts.csv
      transactions.csv
      behavioural_events.csv
      features.csv
      historical_cases.csv
      data_quality.csv
      lineage.csv
    bb_dataset_mapping.yaml

  knowledge/
    fraud_typologies/
      account_takeover.md
      mule_account.md
      scam_payment.md
      synthetic_identity.md
    policies/
      fraud_escalation_policy.md
      data_privacy_policy.md
      signal_promotion_policy.md
    data_dictionary/
      transaction_features.md
      behavioural_features.md
      model_features.md

  signal_registry/
    candidate_signals.yaml
    approved_signals.yaml
    rejected_signals.yaml

  reports/
    .gitkeep

  runs/
    .gitkeep

  src/
    airlab_fraud_agentic_ai/
      __init__.py
      cli.py
      config.py

      data/
        contracts.py
        loaders.py
        bb_adapter.py

      tools/
        alert_tools.py
        bb_dataset_tools.py
        retrieval_tools.py
        signal_eval_tools.py
        governance_tools.py
        registry_tools.py

      rag/
        ingest.py
        retriever.py
        vector_store.py

      graph/
        state.py
        nodes.py
        routing.py
        workflow.py
        persistence.py

      agents/
        llm_factory.py
        prompts.py
        planner.py
        classifier.py
        evidence_summariser.py
        signal_hypothesis.py
        case_report_writer.py

      governance/
        lineage_check.py
        data_quality_check.py
        privacy_check.py
        explainability_check.py

      signal_layer/
        schema.py
        registry.py
        monitoring.py

      evaluation/
        signal_metrics.py
        case_report_eval.py
        regression_tests.py

      dashboard/
        models.py
        service.py
        view_models.py

  streamlit_app/
    fraud_case_dashboard.py
    README.md

  tests/
    test_project_structure.py
    test_data_contracts.py
    test_bb_dataset_tools.py
    test_rag_retriever.py
    test_graph_workflow.py
    test_signal_evaluation.py
    test_governance_checks.py
    test_human_review.py
    test_dashboard_service.py
```

---

## 7. Whole-project definition of done

The full project is complete when:

1. A user can run a CLI command such as:

   ```bash
   python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001
   ```

2. The workflow:

   - loads an ML alert
   - classifies likely fraud typology
   - plans required evidence
   - retrieves relevant fraud typologies and policies
   - queries approved BB_Datasets tools
   - summarises case evidence
   - generates candidate signals
   - evaluates signal usefulness
   - runs governance checks
   - pauses for human review before promotion
   - promotes approved signals to the Signal Layer
   - generates a Markdown case report
   - writes an audit trace
   - exposes the same workflow through a business analyst dashboard

3. The dashboard lets an analyst select a case, run an investigation, inspect evidence, ask bounded case questions, approve/reject candidate signals, download the report, and view audit trace.

4. Tests pass without an external LLM key.

5. README contains:

   - business objective
   - architecture diagram
   - setup instructions
   - demo instructions
   - governance rules
   - enterprise mapping
   - sample report

6. The repository is polished enough to pin on GitHub and add as a LinkedIn project.

---

## 8. Dashboard component design

The project should include a business analyst dashboard so a fraud analyst can interact with the agentic system without using the CLI.

The dashboard is a **controlled interaction layer** over the existing LangGraph workflow, approved data tools, RAG retriever, human-review functions, Signal Layer registry, report generator, and audit trace. It is not a separate fraud application and must not duplicate the investigation logic.

### 8.1 Dashboard objective

Build an interactive analyst workspace that supports this user journey:

1. Analyst selects an ML-flagged fraud case from a case queue.
2. Analyst reviews alert details, model score, threshold, and triggered features.
3. Analyst starts the agentic investigation workflow.
4. Dashboard shows workflow progress and node-level status.
5. Analyst reviews retrieved typologies, policy snippets, data definitions, and similar case context.
6. Analyst reviews deterministic data-tool results: customer, transaction, behavioural, feature, lineage, and data quality summaries.
7. Analyst asks bounded case questions through a governed copilot panel.
8. Analyst reviews candidate fraud signals, signal evaluation metrics, and governance findings.
9. Analyst approves, rejects, or requests edit for signal promotion.
10. Dashboard writes the decision to the audit trail and resumes the workflow.
11. Analyst views or downloads the final case report.
12. Analyst reviews promoted signals and monitoring status.

### 8.2 Dashboard tabs

Use Streamlit tabs in a single app first. Multipage Streamlit can be added later, but the MVP should stay simple.

| Tab | Purpose | Required content |
|---|---|---|
| **Case Queue** | Select an alert to investigate | Case ID, customer ID, model score, threshold, triggered features, current status |
| **Investigation Workspace** | Run and inspect the agentic workflow | Run button, workflow progress, node status, latest state summary |
| **Evidence Explorer** | Review retrieved and queried evidence | Fraud typologies, policy snippets, data dictionary, data-tool summaries |
| **Case Copilot** | Ask bounded questions about the current case | Question box, suggested questions, answer with evidence references and limitations |
| **Signal Review** | Review and decide on candidate signals | Candidate signal cards, metrics, governance findings, approve/reject/edit controls |
| **Governance & Audit** | Show control evidence | Lineage, data quality, privacy, explainability, approval status, audit trace |
| **Report & Export** | View and download outputs | Markdown report, report download, run trace download |
| **Signal Layer Monitor** | Review approved/rejected/candidate signals | Signal registry, drift proxy, false-positive proxy, decay status, review recommendation |

### 8.3 Dashboard service layer

Do not put business logic directly into Streamlit widgets. Create a dashboard service layer under:

```text
src/airlab_fraud_agentic_ai/dashboard/
  models.py
  service.py
  view_models.py
```

The Streamlit app should call these service functions:

```python
def list_case_queue() -> list[dict]: ...
def get_case_overview(case_id: str) -> dict: ...
def run_investigation(case_id: str, llm_provider: str = "fake", require_human_review: bool = True) -> dict: ...
def get_run_state(run_id: str) -> dict: ...
def ask_case_question(run_id: str, question: str) -> dict: ...
def submit_signal_decision(run_id: str, signal_id: str, decision: str, reviewer: str, comments: str = "") -> dict: ...
def get_report(run_id: str) -> str: ...
def get_audit_trace(run_id: str) -> dict: ...
def list_signal_registry(status: str | None = None) -> list[dict]: ...
def get_signal_monitoring_summary() -> list[dict]: ...
```

This service layer makes the dashboard testable without Streamlit UI automation.

### 8.4 Dashboard interaction rules

The dashboard must obey the same enterprise-safe rules as the CLI:

1. It must not expose raw tables.
2. It must not allow arbitrary SQL.
3. It must not let the LLM approve or promote signals.
4. Approve/reject/edit decisions must be submitted by a human user action.
5. All approval actions must be logged with reviewer, decision, timestamp, signal ID, and comments.
6. Copilot answers must use current case state, retrieved knowledge, and approved tool outputs only.
7. Copilot answers must show evidence references and limitations.
8. Dashboard must use sample data only.
9. Default LLM provider must remain `fake`.
10. CLI and tests must continue to work after dashboard changes.

### 8.5 Suggested dashboard questions

Add preset questions so the analyst can use the copilot without inventing prompts:

```text
Why was this case flagged?
Which fraud typologies are most relevant?
What evidence supports account takeover risk?
What evidence weakens the fraud hypothesis?
Which triggered features are most important?
Are there data quality or lineage concerns?
Should this signal be promoted, monitored, or rejected?
What should the analyst do next?
```

### 8.6 Dashboard visual elements

Keep visuals simple and business-facing:

- model score versus threshold metric card
- risk level badge
- workflow progress/status table
- triggered feature list
- evidence table
- retrieved source snippets with source paths
- signal candidate cards
- governance status badges: pass, conditional pass, fail
- audit trace table
- markdown report viewer
- download buttons for report and run trace
- signal monitoring table

Optional later enhancements:

- trend chart for signal coverage over time
- false-positive proxy chart
- signal decay status chart
- node execution timeline

### 8.7 Dashboard definition of done

The dashboard component is complete when a business analyst can:

1. select `A-1001` from the case queue;
2. run the investigation from the UI;
3. see alert, evidence, retrieval, candidate signals, governance findings, and report;
4. ask at least three bounded copilot questions about the current case;
5. approve or reject a candidate signal from the UI;
6. see the Signal Layer registry update after the decision;
7. download the case report;
8. view the audit trace showing workflow nodes, tool calls, retrieval sources, governance checks, and human decision;
9. run the Streamlit app without needing a paid LLM key;
10. still run all CLI workflows and tests successfully.

### 8.8 Dashboard business analyst demo script

Use this script for LinkedIn/GitHub screenshots:

1. Open dashboard.
2. Select case `A-1001`.
3. Point out model score, threshold, and triggered features.
4. Click **Run Investigation**.
5. Show workflow progress: intake → classify → plan → retrieve → query data → summarise → generate signal → evaluate → governance.
6. Open Evidence Explorer and show retrieved account takeover typology and policy evidence.
7. Ask: “Why was this case flagged?”
8. Show answer with evidence references.
9. Open Signal Review and review `new_device_high_value_new_payee_velocity`.
10. Show evaluation and governance status.
11. Approve signal promotion as `fraud_analyst_demo`.
12. Show Signal Layer registry update.
13. Open final report and download it.
14. Open Governance & Audit to show decision trace.

# Build Phases

---

## Phase 0 — Bootstrap repository and project standards

### Objective

Create the repository skeleton, development environment, AGENTS.md, README, sample folders, and test baseline.

### Files to create

```text
AGENTS.md
README.md
pyproject.toml
requirements.txt
.env.example
.gitignore
docs/codex_handoff.md
data/README.md
reports/.gitkeep
runs/.gitkeep
src/airlab_fraud_agentic_ai/__init__.py
src/airlab_fraud_agentic_ai/cli.py
tests/test_project_structure.py
```

### Concrete tasks for Codex

1. Create a Python package called `airlab_fraud_agentic_ai`.
2. Add `pyproject.toml` with:
   - Python 3.11+
   - pytest
   - pydantic
   - pandas
   - pyyaml
   - typer or argparse
   - rich optional
3. Add `.gitignore` for Python, virtual environments, cache files, `.env`, generated vector stores, and run outputs.
4. Add `.env.example` with placeholders only:
   - `OPENAI_API_KEY=`
   - `LOCAL_LLM_PROVIDER=`
   - `MODEL_NAME=`
5. Create `AGENTS.md` using the content in Section 5.
6. Create initial README with:
   - project purpose
   - business objective
   - key architecture rule
   - build phases
   - governance warning: sample data only
7. Create CLI placeholder:

   ```bash
   python -m airlab_fraud_agentic_ai.cli --help
   ```

8. Add a structure test that verifies required top-level folders exist.

### Acceptance criteria

- `pytest` passes.
- CLI help command works.
- README clearly states this is not a production fraud system.
- No implementation beyond Phase 0 is started.

### Suggested Codex prompt

```text
Read AGENTS.md requirements from this handoff. Implement Phase 0 only.

Goal: bootstrap the Air-lab Fraud Agentic AI repository.
Context: use the Phase 0 section of docs/codex_handoff.md.
Constraints: do not implement RAG, LangGraph, tools, or agents yet. Create only repo skeleton, README, AGENTS.md, pyproject, CLI placeholder, and tests.
Done when: pytest passes and `python -m airlab_fraud_agentic_ai.cli --help` works.
```

### Phase gate

Commit message:

```text
phase-0 bootstrap repo and codex instructions
```

---

## Phase 1 — Data contracts, sample BB_Datasets adapter, and approved data tools

### Objective

Create deterministic, approved data tools over BB_Datasets or sample data. This phase teaches the core governance pattern: **LLMs use approved tools; they do not access raw tables directly.**

### Files to create or modify

```text
data/sample/alerts.csv
data/sample/customers.csv
data/sample/accounts.csv
data/sample/transactions.csv
data/sample/behavioural_events.csv
data/sample/features.csv
data/sample/historical_cases.csv
data/sample/data_quality.csv
data/sample/lineage.csv
data/bb_dataset_mapping.yaml
src/airlab_fraud_agentic_ai/data/contracts.py
src/airlab_fraud_agentic_ai/data/loaders.py
src/airlab_fraud_agentic_ai/data/bb_adapter.py
src/airlab_fraud_agentic_ai/tools/alert_tools.py
src/airlab_fraud_agentic_ai/tools/bb_dataset_tools.py
tests/test_data_contracts.py
tests/test_bb_dataset_tools.py
```

### Sample data requirements

Create at least three cases:

| Case | Purpose |
|---|---|
| `A-1001` | High-risk case with device change, new payee, high-value transfer |
| `A-1002` | Medium-risk case with transaction velocity but no device change |
| `A-1003` | Governance-fail case with incomplete lineage or data quality issue |

### Required data contracts

Create Pydantic models for:

- `Alert`
- `CustomerProfile`
- `Account`
- `TransactionEvent`
- `BehaviouralEvent`
- `FeatureValue`
- `HistoricalCase`
- `DataQualityRecord`
- `LineageRecord`

Example fields:

```python
class Alert(BaseModel):
    alert_id: str
    customer_id: str
    alert_time: datetime
    model_score: float
    threshold: float
    triggered_features: list[str]
    model_version: str
```

### Approved tool functions

Create deterministic functions:

```python
def get_alert(alert_id: str) -> dict: ...
def get_customer_profile(customer_id: str) -> dict: ...
def get_transaction_summary(customer_id: str, window_days: int = 7) -> dict: ...
def get_new_payee_activity(customer_id: str, window_days: int = 7) -> dict: ...
def get_device_change_summary(customer_id: str, window_days: int = 7) -> dict: ...
def get_feature_values(alert_id: str) -> dict: ...
def get_lineage_for_features(feature_names: list[str]) -> dict: ...
def get_data_quality_for_sources(source_names: list[str]) -> dict: ...
```

### BB_Datasets mapping

Create `data/bb_dataset_mapping.yaml`:

```yaml
logical_datasets:
  alerts:
    type: csv
    path: data/sample/alerts.csv
    key: alert_id
  customers:
    type: csv
    path: data/sample/customers.csv
    key: customer_id
  transactions:
    type: csv
    path: data/sample/transactions.csv
    key: transaction_id
  behavioural_events:
    type: csv
    path: data/sample/behavioural_events.csv
    key: event_id
  features:
    type: csv
    path: data/sample/features.csv
    key: feature_name
  historical_cases:
    type: csv
    path: data/sample/historical_cases.csv
    key: case_id
  data_quality:
    type: csv
    path: data/sample/data_quality.csv
    key: dataset_name
  lineage:
    type: csv
    path: data/sample/lineage.csv
    key: field_name
```

The adapter should be able to later point to your real BB_Datasets without changing agent logic.

### CLI command

Add:

```bash
python -m airlab_fraud_agentic_ai.cli inspect-data --case-id A-1001
```

Expected output:

- alert summary
- customer summary
- transaction summary
- behavioural summary
- triggered features

### Acceptance criteria

- Tool functions return JSON-serialisable dictionaries.
- `A-1001`, `A-1002`, and `A-1003` all load successfully.
- `pytest` passes.
- No LLM calls are used in this phase.
- CLI demo command works.

### Suggested Codex prompt

```text
Implement Phase 1 only.

Goal: create data contracts, sample BB_Datasets files, adapter, and approved deterministic data tools.
Context: use Phase 1 in docs/codex_handoff.md. The LLM must never access raw datasets directly; later agents will call these tools.
Constraints: no LangChain, no LangGraph, no LLM calls yet. Use Pydantic models and JSON-serialisable outputs. Include three sample cases A-1001, A-1002, A-1003.
Done when: `pytest` passes and `python -m airlab_fraud_agentic_ai.cli inspect-data --case-id A-1001` prints alert, customer, transaction, behavioural, feature, lineage, and data quality summaries.
```

### Phase gate

Commit message:

```text
phase-1 add bb dataset contracts and approved tools
```

---

## Phase 2 — Fraud knowledge base and RAG retriever

### Objective

Build a small fraud knowledge base and retrieval layer for fraud typologies, policies, data definitions, and model notes.

This phase introduces **LangChain retrieval** while keeping generation optional.

### Files to create or modify

```text
knowledge/fraud_typologies/account_takeover.md
knowledge/fraud_typologies/mule_account.md
knowledge/fraud_typologies/scam_payment.md
knowledge/fraud_typologies/synthetic_identity.md
knowledge/policies/fraud_escalation_policy.md
knowledge/policies/data_privacy_policy.md
knowledge/policies/signal_promotion_policy.md
knowledge/data_dictionary/transaction_features.md
knowledge/data_dictionary/behavioural_features.md
knowledge/data_dictionary/model_features.md
src/airlab_fraud_agentic_ai/rag/ingest.py
src/airlab_fraud_agentic_ai/rag/vector_store.py
src/airlab_fraud_agentic_ai/rag/retriever.py
src/airlab_fraud_agentic_ai/tools/retrieval_tools.py
tests/test_rag_retriever.py
```

### Knowledge document requirements

Each fraud typology document should include:

- description
- common indicators
- relevant customer signals
- relevant transaction signals
- relevant behavioural signals
- false positive risks
- analyst questions

Example typologies:

1. Account takeover
2. Mule account activity
3. Scam-induced payment
4. Synthetic identity

### Retriever requirements

Create a retriever that can answer queries such as:

```text
What typologies are relevant when a customer changes device and sends high-value payments to a new payee within 24 hours?
```

Implementation options:

- Preferred: LangChain document objects + local vector store such as Chroma or FAISS.
- Fallback: deterministic keyword retriever for tests.

Tests must not depend on paid API keys. If embeddings require an API, provide a fake embedding or deterministic fallback.

### Retrieval tool

Create:

```python
def retrieve_fraud_knowledge(query: str, top_k: int = 4) -> list[dict]: ...
```

Each result should include:

- title
- source path
- content snippet
- score if available
- document type: typology, policy, data_dictionary, model_doc

### CLI command

Add:

```bash
python -m airlab_fraud_agentic_ai.cli search-knowledge "device change new payee high value transfer"
```

### Acceptance criteria

- At least 10 knowledge documents exist.
- Retriever returns relevant typology and policy snippets.
- Tests pass without external API keys.
- CLI search command works.
- README updated with RAG explanation.

### Suggested Codex prompt

```text
Implement Phase 2 only.

Goal: add fraud knowledge documents and a local RAG retriever.
Context: Phase 2 in docs/codex_handoff.md. Phase 1 data tools already exist.
Constraints: tests must not require external LLM or embedding API keys. Use a deterministic fallback retriever or fake embeddings if needed. Do not implement LangGraph workflow yet.
Done when: `pytest` passes and `python -m airlab_fraud_agentic_ai.cli search-knowledge "device change new payee high value transfer"` returns relevant typology/policy snippets with source paths.
```

### Phase gate

Commit message:

```text
phase-2 add fraud knowledge rag retriever
```

---

## Phase 3 — LangGraph deterministic workflow skeleton

### Objective

Create the core LangGraph workflow with state, nodes, edges, and conditional routing. Use deterministic placeholder nodes first. Do not introduce LLM calls yet.

### Files to create or modify

```text
src/airlab_fraud_agentic_ai/graph/state.py
src/airlab_fraud_agentic_ai/graph/nodes.py
src/airlab_fraud_agentic_ai/graph/routing.py
src/airlab_fraud_agentic_ai/graph/workflow.py
src/airlab_fraud_agentic_ai/graph/persistence.py
tests/test_graph_workflow.py
docs/langgraph_workflow.md
```

### Required state object

Create a typed graph state similar to:

```python
class FraudInvestigationState(TypedDict, total=False):
    case_id: str
    analyst_request: str
    alert: dict
    case_type: str
    risk_level: str
    investigation_plan: list[dict]
    retrieved_knowledge: list[dict]
    customer_profile: dict
    transaction_summary: dict
    behavioural_summary: dict
    feature_summary: dict
    evidence_summary: str
    signal_candidates: list[dict]
    signal_evaluations: list[dict]
    governance_findings: dict
    human_review_status: str
    human_review_comments: str
    promoted_signals: list[dict]
    final_case_report: str
    audit_log: list[dict]
```

### Required nodes

Start with deterministic implementations:

```text
intake_case
classify_case_type
plan_investigation
retrieve_knowledge
query_case_data
summarise_evidence
generate_signal_hypotheses
evaluate_signals
governance_check
route_after_governance
generate_case_report
```

Do not add human interrupt yet. That is Phase 6.

### Required graph flow

```text
START
  -> intake_case
  -> classify_case_type
  -> plan_investigation
  -> retrieve_knowledge
  -> query_case_data
  -> summarise_evidence
  -> generate_signal_hypotheses
  -> evaluate_signals
  -> governance_check
  -> generate_case_report
  -> END
```

### CLI command

Add:

```bash
python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001 --deterministic
```

### Acceptance criteria

- Graph compiles.
- Workflow runs end-to-end for `A-1001`.
- State contains all major fields after execution.
- Report is generated in memory or written to `reports/`.
- Tests verify node order and required state fields.
- No LLM calls yet.

### Suggested Codex prompt

```text
Implement Phase 3 only.

Goal: create a deterministic LangGraph workflow skeleton for fraud investigation.
Context: Phase 1 data tools and Phase 2 retriever already exist. Use them inside graph nodes.
Constraints: no LLM calls yet. Use deterministic placeholder logic. The graph must compile and run end-to-end for A-1001. Do not implement human interrupts yet.
Done when: pytest passes and `python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001 --deterministic` runs the graph and prints or writes a case report.
```

### Phase gate

Commit message:

```text
phase-3 add deterministic langgraph workflow
```

---

## Phase 4 — LLM agents, prompts, structured outputs, and fake model fallback

### Objective

Replace deterministic placeholders with controlled LLM-assisted nodes while preserving testability through fake model implementations.

### Files to create or modify

```text
src/airlab_fraud_agentic_ai/agents/llm_factory.py
src/airlab_fraud_agentic_ai/agents/prompts.py
src/airlab_fraud_agentic_ai/agents/classifier.py
src/airlab_fraud_agentic_ai/agents/planner.py
src/airlab_fraud_agentic_ai/agents/evidence_summariser.py
src/airlab_fraud_agentic_ai/agents/signal_hypothesis.py
src/airlab_fraud_agentic_ai/agents/case_report_writer.py
src/airlab_fraud_agentic_ai/graph/nodes.py
tests/test_graph_workflow.py
tests/test_llm_agents_fake.py
```

### LLM factory requirements

Create a model abstraction that supports:

- `fake` provider for tests and demos
- optional OpenAI-compatible provider
- optional local provider placeholder for Ollama / LM Studio

Environment variables:

```text
LLM_PROVIDER=fake|openai|local
MODEL_NAME=
OPENAI_API_KEY=
```

Default must be `fake`.

### Structured outputs

Create Pydantic models for LLM outputs:

- `CaseClassification`
- `InvestigationPlan`
- `EvidenceSummary`
- `SignalHypothesis`
- `CaseReportSections`

Do not accept free-form JSON without validation.

### Agent behaviours

#### Classifier agent

Input:

- alert
- triggered features
- transaction summary
- behavioural summary

Output:

- case_type
- risk_level
- confidence
- rationale

#### Planner agent

Input:

- case type
- risk level
- alert

Output:

- evidence needed
- tools to call
- retrieval queries
- whether human approval is needed

#### Evidence summariser

Input:

- retrieved knowledge
- case data summaries

Output:

- grounded summary
- evidence table
- missing evidence

#### Signal hypothesis agent

Input:

- evidence summary
- feature values
- typology context

Output:

- candidate signals
- source features
- expected risk direction
- business explanation

#### Report writer

Input:

- full state

Output:

- Markdown case report

### Acceptance criteria

- Fake provider produces deterministic test outputs.
- Optional real provider is wired but not required for tests.
- LLM outputs are schema-validated.
- Existing deterministic run mode still works.
- LLM-assisted run works with fake provider.

### CLI command

```bash
python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001 --llm-provider fake
```

### Suggested Codex prompt

```text
Implement Phase 4 only.

Goal: add LLM-assisted agents with structured outputs and a fake model fallback.
Context: Phase 3 deterministic LangGraph workflow exists. Replace selected placeholder logic with agent modules, but keep deterministic/fake testability.
Constraints: tests must not require an API key. Default provider must be fake. All LLM outputs must be validated with Pydantic models. Do not add human interrupts yet.
Done when: pytest passes and `python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001 --llm-provider fake` runs end-to-end with schema-validated outputs.
```

### Phase gate

Commit message:

```text
phase-4 add llm agents with fake provider
```

---

## Phase 5 — Signal evaluation, governance checks, and Signal Layer registry

### Objective

Make the Signal Layer real. Add deterministic signal evaluation, governance checks, and registries for candidate, approved, and rejected signals.

### Files to create or modify

```text
src/airlab_fraud_agentic_ai/evaluation/signal_metrics.py
src/airlab_fraud_agentic_ai/governance/lineage_check.py
src/airlab_fraud_agentic_ai/governance/data_quality_check.py
src/airlab_fraud_agentic_ai/governance/privacy_check.py
src/airlab_fraud_agentic_ai/governance/explainability_check.py
src/airlab_fraud_agentic_ai/signal_layer/schema.py
src/airlab_fraud_agentic_ai/signal_layer/registry.py
src/airlab_fraud_agentic_ai/tools/signal_eval_tools.py
src/airlab_fraud_agentic_ai/tools/governance_tools.py
src/airlab_fraud_agentic_ai/tools/registry_tools.py
signal_registry/candidate_signals.yaml
signal_registry/approved_signals.yaml
signal_registry/rejected_signals.yaml
tests/test_signal_evaluation.py
tests/test_governance_checks.py
```

### Candidate signal schema

Create a Pydantic model similar to:

```python
class CandidateSignal(BaseModel):
    signal_name: str
    fraud_typology: str
    description: str
    source_features: list[str]
    expected_direction: str
    business_rationale: str
```

### Evaluation output schema

```python
class SignalEvaluation(BaseModel):
    signal_name: str
    coverage_rate: float
    fraud_lift: float
    false_positive_risk: str
    stability_score: float
    explainability_score: int
    data_quality_status: str
    recommendation: str
```

### Governance output schema

```python
class GovernanceFinding(BaseModel):
    governance_status: str
    lineage_status: str
    data_quality_status: str
    privacy_status: str
    explainability_status: str
    approval_required: bool
    comments: str
```

### Evaluation metrics

Implement simple deterministic proxy metrics:

- coverage rate
- fraud lift proxy
- false-positive risk proxy
- stability score
- explainability score
- data quality pass/fail
- recommendation

### Governance checks

Implement:

1. lineage check
2. data quality check
3. privacy check
4. explainability check
5. approval requirement check

### Registry behaviours

Support:

```python
write_candidate_signal(signal: CandidateSignal, evaluation: SignalEvaluation, governance: GovernanceFinding)
promote_signal(signal_id: str, approved_by: str, comments: str)
reject_signal(signal_id: str, rejected_by: str, reason: str)
```

Promotion should not yet be wired to human interrupt. That comes in Phase 6.

### Acceptance criteria

- Signal candidates are evaluated.
- Governance checks can pass, fail, or conditional-pass.
- Candidate signals are written to `signal_registry/candidate_signals.yaml`.
- No approved signal is written without explicit promotion function.
- Tests cover pass, fail, and conditional-pass.

### CLI command

```bash
python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001 --llm-provider fake --write-candidate-signals
```

### Suggested Codex prompt

```text
Implement Phase 5 only.

Goal: add deterministic signal evaluation, governance checks, and Signal Layer registry.
Context: Phase 4 graph produces candidate signals. Use Phase 5 to evaluate signals, check governance, and write candidate signals.
Constraints: do not auto-approve or promote signals. Promotion requires explicit function but should not be called automatically yet. No real PII. Tests must cover pass/fail/conditional governance outcomes.
Done when: pytest passes and the investigate CLI can write candidate signals for A-1001 into signal_registry/candidate_signals.yaml.
```

### Phase gate

Commit message:

```text
phase-5 add signal evaluation governance and registry
```

---

## Phase 6 — Human-in-the-loop approval with LangGraph interrupts

### Objective

Add human approval before signal promotion using LangGraph interrupts and persistence/checkpointing.

### Files to create or modify

```text
src/airlab_fraud_agentic_ai/graph/persistence.py
src/airlab_fraud_agentic_ai/graph/nodes.py
src/airlab_fraud_agentic_ai/graph/routing.py
src/airlab_fraud_agentic_ai/graph/workflow.py
src/airlab_fraud_agentic_ai/cli.py
tests/test_human_review.py
docs/langgraph_workflow.md
```

### Required behaviour

After governance check:

- If governance status is `fail`, do not interrupt; generate report with rejected recommendation.
- If governance status is `pass` or `conditional_pass` and a signal is promotion-ready, pause for human review.
- Human reviewer can:
  - approve
  - reject
  - request edit

### Human review payload

The interrupt payload should include:

```json
{
  "case_id": "A-1001",
  "candidate_signals": [],
  "signal_evaluations": [],
  "governance_findings": {},
  "evidence_summary": "...",
  "question": "Approve signal promotion?"
}
```

### CLI commands

Implement a simple terminal approval flow first.

```bash
python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001 --require-human-review
```

When interrupted, CLI asks:

```text
Approve candidate signal promotion? [approve/reject/edit]
```

On approval:

- promote signal to `approved_signals.yaml`
- remove or mark candidate as promoted
- continue report generation

On rejection:

- write to `rejected_signals.yaml`
- continue report generation

### Tests

Use deterministic test flow to simulate:

1. approval
2. rejection
3. governance fail, no interrupt

### Acceptance criteria

- Human approval is required before signal promotion.
- Approved signal appears in `approved_signals.yaml`.
- Rejected signal appears in `rejected_signals.yaml`.
- Graph can resume after human decision.
- Tests pass.

### Suggested Codex prompt

```text
Implement Phase 6 only.

Goal: add LangGraph human-in-the-loop approval before signal promotion.
Context: Phase 5 writes candidate signals and has promotion/rejection functions. Phase 6 should wire human approval into the graph.
Constraints: use LangGraph interrupt/checkpoint pattern where appropriate. If a simple CLI fallback is needed, keep it clearly separated. The LLM must never approve or promote signals. Tests must simulate approve/reject/fail outcomes without real user input.
Done when: pytest passes, A-1001 can be approved into approved_signals.yaml, rejection writes rejected_signals.yaml, and governance-fail case A-1003 does not trigger approval.
```

### Phase gate

Commit message:

```text
phase-6 add human review signal promotion
```

---

## Phase 7 — Analyst report, audit trail, and workflow trace

### Objective

Create a professional, auditable case report and run trace suitable for GitHub and LinkedIn demonstration.

### Files to create or modify

```text
src/airlab_fraud_agentic_ai/agents/case_report_writer.py
src/airlab_fraud_agentic_ai/evaluation/case_report_eval.py
src/airlab_fraud_agentic_ai/graph/nodes.py
reports/.gitkeep
runs/.gitkeep
tests/test_case_report.py
```

### Report requirements

Generate a Markdown report with:

```markdown
# Fraud Investigation Report — A-1001

## Executive Summary

## Alert Details

## Likely Fraud Typology

## Evidence Reviewed

## Retrieved Knowledge Sources

## Data Tool Results

## Candidate Signals

## Signal Evaluation

## Governance Findings

## Human Review Decision

## Recommendation

## Audit Trail

## Limitations
```

### Audit trail requirements

Each run should create a JSON file:

```text
runs/A-1001-run-<timestamp>.json
```

The run trace should include:

- node execution order
- tool calls
- retrieval sources
- signal evaluation outputs
- governance result
- human decision
- report path

### Acceptance criteria

- Report is generated under `reports/`.
- Run trace is generated under `runs/`.
- Report includes evidence and limitations.
- Report does not expose raw PII.
- Tests verify report sections exist.

### CLI command

```bash
python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001 --llm-provider fake --require-human-review --write-report
```

### Suggested Codex prompt

```text
Implement Phase 7 only.

Goal: add professional Markdown report generation and JSON audit trace.
Context: The graph already investigates cases and supports human review. Add report and run trace outputs.
Constraints: report must include evidence, source references, governance result, human decision, recommendation, and limitations. Do not expose raw PII. Tests must verify required report sections.
Done when: pytest passes and the CLI writes a report under reports/ and a run trace under runs/ for A-1001.
```

### Phase gate

Commit message:

```text
phase-7 add auditable reports and run traces
```

---

## Phase 8 — Business analyst dashboard and interactive fraud case copilot

### Objective

Add a Streamlit dashboard so a business analyst or fraud analyst can interact with the fraud-agentic-ai system through a guided UI rather than the CLI.

The dashboard should demonstrate the enterprise interaction model: case selection, agentic investigation, evidence review, bounded copilot questions, signal review, human approval, report download, and audit trace.

### Files to create or modify

```text
src/airlab_fraud_agentic_ai/dashboard/models.py
src/airlab_fraud_agentic_ai/dashboard/service.py
src/airlab_fraud_agentic_ai/dashboard/view_models.py
streamlit_app/fraud_case_dashboard.py
streamlit_app/README.md
tests/test_dashboard_service.py
README.md
```

Optional if Codex chooses to keep the app modular:

```text
streamlit_app/components/case_queue.py
streamlit_app/components/investigation_workspace.py
streamlit_app/components/evidence_explorer.py
streamlit_app/components/case_copilot.py
streamlit_app/components/signal_review.py
streamlit_app/components/governance_audit.py
streamlit_app/components/report_export.py
streamlit_app/components/signal_monitor.py
```

### Dashboard users

Primary user:

```text
Business analyst / fraud analyst investigating an ML-flagged case.
```

Secondary user:

```text
Reviewer or fraud lead approving or rejecting candidate signal promotion.
```

For this portfolio project, implement reviewer identity as a text input with default value:

```text
fraud_analyst_demo
```

Do not implement authentication.

### Dashboard service layer

Create a service module that hides workflow and registry complexity from Streamlit.

Required functions:

```python
def list_case_queue() -> list[dict]:
    """Return available ML alerts and status for dashboard case selection."""


def get_case_overview(case_id: str) -> dict:
    """Return alert details, model score, threshold, triggered features, and high-level customer summary."""


def run_investigation(case_id: str, llm_provider: str = "fake", require_human_review: bool = True) -> dict:
    """Run or resume the LangGraph investigation workflow and return dashboard-ready run summary."""


def get_run_state(run_id: str) -> dict:
    """Return current workflow state, node status, evidence, signals, governance findings, and report path."""


def ask_case_question(run_id: str, question: str) -> dict:
    """Answer a bounded analyst question using current case state, retrieved knowledge, and approved tool outputs."""


def submit_signal_decision(run_id: str, signal_id: str, decision: str, reviewer: str, comments: str = "") -> dict:
    """Approve, reject, or request edit for a candidate signal. This is the only dashboard path to signal promotion."""


def get_report(run_id: str) -> str:
    """Return final Markdown report if available."""


def get_audit_trace(run_id: str) -> dict:
    """Return JSON audit trace for display and download."""


def list_signal_registry(status: str | None = None) -> list[dict]:
    """Return candidate, approved, or rejected signals."""


def get_signal_monitoring_summary() -> list[dict]:
    """Return monitoring summary for approved signals if Phase 9 has been implemented."""
```

### Dashboard data/view models

Create lightweight Pydantic models or typed dictionaries for:

```text
CaseQueueItem
CaseOverview
WorkflowStepStatus
DashboardRunSummary
EvidenceItem
CopilotAnswer
SignalReviewCard
GovernanceStatusCard
AuditTraceItem
ReportDownload
SignalMonitoringCard
```

These models should make the dashboard output stable and testable.

### Dashboard tabs

Use Streamlit tabs in a single app first. Keep the UI polished but not overbuilt.

#### Tab 1 — Case Queue

Purpose:

```text
Allow the analyst to select a fraud alert and understand why it needs review.
```

Must show:

- case ID / alert ID
- customer ID, masked if appropriate
- model score
- threshold
- score above threshold
- triggered features
- alert time
- current investigation status

Required actions:

- select case
- load case overview
- start investigation

#### Tab 2 — Investigation Workspace

Purpose:

```text
Show the progress and current output of the LangGraph workflow.
```

Must show workflow steps:

```text
intake_case
classify_case_type
plan_investigation
retrieve_knowledge
query_case_data
summarise_evidence
generate_signal_hypotheses
evaluate_signals
governance_check
human_review
generate_case_report
```

Must show:

- completed / pending / blocked status
- likely fraud typology
- risk level
- investigation plan
- latest evidence summary

#### Tab 3 — Evidence Explorer

Purpose:

```text
Let the analyst inspect the evidence behind the agent's reasoning.
```

Must show:

- retrieved fraud typologies
- policy snippets
- data dictionary snippets
- similar case summaries if available
- customer profile summary
- transaction summary
- behavioural summary
- triggered feature values
- lineage summary
- data quality summary

UI rule:

```text
Show summarised approved outputs only. Do not expose raw tables.
```

#### Tab 4 — Case Copilot

Purpose:

```text
Allow the analyst to ask bounded questions about the current case.
```

Required preset questions:

```text
Why was this case flagged?
Which fraud typologies are most relevant?
What evidence supports account takeover risk?
What evidence weakens the fraud hypothesis?
Which triggered features are most important?
Are there data quality or lineage concerns?
Should this signal be promoted, monitored, or rejected?
What should the analyst do next?
```

Copilot answer requirements:

- answer must be grounded in current case state, retrieved knowledge, and approved data-tool outputs
- answer must include evidence references
- answer must include limitations if evidence is incomplete
- answer must not claim a final fraud decision
- answer must not generate SQL

#### Tab 5 — Signal Review

Purpose:

```text
Allow the analyst to review and decide on candidate signal promotion.
```

Must show each candidate signal as a card with:

- signal name
- fraud typology
- description
- source features
- business rationale
- expected direction
- coverage rate
- fraud lift proxy
- false-positive risk
- stability score
- explainability score
- data quality status
- governance status

Required actions:

```text
approve
reject
request edit
```

Approval form fields:

```text
reviewer
comments
```

Decision rules:

- approve writes to approved registry only through `submit_signal_decision`
- reject writes to rejected registry only through `submit_signal_decision`
- request edit records the request and routes back to signal hypothesis / report flow if implemented
- governance fail cannot be approved from dashboard

#### Tab 6 — Governance & Audit

Purpose:

```text
Show why the workflow is enterprise-safe and auditable.
```

Must show:

- lineage status
- data quality status
- privacy status
- explainability status
- approval required flag
- human decision
- reviewer
- comments
- timestamp
- node execution order
- tool calls
- retrieved source paths
- report path

Required actions:

- download JSON audit trace

#### Tab 7 — Report & Export

Purpose:

```text
Allow the analyst to read and export the final investigation report.
```

Must show:

- Markdown case report
- report status
- report file path
- limitations

Required actions:

- download Markdown report
- download JSON run trace

#### Tab 8 — Signal Layer Monitor

Purpose:

```text
Show candidate, approved, and rejected signals plus monitoring results.
```

Must show:

- candidate signals
- approved signals
- rejected signals
- signal status
- drift proxy
- false-positive proxy
- signal decay score
- review recommendation

This tab may show placeholder monitoring until Phase 9 is complete.

### Dashboard architecture rules

1. Streamlit must call dashboard service functions only.
2. Streamlit must not call lower-level registry write functions directly.
3. Streamlit must not call raw data loaders directly.
4. Streamlit must not duplicate graph node logic.
5. Streamlit must not execute arbitrary SQL.
6. Dashboard approval actions must be logged in audit trace.
7. Dashboard must default to fake LLM provider.
8. Tests should target the service layer, not the Streamlit UI rendering.

### Streamlit command

```bash
streamlit run streamlit_app/fraud_case_dashboard.py
```

### Dashboard demo path

The UI should support this path end-to-end:

```text
1. Select A-1001.
2. View model score and triggered features.
3. Click Run Investigation.
4. View workflow progress.
5. Review evidence and retrieved typology context.
6. Ask: Why was this case flagged?
7. Review candidate signal new_device_high_value_new_payee_velocity.
8. Review governance status.
9. Approve signal as fraud_analyst_demo.
10. See approved signal in Signal Layer registry.
11. View final report.
12. Download report and audit trace.
```

### Acceptance criteria

- Streamlit app starts successfully.
- `A-1001`, `A-1002`, and `A-1003` appear in the case queue.
- Analyst can run an investigation for `A-1001` from the UI.
- Dashboard displays workflow status, evidence summary, retrieved knowledge, candidate signals, governance findings, report, and audit trace.
- Analyst can ask at least three preset case questions.
- Analyst can approve or reject a candidate signal from the UI.
- Governance-fail case `A-1003` cannot be approved.
- Dashboard writes human decision to audit trace.
- Dashboard can download Markdown report and JSON run trace.
- Tests pass.
- CLI still works.

### Suggested Codex prompt

```text
Implement Phase 8 only.

Goal: create a business analyst dashboard for Air-lab Fraud Agentic AI.
Context: The CLI workflow already supports investigation, human review, signal promotion, reports, and run traces. Build a Streamlit dashboard over existing workflow/service functions.
Constraints: do not duplicate graph, tool, governance, registry, or report logic in Streamlit. Create a dashboard service layer and test that layer. The UI must not expose raw data, arbitrary SQL, or autonomous signal promotion. Default provider must be fake. Existing CLI and tests must still work.
Done when: Streamlit app starts, A-1001 can be investigated from the UI, evidence and governance are visible, the analyst can ask bounded case questions, approve/reject a candidate signal, view the final report, download report and audit trace, and pytest passes.
```

### Phase gate

Commit message:

```text
phase-8 add business analyst fraud dashboard
```
## Phase 9 — Monitoring, regression evaluation, signal decay, and dashboard monitoring widgets

### Objective

Add lightweight signal monitoring and regression evaluation to show lifecycle management after signal promotion.

### Files to create or modify

```text
src/airlab_fraud_agentic_ai/signal_layer/monitoring.py
src/airlab_fraud_agentic_ai/evaluation/regression_tests.py
src/airlab_fraud_agentic_ai/dashboard/service.py
src/airlab_fraud_agentic_ai/cli.py
streamlit_app/fraud_case_dashboard.py
tests/test_signal_monitoring.py
tests/test_dashboard_service.py
docs/signal_layer_design.md
```

### Monitoring metrics

Implement simple proxy metrics:

- signal coverage over time
- false-positive proxy
- fraud lift proxy over time
- data freshness
- drift proxy
- signal decay score
- review status

### CLI command

```bash
python -m airlab_fraud_agentic_ai.cli monitor-signals
```

Expected output:

```text
Signal: SIG-ATO-001
Status: approved
Coverage: 18%
Fraud lift: 2.7x
Drift status: stable
False positive proxy: medium
Review recommendation: continue monitoring
```

### Dashboard monitoring requirements

Update the dashboard Signal Layer Monitor tab to show:

- approved signal list
- candidate signal list
- rejected signal list
- coverage trend proxy
- fraud lift proxy
- false-positive proxy
- drift status
- signal decay score
- next review recommendation

The dashboard should clearly label these as sample-data proxy metrics, not production fraud validation metrics.

### Acceptance criteria

- Approved signals can be monitored.
- Monitoring output is deterministic.
- Dashboard Signal Layer Monitor tab shows monitoring status.
- Tests cover stable, decaying, and failing signal states.
- README explains that monitoring is a proxy, not production validation.

### Suggested Codex prompt

```text
Implement Phase 9 only.

Goal: add lightweight monitoring, regression evaluation, and dashboard monitoring widgets for approved signals.
Context: Approved signals exist in the Signal Layer registry. Monitoring should compute simple proxy metrics over sample data and expose them through both CLI and the dashboard Signal Layer Monitor tab.
Constraints: do not claim production fraud validation. Keep calculations deterministic and explainable. Tests must cover stable, decaying, and failing signal states. Dashboard must call dashboard service functions, not monitoring internals directly.
Done when: pytest passes, `python -m airlab_fraud_agentic_ai.cli monitor-signals` prints monitoring status for approved signals, and the Streamlit dashboard shows monitoring status in the Signal Layer Monitor tab.
```

### Phase gate

Commit message:

```text
phase-9 add signal monitoring and regression evaluation
```

---

## Phase 10 — Enterprise architecture mapping and portfolio polish

### Objective

Make the repository portfolio-ready for LinkedIn, GitHub, EY-style interviews, and architecture discussions.

### Files to create or modify

```text
README.md
docs/architecture_overview.md
docs/governance_model.md
docs/enterprise_mapping.md
docs/signal_layer_design.md
docs/langgraph_workflow.md
docs/demo_script.md
```

### README final structure

```markdown
# Air-lab Fraud Agentic AI

## Summary
## Business Objective
## Why Agentic AI?
## Architecture Diagram
## Governance Principles
## Demo Scenarios
## Setup
## CLI Demo
## Streamlit Demo
## Project Structure
## LangChain / LangGraph Design
## Signal Layer Design
## Human-in-the-loop Approval
## Evaluation and Monitoring
## Enterprise Mapping
## Limitations
## LinkedIn Project Summary
```

### Enterprise mapping table

| Local component | Enterprise mapping |
|---|---|
| Fake/local LLM | AWS Bedrock model endpoint |
| LangChain tools | API Gateway + Lambda tools |
| LangGraph workflow | Enterprise orchestration layer / Bedrock Agent workflow / Step Functions comparison |
| Markdown knowledge docs | S3 knowledge base / enterprise document repository |
| Local vector store | Bedrock Knowledge Bases / OpenSearch / Snowflake Cortex Search |
| DuckDB/CSV sample data | Snowflake governed data platform |
| Signal registry YAML | Feature Store / governed Signal Layer registry |
| pytest regression checks | AI evaluation harness / CI pipeline |
| Streamlit UI | Internal analyst portal |
| JSON run trace | CloudWatch / audit evidence / observability platform |

### Demo script

Create `docs/demo_script.md` with:

1. Business problem explanation
2. Architecture walkthrough
3. Run `inspect-data`
4. Run `search-knowledge`
5. Run deterministic investigation
6. Run fake LLM investigation
7. Approve signal
8. Show report
9. Show Signal Layer registry
10. Show monitoring
11. Explain limitations and enterprise mapping

### LinkedIn project summary

Add this to README:

```text
Air-lab Fraud Agentic AI is a hands-on enterprise GenAI project demonstrating an agentic fraud investigation and signal-discovery ecosystem using LangChain, LangGraph, governed RAG, BB_Datasets, deterministic data tools, human-in-the-loop approval and a governed Signal Layer.

The project simulates how a fraud analyst investigates an ML-flagged case by orchestrating planner, retrieval, data-tool, signal-evaluation, governance and human-review components. It demonstrates stateful LangGraph workflow orchestration, governed data access, evidence-grounded reporting, signal lifecycle governance, and monitoring for drift, false positives and signal decay.
```

### Acceptance criteria

- README is polished and recruiter-friendly.
- Architecture diagrams render in GitHub Markdown.
- Demo script is clear.
- Limitations are honest.
- Project can be pinned on GitHub.

### Suggested Codex prompt

```text
Implement Phase 10 only.

Goal: polish documentation and enterprise architecture mapping for portfolio use.
Context: The project is functionally complete. Now make README and docs clear for GitHub, LinkedIn, and architecture interviews.
Constraints: do not overclaim production readiness. Emphasise governed AI, deterministic tools, human approval, and enterprise mapping. Include limitations.
Done when: README contains all final sections, docs include architecture/governance/signal layer/enterprise mapping/demo script, diagrams render, and tests still pass.
```

### Phase gate

Commit message:

```text
phase-10 polish portfolio docs and enterprise mapping
```

---

# Additional implementation details

---

## A. Minimal data examples

### A-1001 high-risk case

```text
customer_id: C-001
alert_id: A-1001
model_score: 0.91
threshold: 0.75
triggered_features:
  - device_change_count_24h
  - new_payee_count_24h
  - transaction_amount_zscore_24h
  - failed_login_count_24h
```

Expected workflow outcome:

- likely case type: account takeover or scam-induced payment
- governance: pass or conditional pass
- human approval: required
- signal candidate: `new_device_high_value_new_payee_velocity`

### A-1002 medium-risk case

```text
customer_id: C-002
alert_id: A-1002
model_score: 0.78
threshold: 0.75
triggered_features:
  - transaction_velocity_7d
  - new_payee_count_7d
```

Expected workflow outcome:

- likely case type: payment scam or benign high activity
- governance: pass
- promotion recommendation: monitor, not promote

### A-1003 governance-fail case

```text
customer_id: C-003
alert_id: A-1003
model_score: 0.88
threshold: 0.75
triggered_features:
  - sensitive_demographic_proxy
  - transaction_amount_zscore_24h
```

Expected workflow outcome:

- governance: fail
- reason: privacy/explainability/lineage issue
- no human promotion interrupt
- no approved signal

---

## B. Example signal schema

```yaml
signal_id: SIG-ATO-001
signal_name: new_device_high_value_new_payee_velocity
business_domain: fraud
fraud_typology: account_takeover
description: >
  Identifies cases where a customer changes device and initiates
  high-value transfers to new payees within a short time window.
source_features:
  - device_change_count_24h
  - new_payee_count_24h
  - transaction_amount_zscore_24h
lineage:
  source_datasets:
    - behavioural_events
    - transactions
    - payee_events
governance:
  data_quality_status: pass
  privacy_status: pass
  explainability_status: pass
  approved_by: fraud_analyst
  approval_date: "2026-04-24"
monitoring:
  drift_check: enabled
  false_positive_monitoring: enabled
  review_frequency: monthly
status: approved
```

---

## C. Example case report skeleton

```markdown
# Fraud Investigation Report — A-1001

## Executive Summary
Alert A-1001 was flagged due to elevated transaction velocity, recent device change, and new payee activity.

## Alert Details
- Alert ID: A-1001
- Customer ID: C-001
- Model score: 0.91
- Threshold: 0.75

## Likely Fraud Typology
- Account takeover
- Scam-induced payment

## Evidence Reviewed
| Evidence | Summary | Source |
|---|---|---|
| Device behaviour | Device changed within 24h | behavioural_events |
| Payee activity | Two new payees created | transactions |
| Transaction pattern | High-value transfer above normal pattern | transactions |

## Retrieved Knowledge Sources
- fraud_typologies/account_takeover.md
- policies/fraud_escalation_policy.md
- data_dictionary/behavioural_features.md

## Candidate Signal
`new_device_high_value_new_payee_velocity`

## Signal Evaluation
- Coverage: 18%
- Fraud lift proxy: 2.7x
- False positive risk: medium
- Explainability score: 4/5

## Governance Findings
- Lineage: pass
- Data quality: pass
- Privacy: pass after PII redaction
- Explainability: pass
- Approval required: yes

## Human Review Decision
Approved for Signal Layer candidate monitoring.

## Recommendation
Escalate case for analyst review and monitor the approved signal over the next evaluation cycle.

## Audit Trail
Include node execution order, tool calls, retrieval sources, governance decision, and human review decision.

## Limitations
This is a sample-data portfolio project and is not a production fraud-detection system.
```

---

## D. Testing strategy

### Unit tests

- data contract validation
- approved data tools
- retriever output shape
- signal evaluation metrics
- governance checks
- registry writes

### Workflow tests

- A-1001 end-to-end investigation
- A-1002 no promotion recommendation
- A-1003 governance fail
- approve path
- reject path
- report generation path

### Non-regression tests

- approved tools remain JSON-serialisable
- LLM is not called in tests unless fake provider is used
- signal promotion cannot happen without human decision
- report contains required sections

---

## E. Non-functional requirements

| NFR | Local project implementation |
|---|---|
| Testability | Fake LLM provider and deterministic sample data |
| Auditability | JSON run trace and report audit trail |
| Privacy | No real PII; masked fields in reports |
| Explainability | evidence table, retrieved sources, signal rationale |
| Safety | no unrestricted SQL; no autonomous signal promotion |
| Cost control | local/fake model default; optional real provider only |
| Maintainability | modular tools, graph nodes, agents, governance checks |
| Extensibility | BB_Datasets adapter and enterprise mapping |

---

## F. Project risks and controls

| Risk | Control |
|---|---|
| Codex overbuilds too much at once | Use one phase at a time and explicit “do not implement later phases” instructions |
| LLM writes arbitrary SQL | Only expose deterministic approved data tools |
| Project looks like unsafe autonomous fraud AI | Position as analyst copilot with human approval |
| Tests depend on paid APIs | Fake provider must be default |
| Signal Layer sounds abstract | Persist candidate/approved/rejected YAML registries |
| Governance is only words | Implement deterministic lineage, data quality, privacy, and explainability checks |
| Repo looks like a coding toy | Add architecture docs, reports, audit traces, enterprise mapping |

---

## G. Final Codex review prompt

After all phases are complete, run this prompt:

```text
Review this repository as if you are a senior enterprise AI architect reviewing a portfolio project for an AI Architect role.

Assess:
1. Is the architecture clear?
2. Are LangChain and LangGraph used appropriately?
3. Are governance and human-in-the-loop controls explicit?
4. Is the LLM safely separated from raw data access and signal promotion?
5. Are tests sufficient for a portfolio project?
6. Is the README strong enough for GitHub and LinkedIn?
7. What should be simplified, renamed, or clarified before publishing?

Do not make changes yet. Produce a review report with recommended improvements.
```

Then ask Codex to implement selected improvements only.

---

## H. Final LinkedIn project entry

Use this after completion:

```text
Air-lab Fraud Agentic AI is a hands-on enterprise GenAI project demonstrating an agentic fraud investigation and signal-discovery ecosystem using LangChain, LangGraph, governed RAG, BB_Datasets, deterministic data tools, human-in-the-loop approval and a governed Signal Layer.

The project simulates how a fraud analyst investigates an ML-flagged case by orchestrating planner, retrieval, data-tool, signal-evaluation, governance and human-review components. The workflow retrieves fraud typologies, policy documents, data definitions and historical case context; queries approved customer, transaction and behavioural data tools; generates candidate fraud signals; evaluates signal usefulness; performs governance checks; and promotes approved signals into a governed Signal Layer.

Key architecture patterns include agentic RAG, LangGraph stateful orchestration, deterministic data-access boundaries, signal lifecycle governance, auditability, explainability and monitoring for drift, false positives and signal decay.

Technologies: Python, LangChain, LangGraph, DuckDB/SQLite, FAISS/Chroma, Streamlit, BB_Datasets, RAG, semantic search, signal registry, governance checks and optional AWS Bedrock/Snowflake mapping.
```

---

## I. Final interview explanation

```text
I built Air-lab Fraud Agentic AI as a portfolio project to learn and demonstrate agentic AI architecture with LangChain and LangGraph.

The project simulates an ML-flagged fraud case investigation. LangChain is used for tools, retrieval and prompt orchestration. LangGraph is used to control the stateful workflow: alert intake, investigation planning, RAG retrieval, approved data-tool queries, evidence summarisation, signal hypothesis generation, statistical evaluation, governance checks, human approval and signal promotion.

The important architecture decision was that the LLM never directly accesses raw data, never executes unrestricted SQL, and never promotes fraud signals autonomously. It reasons over evidence provided by governed tools. Signal promotion requires human approval and all outputs are captured with evidence, lineage and audit traceability.

That makes the project an enterprise AI architecture pattern, not just a chatbot demo.
```

---

## J. Reference links for Codex and implementation

Use these references while building:

- OpenAI Codex CLI: https://developers.openai.com/codex/cli
- OpenAI Codex best practices: https://developers.openai.com/codex/learn/best-practices
- Codex AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- LangGraph Graph API: https://docs.langchain.com/oss/python/langgraph/graph-api
- LangGraph interrupts: https://docs.langchain.com/oss/python/langgraph/interrupts
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence
- LangChain retrieval: https://docs.langchain.com/oss/python/langchain/retrieval
- LangChain tools: https://docs.langchain.com/oss/python/integrations/tools

