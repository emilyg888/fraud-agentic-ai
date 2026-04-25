---
"markdown.marp.enableHtml": true
theme: gaia
paginate: true
class: invert
---

# Architecture Overview

Air-lab Fraud Agentic AI is structured to look like an enterprise analyst-assist
platform rather than a single chatbot. The architecture separates presentation,
orchestration, deterministic controls, and governed outputs.

## Core Separation
----
```text
Business Analyst UI
        |
        v
streamlit_app/
        |
        v
dashboard.service
        |
        v
workflow / graph
        |
        +-- retrieval tools
        +-- approved data tools
        +-- signal evaluation
        +-- governance checks
        +-- report writer
        +-- signal registry
```
---
## Mermaid View

```mermaid
flowchart LR
    A["Analyst UI"] --> B["Service Layer"]
    B --> C["Workflow State + Nodes"]
    C --> D["Knowledge Retrieval"]
    C --> E["Approved Data Tools"]
    C --> F["Signal Evaluation"]
    C --> G["Governance Controls"]
    C --> H["Human Review"]
    C --> I["Report + Run Trace"]
    H --> J["Signal Registry"]
    J --> K["Monitoring Proxies"]
```
---
## Why This Structure Matters

- The Streamlit app stays presentation-only.
- Deterministic tools, not the LLM, own governed data access.
- Workflow orchestration makes step order, pause points, and auditability explicit.
- Signal promotion is controlled and reviewable.
- Reports, traces, and monitoring exist as downstream artifacts rather than implicit logs.
---
## Main Runtime Flow

1. Intake an alert and classify likely case type.
2. Retrieve relevant fraud knowledge and policies.
3. Query approved case data tools.
4. Summarise evidence and generate signal hypotheses.
5. Evaluate signals and run governance checks.
6. Pause for human decision where required.
7. Persist report, audit trace, and signal registry changes.
8. Monitor approved signals with deterministic proxy metrics.

## Enterprise Interpretation

This local implementation is intentionally small, but the boundaries map to an
enterprise design:

- `streamlit_app/` -> analyst portal
- `dashboard.service` -> application service layer
- `graph/` -> orchestration tier
- `tools/` -> governed tool/API layer
- `knowledge/` + `rag/` -> enterprise retrieval layer
- `signal_registry/` -> governed feature or signal registry
- `reports/` + `runs/` -> audit evidence and observability artifacts
---
```mermaid
flowchart TD
    U["Business Analyst / Fraud Analyst"]
    UI["Streamlit Dashboard<br/>streamlit_app/fraud_case_dashboard.py"]
    SVC["Dashboard Service Layer<br/>dashboard/service.py"]

    WF["Fraud Investigation Workflow<br/>graph/workflow.py"]
    ST["Workflow State + Persistence<br/>graph/state.py + graph/persistence.py"]

    AG["Agent Layer<br/>planner / classifier / summariser / signal_hypothesis / report_writer"]
    RAG["Knowledge Retrieval Layer<br/>rag/* + retrieval_tools.py"]
    TOOLS["Approved Data Tool Layer<br/>bb_dataset_tools.py + alert_tools.py"]
    GOV["Governance Layer<br/>quality / lineage / privacy / explainability"]
    EVAL["Signal Evaluation Layer<br/>signal_metrics.py + regression_tests.py"]
    REG["Signal Registry<br/>signal_registry/*.yaml + registry.py"]
    MON["Monitoring Layer<br/>signal_layer/monitoring.py"]

    DATA["Sample Data Platform<br/>data/sample/*.csv"]
    KNOW["Knowledge Base<br/>knowledge/fraud_typologies<br/>knowledge/policies<br/>knowledge/data_dictionary"]

    ART["Artifacts<br/>reports/*.md<br/>runs/*.json"]
    CLI["CLI<br/>airlab_fraud_agentic_ai/cli.py"]

    U --> UI
    U --> CLI

    UI --> SVC
    CLI --> SVC

    SVC --> WF
    WF --> ST
    WF --> AG
    WF --> RAG
    WF --> TOOLS
    WF --> EVAL
    WF --> GOV
    WF --> REG
    WF --> ART

    RAG --> KNOW
    TOOLS --> DATA
    EVAL --> DATA
    GOV --> DATA

    REG --> MON
    MON --> DATA
    SVC --> MON

    WF -->|pause / resume| U

```
---
```mermaid
flowchart TD
    U["Users
    Business Analyst
    Fraud Reviewer"]

    UI["Presentation Layer
    Streamlit
    Python
    Browser UI"]

    SVC["Application Service Layer
    Python service functions
    Pydantic-style view models
    JSON serialization"]

    ORCH["Workflow / Orchestration Layer
    Python orchestration
    LangGraph Graph API
    SQLite checkpointer
    UUID / datetime audit trail"]

    AGENTS["Reasoning / Agent Layer
    Local fake LLM path
    Ollama-compatible client path
    Prompt templates
    Structured Python outputs"]

    RAG["Knowledge / RAG Layer
    Markdown knowledge base
    Local retriever
    Local vector store
    No external managed vector DB"]

    TOOLS["Deterministic Tool Layer
    Pandas
    CSV-backed dataset adapter
    Governed fraud query tools"]

    GOV["Governance Layer
    Rule-based checks
    Data quality checks
    Lineage checks
    Privacy checks
    Explainability checks"]

    EVAL["Signal Evaluation Layer
    Deterministic metrics
    Regression checks
    Monitoring proxies"]

    REG["Signal Registry Layer
    YAML registry
    PyYAML
    Candidate / approved / rejected states"]

    DATA["Data Layer
    CSV sample datasets
    Pandas
    Local file storage"]

    ART["Artifacts / Audit Layer
    Markdown reports
    JSON run traces
    Local filesystem persistence"]

    MON["Monitoring Layer
    Deterministic proxy metrics
    Coverage / drift / decay logic"]

    TEST["Quality / Validation Layer
    pytest
    deterministic unit tests
    workflow tests"]

    U --> UI
    U --> SVC
    UI --> SVC
    SVC --> ORCH
    ORCH --> AGENTS
    ORCH --> RAG
    ORCH --> TOOLS
    ORCH --> GOV
    ORCH --> EVAL
    ORCH --> REG
    ORCH --> ART
    TOOLS --> DATA
    RAG --> DATA
    REG --> MON
    MON --> DATA
    TEST --> ORCH
    TEST --> GOV
    TEST --> EVAL
    TEST --> MON

```
---

