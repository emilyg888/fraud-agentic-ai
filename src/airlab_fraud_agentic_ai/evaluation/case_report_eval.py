from __future__ import annotations


REQUIRED_REPORT_SECTIONS = [
    "## Executive Summary",
    "## Alert Details",
    "## Likely Fraud Typology",
    "## Evidence Reviewed",
    "## Retrieved Knowledge Sources",
    "## Candidate Signals",
    "## Governance Findings",
    "## Human Review Decision",
    "## Audit Trail",
]


def validate_case_report(report: str) -> list[str]:
    return [section for section in REQUIRED_REPORT_SECTIONS if section not in report]
