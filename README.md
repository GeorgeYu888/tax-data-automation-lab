# Tax Data Automation Lab

Practical Python and SQL project for turning messy finance transactions into traceable tax automation outputs.

This repository is a portfolio project built around the kind of work described in tax transformation and data automation roles: clarify business rules, map finance data, validate inputs, classify transactions, reconcile expected outputs, and produce an audit-friendly exception report.

It uses synthetic data only. It is not tax advice and does not implement official Australian tax law.

## Why This Project Exists

Tax data automation is rarely just a calculator. The real work sits at the intersection of:

- business rules and exceptions
- finance and ERP-style data
- Python and SQL transformations
- data quality and reconciliation
- traceable documentation for review
- human judgement before production use

This lab demonstrates those habits in a compact, runnable project.

## What It Does

The pipeline ingests synthetic transaction data and reference tables, then:

1. validates required fields, values, dates and GST rates
2. applies configurable tax classification rules from YAML
3. calculates expected GST amounts for demo scenarios
4. reconciles calculated values against supplied ledger values
5. flags exceptions by severity and reason
6. writes clean outputs to CSV and DuckDB
7. generates a Markdown audit summary for reviewers

## Architecture

```text
data/raw/transactions.csv
data/reference/account_tax_rules.csv
config/tax_rules.yaml
        |
        v
tax_automation_lab/
  pipeline.py          orchestrates the workflow
  validation.py        data quality checks
  rules_engine.py      metadata-driven classification
  reconciliation.py    output comparison and exception flags
  reporting.py         markdown audit summary
        |
        v
outputs/
  clean_transactions.csv
  exception_report.csv
  reconciliation_summary.csv
  audit_summary.md
  tax_automation.duckdb
```

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m tax_automation_lab run
```

Run tests:

```bash
pytest
```

## Example Output

After running the pipeline, open:

- `outputs/audit_summary.md` for a reviewer-friendly summary
- `outputs/exception_report.csv` for records requiring human review
- `outputs/tax_automation.duckdb` for SQL exploration

Example SQL:

```sql
select
  tax_category,
  count(*) as transactions,
  round(sum(net_amount), 2) as net_amount,
  round(sum(calculated_gst), 2) as calculated_gst
from clean_transactions
group by tax_category
order by calculated_gst desc;
```

## Rules Covered

The demo rules classify transactions into:

- `GST_TAXABLE`
- `GST_FREE`
- `INPUT_TAXED`
- `OUT_OF_SCOPE`
- `NEEDS_REVIEW`

The rules are deliberately simplified. The goal is to show the automation pattern: transparent inputs, explicit rules, testable outputs and reviewer visibility.

## Deloitte-Relevant Skills Demonstrated

- Python pipeline design
- SQL/DuckDB analytical outputs
- configurable rules-based processing
- validation and reconciliation
- exception handling and audit trail
- reference data mapping
- technical documentation
- automated tests
- GitHub Actions CI
- careful distinction between automation support and tax specialist judgement

## What This Does Not Claim

This project does not claim production tax-engineering experience, accounting qualification, tax-adviser status, enterprise ERP implementation, or legal/tax correctness.

It is a practical learning and portfolio project showing readiness to work with tax specialists and engineers in a controlled data automation environment.

