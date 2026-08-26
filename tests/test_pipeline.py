from pathlib import Path

import duckdb

from tax_automation_lab.pipeline import PipelinePaths, run_pipeline


def test_pipeline_generates_expected_outputs(tmp_path):
    paths = PipelinePaths(
        transactions=Path("data/raw/transactions.csv"),
        account_rules=Path("data/reference/account_tax_rules.csv"),
        golden_results=Path("data/reference/golden_expected_results.csv"),
        rules_config=Path("config/tax_rules.yaml"),
        output_dir=tmp_path,
    )

    summary = run_pipeline(paths)

    assert summary.total_transactions == 36
    assert summary.exception_count == 23
    assert (tmp_path / "clean_transactions.csv").exists()
    assert (tmp_path / "exception_report.csv").exists()
    assert (tmp_path / "scenario_summary.csv").exists()
    assert (tmp_path / "audit_summary.md").exists()

    with duckdb.connect(str(tmp_path / "tax_automation.duckdb")) as con:
        result = con.execute("select count(*) from exception_report").fetchone()[0]
        scenario_rows = con.execute("select count(*) from scenario_summary").fetchone()[0]
        golden_breaks = con.execute("select count(*) from golden_comparison where not golden_match").fetchone()[0]

    assert result == 23
    assert scenario_rows > 10
    assert golden_breaks == 0
