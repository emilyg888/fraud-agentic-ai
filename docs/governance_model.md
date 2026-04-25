# Governance Model

The project is designed around governed analyst assistance, not autonomous fraud
decisioning.

## Control Objective

Allow an analyst to investigate, explain, and review a fraud alert while keeping data
access, signal promotion, and monitoring inside explicit control boundaries.

## Governance Principles

- Deterministic tools own dataset access.
- Evidence must be traceable to known sources.
- Signal promotion requires explicit approval or documented automation mode.
- Reports must be auditable and avoid raw PII exposure.
- Monitoring outputs must be framed honestly as proxies.

## Control Layers

### Data Quality

- freshness checks
- anomaly checks
- dataset status roll-up

### Lineage

- source-field provenance
- certification status
- restricted feature visibility

### Privacy

- no raw PII in analyst-facing reports
- bounded dashboard outputs

### Explainability

- candidate signals include source features and human-readable rationale
- reports show evidence summary and knowledge references

### Auditability

- workflow steps are logged
- human decisions are recorded
- reports and traces are persisted as artifacts

## Human Review Boundary

The most important control is the human review boundary:

- the workflow may generate a candidate signal
- the workflow may evaluate and govern that signal
- the workflow may not treat a generated signal as a clean business decision without approval

This is why the dashboard and CLI route approval through explicit review actions.

## Governance Status Interpretation

- `pass`: evidence and controls are acceptable for the current stage
- `conditional_pass`: usable with reviewer caution; caveats must be visible
- `fail`: promotion or trust should stop until the issue is resolved

## Portfolio Framing

This governance model is intentionally simple enough for a local demo, but it mirrors
how enterprise AI systems should separate recommendation, control enforcement, and
human accountability.
