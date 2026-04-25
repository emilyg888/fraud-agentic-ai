from __future__ import annotations


def run_explainability_check(signal_candidates: list[dict]) -> dict:
    missing_descriptions = [signal["signal_name"] for signal in signal_candidates if not signal.get("description")]
    return {
        "status": "pass" if not missing_descriptions else "fail",
        "issues": [f"Missing description for {name}" for name in missing_descriptions],
    }
