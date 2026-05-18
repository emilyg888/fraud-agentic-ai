# Case Evidence Record Schema

The analyst-assist fraud workflow should represent each evidence item as a
`CaseEvidenceRecord` before it is used by hypotheses, governance checks, or report
claims. The schema lives in
`src/airlab_fraud_agentic_ai/data/contracts.py` with the other Pydantic data contracts.

## Required linkage and provenance

| Field | Purpose |
|---|---|
| `evidence_id` | Stable evidence identifier used by hypotheses and report claims. |
| `case_id` | Investigation case or alert case this evidence belongs to. |
| `alert_id` | ML alert that initiated the investigation. |
| `run_id` | Optional workflow run identifier for persisted trace lookup. |
| `customer_id` | Optional synthetic customer identifier, when applicable. |
| `evidence_type` | Evidence category, such as `retrieved_typology`, `transaction_summary`, `behavioural_summary`, `policy_note`, `governance_finding`, or `historical_case`. |
| `source_tool` | Deterministic tool or service function that produced the evidence. |
| `source_document` | Retrieved knowledge document title, when the source is a document. |
| `source_path` | Local path or enterprise object reference for the source. |
| `source_record_id` | Source row, event, document chunk, or record identifier when available. |
| `retrieval_timestamp` | ISO-8601 timestamp showing when the evidence was retrieved or generated. |
| `workflow_step` | Workflow node that created the record. |

## Evidence content and quality

| Field | Purpose |
|---|---|
| `summary` | Analyst-readable summary grounded in the source reference. |
| `raw_reference` | Structured pointer to the original sample-data rows, document chunks, fields, or aggregate inputs. |
| `confidence_score` | Optional 0.0-1.0 quality or retrieval confidence score. |
| `quality_notes` | Data quality, retrieval quality, or interpretation caveats. |
| `policy_sensitivity` | Sensitivity label such as `public`, `internal`, `restricted`, or `requires_review`. |
| `sensitivity_rationale` | Reason for the policy sensitivity label. |

## Traceability

| Field | Purpose |
|---|---|
| `lineage_references` | Dataset fields or lineage entries consulted for this evidence. |
| `audit_event_ids` | Audit log entries associated with retrieval, transformation, or analyst action. |
| `supporting_hypothesis_ids` | Hypotheses that cite this evidence. |
| `supporting_claim_ids` | Report claims that cite this evidence. |
| `metadata` | Reserved structured metadata for local demo or enterprise mappings. |

Evidence records must contain source references and audit trace metadata. They must not
contain real customer PII or let the LLM access raw datasets directly.
