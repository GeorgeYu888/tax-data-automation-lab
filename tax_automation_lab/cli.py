from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import PipelinePaths, run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the synthetic tax data automation lab.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run validation, classification and reconciliation.")
    run_parser.add_argument("--transactions", default="data/raw/transactions.csv")
    run_parser.add_argument("--account-rules", default="data/reference/account_tax_rules.csv")
    run_parser.add_argument("--golden", default="data/reference/golden_expected_results.csv")
    run_parser.add_argument("--rules", default="config/tax_rules.yaml")
    run_parser.add_argument("--output-dir", default="outputs")

    args = parser.parse_args()

    if args.command == "run":
        paths = PipelinePaths(
            transactions=Path(args.transactions),
            account_rules=Path(args.account_rules),
            golden_results=Path(args.golden),
            rules_config=Path(args.rules),
            output_dir=Path(args.output_dir),
        )
        summary = run_pipeline(paths)
        print(f"Processed {summary.total_transactions} transactions")
        print(f"Exceptions requiring review: {summary.exception_count}")
        print(f"Audit summary: {summary.audit_summary_path}")

