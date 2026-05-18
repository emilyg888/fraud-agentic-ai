# Issues Pending Review

## Summary

| ID | Severity | Area | Issue | Recommended action | Status |
|---|---|---|---|---|---|
| ISSUE-001 | Low | Docs | `README.md` previously linked to missing `docs/reference_architecture_pattern.md`. | Broken link removed during housekeeping; confirm no external handoff depends on the missing file. | Pending review |
| ISSUE-002 | Low | Housekeeping | Local generated outputs exist in ignored paths such as `reports/`, `runs/`, `benchmark_plots/`, caches, and `.DS_Store` files. | Keep ignored; optionally clean locally before demos if they distract from review. | Pending review |
| ISSUE-003 | Low | Runtime | Local Ollama mode depends on an external local server and model availability. | Use `--llm-backend fake` for offline SIT; start Ollama for Qwen demo runs. | Pending review |
| ISSUE-004 | Low | UI | Streamlit emits a deprecation warning for `use_container_width`. | Replace with `width='stretch'` in a focused UI maintenance pass. | Pending review |

## SIT Results

| Command | Result | Notes |
|---|---|---|
| `uv run pytest` | Passed | Full deterministic test suite passed on 2026-05-18. |
| `.venv/bin/python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001 --llm-backend fake` | Passed | Practical workflow smoke test passed with fake backend. |
| `.venv/bin/python -m airlab_fraud_agentic_ai.cli investigate --case-id A-1001` | Not run as pass criterion | Requires local Ollama and `qwen3.6:35b-a3b`; use for local model demo, not offline SIT. |

## Archived Code Review

| Original path | Archived path | Reason | Review needed? |
|---|---|---|---|
| None | None | No low-risk redundant source files had enough evidence for archive. | No |

## Detailed Issues

### ISSUE-001 - Missing Reference Architecture Link

- Severity: Low
- Area: Docs
- Evidence: `README.md` referenced `docs/reference_architecture_pattern.md`, but that file is not present.
- Impact: Reviewers could hit a broken documentation link.
- Recommended action: Keep the removed link out unless the missing document is recreated.
- Status: Pending review

### ISSUE-002 - Ignored Local Generated Outputs

- Severity: Low
- Area: Housekeeping
- Evidence: Generated reports, run traces, benchmark plots, caches, and `.DS_Store` files exist locally and are covered by `.gitignore`.
- Impact: They can distract during local review but are not staged for commit.
- Recommended action: Leave ignored outputs local, or clean them manually before screenshots/demos if needed.
- Status: Pending review

### ISSUE-003 - Ollama Dependency For Local Qwen Mode

- Severity: Low
- Area: Runtime
- Evidence: Default backend is `ollama`; fake backend is required for offline deterministic SIT.
- Impact: A default investigation run can fail if Ollama is not running or the model is not pulled.
- Recommended action: Use `--llm-backend fake` for tests and handoff checks; document Ollama startup for live model demos.
- Status: Pending review

### ISSUE-004 - Streamlit Width Deprecation

- Severity: Low
- Area: UI
- Evidence: Streamlit reports that `use_container_width` should be replaced with `width`.
- Impact: No current functional impact, but future Streamlit versions may remove the old argument.
- Recommended action: Replace deprecated arguments in a UI maintenance pass.
- Status: Pending review
