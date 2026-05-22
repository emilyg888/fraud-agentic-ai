# Enterprise Mapping

This repository is local-first, but it is intentionally structured to resemble an
enterprise analyst-assist architecture.

## Mapping Table

| Local component | Enterprise mapping | Why it matters |
|---|---|---|
| Local/fake LLM provider | AWS Bedrock model endpoint or internal model gateway | Keeps reasoning separate from business controls |
| Markdown knowledge docs | S3 knowledge base or enterprise document repository | Demonstrates governed retrieval over curated content |
| Local vector/retrieval layer | Bedrock Knowledge Bases, OpenSearch, Cortex Search | Shows how evidence retrieval can be grounded and controlled |
| Deterministic Python tools | API Gateway, Lambda, dbt metrics, governed services | Keeps the LLM away from raw datasets and arbitrary queries |
| Workflow orchestrator | LangGraph runtime, orchestration tier, Step Functions-style control plane | Makes state, pause points, and audit boundaries explicit |
| CSV sample datasets | Snowflake governed platform, analytical views, curated fraud marts | Represents controlled enterprise data access patterns |
| YAML signal registry | Feature store, model-risk registry, governed Signal Layer | Shows signal lifecycle management beyond one-off investigations |
| Reports and JSON traces | S3 artifacts, CloudWatch, observability and governance evidence stores | Supports auditability and post-run review |
| Streamlit dashboard | Internal analyst portal | Demonstrates a human-facing investigation workspace |
| pytest regression suite | CI pipeline, AI evaluation harness, release gate | Shows deterministic validation and change control |

## Architecture Discussion Points

If you are explaining this project in an interview, the key point is not that Streamlit,
CSV, or YAML are enterprise tools. The point is that the boundaries are enterprise-grade:

- UI is separated from fraud logic
- workflow is separated from tools
- reasoning is separated from control actions
- human approval is separated from signal generation
- monitoring is separated from the initial investigation

## Honest Positioning

This repo is not production fraud infrastructure. It is a compact architecture lab that
makes enterprise design decisions visible and testable.