```mermaid
flowchart TD
    ENTRY["Workflow Entry
    Package: langgraph.graph
    Runtime: StateGraph invoke()"]

    STATE["Workflow State
    Local type: FraudInvestigationState
    Package: typing.TypedDict"]

    CHECKPOINT["Checkpoint Persistence
    Package: langgraph-checkpoint-sqlite
    Class: SqliteSaver
    DB: SQLite
    Key: thread_id"]

    ROUTER["Routing / Control
    Package: langgraph.graph
    Features: add_edge, add_conditional_edges
    Local rule: should_pause_for_human_review"]

    INTERRUPT["Human Review Boundary
    Package: langgraph.types
    APIs: interrupt(), Command(resume=...)"]

    N1["Node: intake_case
    Local code: graph/nodes.py
    Service/tool: alert_tools"]

    N2["Node: classify_case_type
    Local code: graph/nodes.py
    Service/tool: classifier agent"]

    N3["Node: plan_investigation
    Local code: graph/nodes.py
    Service/tool: planner agent"]

    N4["Node: retrieve_knowledge
    Local code: graph/nodes.py
    Service/tool: retrieval_tools
    Store: local vector store / markdown KB"]

    N5["Node: query_case_data
    Local code: graph/nodes.py
    Service/tool: bb_dataset_tools
    Data: CSV sample data via pandas"]

    N6["Node: summarise_evidence
    Local code: graph/nodes.py
    Service/tool: evidence_summariser agent"]

    N7["Node: generate_signal_hypotheses
    Local code: graph/nodes.py
    Service/tool: signal_hypothesis agent"]

    N8["Node: evaluate_signals
    Local code: graph/nodes.py
    Service/tool: signal_eval_tools"]

    N9["Node: governance_check
    Local code: graph/nodes.py
    Service/tool: governance_tools"]

    N10["Node: register_candidates
    Local code: workflow runtime
    Service/tool: registry_tools
    Store: YAML signal registry"]

    N11["Node: prepare_human_review
    Local code: workflow runtime
    Output: review payload + draft report"]

    N12["Node: human_review
    Package: langgraph.types
    Mechanism: interrupt/resume"]

    N13["Node: promote_signal
    Local code: workflow runtime
    Service/tool: registry_tools
    Store: YAML signal registry"]

    N14["Node: generate_case_report
    Local code: graph/nodes.py
    Service/tool: case_report_writer"]

    ART["Artifact Export
    Local module: graph/persistence.py
    Files: reports/*.md, runs/*.json"]

    AUDIT["Audit Trail
    Local runtime: _audit_entry / audit_log
    Data: timestamped step records"]

    ENTRY --> STATE
    ENTRY --> CHECKPOINT
    ENTRY --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N6 --> N7
    N7 --> N8
    N8 --> N9
    N9 --> N10

    N10 --> ROUTER
    ROUTER -->|human review required| N11
    ROUTER -->|auto-approve path| N13
    ROUTER -->|no candidates| N14

    N11 --> INTERRUPT
    INTERRUPT --> N12
    N12 -->|approve| N14
    N12 -->|reject| N14

    N13 --> N14
    N14 --> ART

    STATE --> N1
    STATE --> N2
    STATE --> N3
    STATE --> N4
    STATE --> N5
    STATE --> N6
    STATE --> N7
    STATE --> N8
    STATE --> N9
    STATE --> N10
    STATE --> N11
    STATE --> N12
    STATE --> N13
    STATE --> N14

    AUDIT --> STATE
    CHECKPOINT --> STATE

```
---
