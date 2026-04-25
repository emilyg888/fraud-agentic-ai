from __future__ import annotations


def run_data_quality_check(data_quality: dict) -> dict:
    worst = data_quality.get("worst_dataset", {})
    status = worst.get("status", "pass")
    return {
        "status": status,
        "issues": [
            f"{worst.get('dataset_name', 'unknown')} freshness={worst.get('freshness_hours', 'n/a')}h"
        ] if status != "pass" else [],
    }
