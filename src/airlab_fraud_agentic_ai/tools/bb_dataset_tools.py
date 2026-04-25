from __future__ import annotations

from statistics import mean

from airlab_fraud_agentic_ai.data.bb_adapter import BBDatasetAdapter


def _adapter(adapter: BBDatasetAdapter | None) -> BBDatasetAdapter:
    return adapter or BBDatasetAdapter.create()


def get_customer_profile(customer_id: str, adapter: BBDatasetAdapter | None = None) -> dict:
    rows = _adapter(adapter).customers()
    row = rows.loc[rows["customer_id"] == customer_id]
    if row.empty:
        raise KeyError(f"Unknown customer_id: {customer_id}")
    return row.iloc[0].to_dict()


def get_account_summary(customer_id: str, adapter: BBDatasetAdapter | None = None) -> dict:
    rows = _adapter(adapter).accounts()
    subset = rows.loc[rows["customer_id"] == customer_id]
    return {
        "account_count": int(len(subset)),
        "product_types": sorted(subset["product_type"].tolist()),
        "statuses": sorted(subset["status"].tolist()),
    }


def get_transaction_velocity(customer_id: str, window_days: int = 7, adapter: BBDatasetAdapter | None = None) -> dict:
    rows = _adapter(adapter).transactions()
    subset = rows.loc[rows["customer_id"] == customer_id]
    amounts = subset["amount"].astype(float).tolist()
    unique_payees = subset["payee_id"].nunique()
    return {
        "window_days": window_days,
        "transaction_count": int(len(subset)),
        "total_amount": round(sum(amounts), 2),
        "average_amount": round(mean(amounts), 2) if amounts else 0.0,
        "unique_payee_count": int(unique_payees),
    }


def get_new_payee_activity(customer_id: str, window_days: int = 1, adapter: BBDatasetAdapter | None = None) -> dict:
    rows = _adapter(adapter).transactions()
    subset = rows.loc[(rows["customer_id"] == customer_id) & (rows["is_new_payee"] == True)]  # noqa: E712
    amounts = subset["amount"].astype(float).tolist()
    return {
        "window_days": window_days,
        "new_payee_count": int(subset["payee_id"].nunique()),
        "new_payee_amount": round(sum(amounts), 2),
        "payees": sorted(subset["payee_id"].unique().tolist()),
    }


def get_device_change_summary(customer_id: str, window_days: int = 7, adapter: BBDatasetAdapter | None = None) -> dict:
    rows = _adapter(adapter).behavioural_events()
    subset = rows.loc[rows["customer_id"] == customer_id]
    return {
        "window_days": window_days,
        "device_change_count": int(subset["device_changed"].sum()),
        "failed_login_total": int(subset["failed_login_count"].sum()),
        "geolocation_anomalies": int(subset["geolocation_anomaly"].sum()),
        "channels": sorted(subset["channel"].unique().tolist()),
    }


def get_feature_values(alert_id: str, adapter: BBDatasetAdapter | None = None) -> dict:
    rows = _adapter(adapter).features()
    subset = rows.loc[rows["alert_id"] == alert_id]
    features = [
        {
            "feature_name": row["feature_name"],
            "feature_value": float(row["feature_value"]),
            "window": row["window"],
            "source_table": row["source_table"],
            "calculation_logic": row["calculation_logic"],
        }
        for _, row in subset.iterrows()
    ]
    return {"alert_id": alert_id, "features": features}


def get_data_quality_status(adapter: BBDatasetAdapter | None = None) -> dict:
    rows = _adapter(adapter).data_quality()
    worst = rows.sort_values(["status", "freshness_hours"], ascending=[True, False]).iloc[-1].to_dict()
    return {
        "datasets": rows.to_dict(orient="records"),
        "worst_dataset": worst,
    }


def get_lineage_status(feature_names: list[str], adapter: BBDatasetAdapter | None = None) -> dict:
    rows = _adapter(adapter).lineage()
    subset = rows.loc[rows["field_name"].isin(feature_names)]
    return {
        "feature_count": len(feature_names),
        "records": subset.to_dict(orient="records"),
    }


def query_case_data(alert: dict, adapter: BBDatasetAdapter | None = None) -> dict:
    customer_id = alert["customer_id"]
    feature_bundle = get_feature_values(alert["alert_id"], adapter=adapter)
    feature_names = [item["feature_name"] for item in feature_bundle["features"]]
    return {
        "customer_profile": get_customer_profile(customer_id, adapter=adapter),
        "account_summary": get_account_summary(customer_id, adapter=adapter),
        "transaction_summary": get_transaction_velocity(customer_id, adapter=adapter),
        "new_payee_activity": get_new_payee_activity(customer_id, adapter=adapter),
        "behavioural_summary": get_device_change_summary(customer_id, adapter=adapter),
        "feature_summary": feature_bundle,
        "data_quality": get_data_quality_status(adapter=adapter),
        "lineage": get_lineage_status(feature_names, adapter=adapter),
    }
