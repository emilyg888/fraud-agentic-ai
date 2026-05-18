---
"markdown.marp.enableHtml": true
theme: gaia
paginate: true
class: invert
---

# Architecture Overview

Air-lab Fraud Agentic AI is designed as an enterprise-style analyst-assist system, not
as a single chatbot. The key architectural rule is strict separation between:

- presentation
- service orchestration
- workflow state/control
- reasoning
- deterministic controls
- governed artifacts

---

## Core Separation

```text
Business Analyst / Reviewer
            |
            v
     Streamlit Dashboard
            |
            v
     dashboard.service
            |
            v
 LangGraph Workflow / StateGraph
            |
            +-- LLM reasoning layer
            +-- RAG / knowledge retrieval
            +-- approved data tools
            +-- governance checks
            +-- signal evaluation
            +-- signal registry
            +-- reports and run traces
```

---

## Full Stack View

```mermaid
flowchart TD
    U["Users
    Business Analyst
    Fraud Reviewer"]

    UI["Presentation Layer
    Streamlit
    Browser UI"]

    CLI["CLI Layer
    argparse
    terminal workflow"]

    SVC["Application Service Layer
    dashboard service
    view models
    JSON responses"]

    ORCH["Workflow / Orchestration Layer
    LangGraph Graph API
    StateGraph
    conditional routing
    interrupt()/resume"]

    CKPT["Checkpoint / State Layer
    SQLite
    SqliteSaver
    thread_id-based state"]

    LLM["Reasoning / LLM Runtime Layer
    fake provider
    Ollama-compatible provider
    prompts
    structured reasoning outputs"]

    RAG["Knowledge / RAG Layer
    markdown knowledge base
    local retriever
    local vector store"]

    TOOLS["Deterministic Tool Layer
    approved fraud data tools
    alert tools
    retrieval tools
    registry tools"]

    GOV["Governance Layer
    data quality
    lineage
    privacy
    explainability"]

    EVAL["Evaluation Layer
    signal metrics
    regression checks
    monitoring proxies"]

    REG["Signal Registry Layer
    YAML registry
    candidate / approved / rejected states"]

    DATA["Data Layer
    sample CSV datasets
    pandas-backed adapter
    local file storage"]

    ART["Artifact Layer
    markdown reports
    JSON run traces
    persisted audit outputs"]

    MON["Monitoring Layer
    coverage proxy
    fraud-lift proxy
    drift proxy
    decay score"]

    U --> UI
    U --> CLI
    UI --> SVC
    CLI --> SVC

    SVC --> ORCH
    ORCH --> CKPT
    ORCH --> LLM
    ORCH --> RAG
    ORCH --> TOOLS
    ORCH --> GOV
    ORCH --> EVAL
    ORCH --> REG
    ORCH --> ART

    RAG --> DATA
    TOOLS --> DATA
    GOV --> DATA
    EVAL --> DATA

    REG --> MON
    MON --> DATA
```

---

## Workflow / Orchestration Deep Dive

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

    N1["intake_case
    alert_tools"]
    N2["classify_case_type
    classifier"]
    N3["plan_investigation
    planner"]
    N4["retrieve_knowledge
    retrieval_tools + local vector store"]
    N5["query_case_data
    bb_dataset_tools + pandas/CSV"]
    N6["summarise_evidence
    evidence_summariser"]
    N7["generate_signal_hypotheses
    signal_hypothesis"]
    N8["evaluate_signals
    signal_eval_tools"]
    N9["governance_check
    governance_tools"]
    N10["register_candidates
    registry_tools + YAML registry"]
    N11["prepare_human_review
    review payload + draft report"]
    N12["human_review
    interrupt/resume"]
    N13["promote_signal
    registry_tools"]
    N14["generate_case_report
    case_report_writer"]
    ART["Artifact Export
    reports/*.md
    runs/*.json"]

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
    N12 --> N14
    N13 --> N14
    N14 --> ART
```

---

## Why This Structure Matters

- The Streamlit app stays presentation-only.
- The service layer hides workflow complexity from the UI.
- LangGraph owns orchestration, pause/resume, and checkpointed state.
- The LLM runtime is a dependency of reasoning, not the orchestration engine itself.
- Deterministic tools, not the LLM, own governed data access and control actions.
- Reports, traces, and monitoring are explicit artifacts rather than implicit logs.

---

## Enterprise Interpretation

This local implementation stays small, but the boundaries map cleanly to enterprise
architecture:

- `streamlit_app/` -> internal analyst portal
- `dashboard.service` -> application service layer
- `graph/` -> orchestration tier
- `langgraph` + SQLite checkpointer -> stateful workflow runtime
- `tools/` -> governed tool/API layer
- `knowledge/` + `rag/` -> enterprise retrieval layer
- `signal_registry/` -> governed Signal Layer / feature registry
- `reports/` + `runs/` -> audit evidence and observability artifacts
