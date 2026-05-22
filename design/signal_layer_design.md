# Signal Layer Design

The Signal Layer separates case-specific hypotheses from governed signals that are worth
tracking and reviewing over time.

## Registry States

- `candidate_signals.yaml`
- `approved_signals.yaml`
- `rejected_signals.yaml`

## Lifecycle

1. A workflow generates one or more candidate signals from case evidence.
2. Deterministic evaluation computes coverage, fraud lift proxy, false-positive proxy,
   and explainability indicators.
3. Governance checks review quality, lineage, privacy, and explainability constraints.
4. A reviewer approves or rejects the signal.
5. The registry state changes and the decision is written to the audit trace.
6. Approved signals enter monitoring for drift and decay proxies.

## Design Intent

This layer exists so the project does not stop at “the model said fraud.” Instead, it
shows a more realistic operating pattern:

- investigate an alert
- extract a reusable signal hypothesis
- govern that hypothesis
- promote only after review
- monitor the promoted signal

## Monitoring Proxy Metrics

Approved signals are monitored with deterministic sample-data proxies:

- coverage rate
- coverage trend proxy
- fraud lift proxy
- fraud lift trend proxy
- false-positive proxy
- data freshness hours
- drift proxy
- signal decay score
- next review recommendation

## Important Limitation

These metrics are useful for governance demos, regression tests, and analyst discussion.
They are not production fraud validation metrics and should not be presented as such.
