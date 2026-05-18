from __future__ import annotations

import argparse
import json
import sys

from airlab_fraud_agentic_ai.config import get_settings
from airlab_fraud_agentic_ai.dashboard.service import (
    get_signal_monitoring_summary,
    get_report,
    run_investigation,
    submit_signal_decision,
)
from airlab_fraud_agentic_ai.evaluation.regression_tests import run_registry_regression_suite


def build_parser() -> argparse.ArgumentParser:
    settings = get_settings()
    parser = argparse.ArgumentParser(description="Air-lab Fraud Agentic AI CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    investigate = subparsers.add_parser("investigate", help="Run an investigation for a case")
    investigate.add_argument("--case-id", required=True)
    investigate.add_argument("--llm-backend", default=settings.llm_backend)
    investigate.add_argument("--llm-provider", dest="llm_backend", help=argparse.SUPPRESS)
    investigate.add_argument("--auto-approve", action="store_true")

    review = subparsers.add_parser("review", help="Submit a human review decision")
    review.add_argument("--run-id", required=True)
    review.add_argument("--signal-id", required=True)
    review.add_argument("--decision", choices=["approve", "reject"], required=True)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--comments", default="")

    report = subparsers.add_parser("report", help="Print a saved report")
    report.add_argument("--run-id", required=True)

    subparsers.add_parser("monitor-signals", help="Print deterministic proxy monitoring for approved signals")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "investigate":
        try:
            result = run_investigation(
                case_id=args.case_id,
                llm_backend=args.llm_backend,
                require_human_review=not args.auto_approve,
            )
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(json.dumps(result, indent=2))
        return 0

    if args.command == "review":
        result = submit_signal_decision(
            run_id=args.run_id,
            signal_id=args.signal_id,
            decision=args.decision,
            reviewer=args.reviewer,
            comments=args.comments,
        )
        print(json.dumps(result, indent=2))
        return 0

    if args.command == "report":
        print(get_report(args.run_id))
        return 0

    if args.command == "monitor-signals":
        summary = get_signal_monitoring_summary()
        regression = run_registry_regression_suite()
        if not summary:
            print("No approved signals available for monitoring.")
            return 0

        for index, item in enumerate(summary):
            if index:
                print()
            print(f"Signal: {item['signal_name']}")
            print(f"Status: {item['review_status']}")
            print(f"Coverage: {round(item['coverage_rate'] * 100)}%")
            print(f"Fraud lift: {item['fraud_lift']}x")
            print(f"Drift status: {item['drift_proxy']}")
            print(f"False positive proxy: {item['false_positive_proxy']}")
            print(f"Signal decay score: {item['signal_decay_score']}")
            print(f"Review recommendation: {item['next_review_recommendation']}")
        print()
        print(json.dumps(regression, indent=2))
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
