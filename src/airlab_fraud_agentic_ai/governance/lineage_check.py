from __future__ import annotations


def run_lineage_check(lineage: dict) -> dict:
    records = lineage.get("records", [])
    uncertified = [record for record in records if record["certification_status"] != "certified"]
    return {
        "status": "pass" if not uncertified else "conditional_pass",
        "issues": [
            f"{record['field_name']} has certification status {record['certification_status']}"
            for record in uncertified
        ],
    }
