# Codex Handoff Summary

This repository structure and MVP implementation are derived from:

- `Air-lab_Fraud_Agentic_AI_Project_Design.md`
- `Air-lab_Fraud_Agentic_AI_Codex_Handoff_v1_1_Dashboard.md`

## Delivery Priorities

1. Keep the reasoning layer separate from deterministic tools.
2. Keep the dashboard thin over a service layer.
3. Use sample data only.
4. Default to a fake LLM provider.
5. Preserve a human approval boundary before signal promotion.

## Build Order

- repository bootstrap
- data contracts and approved tools
- knowledge base and retrieval
- workflow orchestration
- fake-agent reasoning layer
- signal evaluation and governance
- human review and registry updates
- dashboard and report export
