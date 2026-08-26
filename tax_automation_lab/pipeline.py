from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import duckdb

from .io import ensure_output_dir, read_csv, read_yaml
from .reconciliation import build_exception_report, build_scenario_summary, build_summary, reconcile
from .reporting import render_audit_summary
from .rules_engine import classify_transactions
from .validation import normalise_transactions, validate_transactions


@dataclass(frozen=True)
class PipelinePaths:
    transactions: Path
    account_rules: Path
    golden_results: Path
    rules_config: Path
    output_dir: Path


@dataclass(frozen=True)
class PipelineSummary:
    total_transactions: int
    exception_count: int
    audit_summary_path: Path
    duckdb_path: Path


def run_pipeline(paths: PipelinePaths) -> PipelineSummary:
    ensure_output_dir(paths.output_dir)

    rules_config = read_yaml(paths.rules_config)
    transactions = normalise_transactions(read_csv(paths.transactions))
    account_rules = read_csv(paths.account_rules)
    golden = read_csv(paths.golden_results)

    validation_issues = validate_transactions(transactions, account_rules)
    classified = classify_transactions(transactions, rules_config)
    reconciled = reconcile(classified, validation_issues)
    exceptions = build_exception_report(reconciled, validation_issues)
    summary = build_summary(reconciled)
    scenario_summary = build_scenario_summary(reconciled)
    golden_comparison = _compare_with_golden(reconciled, golden)

    clean_path = paths.output_dir / "clean_transactions.csv"
    exception_path = paths.output_dir / "exception_report.csv"
    summary_path = paths.output_dir / "reconciliation_summary.csv"
    scenario_summary_path = paths.output_dir / "scenario_summary.csv"
    validation_path = paths.output_dir / "validation_issues.csv"
    golden_path = paths.output_dir / "golden_comparison.csv"
    duckdb_path = paths.output_dir / "tax_automation.duckdb"
    audit_path = paths.output_dir / "audit_summary.md"

    reconciled.to_csv(clean_path, index=False)
    exceptions.to_csv(exception_path, index=False)
    summary.to_csv(summary_path, index=False)
    scenario_summary.to_csv(scenario_summary_path, index=False)
    validation_issues.to_csv(validation_path, index=False)
    golden_comparison.to_csv(golden_path, index=False)

    audit_summary = render_audit_summary(
        reconciled=reconciled,
        exceptions=exceptions,
        summary=summary,
        scenario_summary=scenario_summary,
        ruleset_name=rules_config.get("metadata", {}).get("ruleset_name", "unknown"),
        ruleset_version=rules_config.get("metadata", {}).get("version", "unknown"),
    )
    audit_path.write_text(audit_summary, encoding="utf-8")
    _write_duckdb(
        duckdb_path,
        reconciled,
        exceptions,
        summary,
        scenario_summary,
        validation_issues,
        golden_comparison,
    )

    return PipelineSummary(
        total_transactions=len(reconciled),
        exception_count=len(exceptions),
        audit_summary_path=audit_path,
        duckdb_path=duckdb_path,
    )


def _compare_with_golden(reconciled, golden):
    expected = golden.copy()
    actual = reconciled[
        ["transaction_id", "tax_category", "calculated_gst", "exception_flag"]
    ].rename(
        columns={
            "tax_category": "actual_tax_category",
            "calculated_gst": "actual_gst_amount",
            "exception_flag": "actual_exception",
        }
    )
    comparison = expected.merge(actual, on="transaction_id", how="outer")
    comparison["category_expected"] = comparison["expected_tax_category"] == comparison["actual_tax_category"]
    comparison["exception_expected"] = comparison["expected_exception"] == comparison["actual_exception"]
    comparison["gst_expected"] = comparison.apply(_gst_expected, axis=1)
    comparison["golden_match"] = (
        comparison["category_expected"] & comparison["exception_expected"] & comparison["gst_expected"]
    )
    return comparison


def _gst_expected(row) -> bool:
    if row["expected_exception"] and row["expected_gst_amount"] != row["expected_gst_amount"]:
        return True
    if row["expected_gst_amount"] != row["expected_gst_amount"] and row["actual_gst_amount"] != row["actual_gst_amount"]:
        return True
    return abs(float(row["expected_gst_amount"]) - float(row["actual_gst_amount"])) <= 0.01


def _write_duckdb(
    path: Path,
    reconciled,
    exceptions,
    summary,
    scenario_summary,
    validation_issues,
    golden_comparison,
) -> None:
    if path.exists():
        path.unlink()
    with duckdb.connect(str(path)) as con:
        con.register("reconciled_df", reconciled)
        con.register("exceptions_df", exceptions)
        con.register("summary_df", summary)
        con.register("scenario_summary_df", scenario_summary)
        con.register("validation_df", validation_issues)
        con.register("golden_df", golden_comparison)
        con.execute("create table clean_transactions as select * from reconciled_df")
        con.execute("create table exception_report as select * from exceptions_df")
        con.execute("create table reconciliation_summary as select * from summary_df")
        con.execute("create table scenario_summary as select * from scenario_summary_df")
        con.execute("create table validation_issues as select * from validation_df")
        con.execute("create table golden_comparison as select * from golden_df")
