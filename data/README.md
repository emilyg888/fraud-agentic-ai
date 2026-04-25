# Data Layout

The `data/` directory contains sample datasets that mimic logical BB_Datasets entities.

## Design Intent

- keep the adapter layer stable even if physical dataset names change later
- provide deterministic local data for tests and demos
- avoid real customer PII

## Files

- `bb_dataset_mapping.yaml`: logical entity to file mapping
- `sample/alerts.csv`: ML alert queue
- `sample/customers.csv`: customer profile data
- `sample/accounts.csv`: account-level context
- `sample/transactions.csv`: transaction history
- `sample/behavioural_events.csv`: device and login patterns
- `sample/features.csv`: alert feature values
- `sample/historical_cases.csv`: evaluation benchmark sample
- `sample/data_quality.csv`: freshness and quality status
- `sample/lineage.csv`: source ownership and certification metadata
