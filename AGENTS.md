# AGENTS.md

## Project identity

This repository is an enterprise AI architecture lab called Air-lab Fraud Agentic AI.
It demonstrates agentic fraud investigation, governed RAG, deterministic data tools,
signal evaluation, governance checks, human-in-the-loop approval, signal promotion,
and a business analyst dashboard.

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
