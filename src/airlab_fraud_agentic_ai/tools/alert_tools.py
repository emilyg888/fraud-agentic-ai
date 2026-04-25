from __future__ import annotations

from airlab_fraud_agentic_ai.data.bb_adapter import BBDatasetAdapter


def get_alert(alert_id: str, adapter: BBDatasetAdapter | None = None) -> dict:
    adapter = adapter or BBDatasetAdapter.create()
    alerts = adapter.alerts()
    row = alerts.loc[alerts["alert_id"] == alert_id]
    if row.empty:
        raise KeyError(f"Unknown alert_id: {alert_id}")
    return row.iloc[0].to_dict()
