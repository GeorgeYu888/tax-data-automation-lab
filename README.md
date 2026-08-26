# Tax Data Automation Lab

Practical Python and SQL project for turning messy enterprise finance transactions into traceable tax automation review outputs.

This repository is a portfolio project built around the kind of work described in tax transformation and data automation roles: clarify business rules, map finance data, validate inputs, classify transactions, reconcile expected outputs, route exceptions, and produce an audit-friendly review pack.

It uses synthetic data only. It is not tax advice and does not implement official Australian tax law.

## Why This Project Exists

Tax data automation is rarely just a calculator. The real work sits at the intersection of:

- business rules and exceptions
- finance and ERP-style data
- Python and SQL transformations
- data quality and reconciliation
- traceable documentation for review
- human judgement before production use

This lab demonstrates those habits in a compact, runnable project using synthetic data for a fictional listed-group style company.

## What It Does

The pipeline ingests synthetic transaction data and reference tables, then:

1. validates required fields, values, dates and GST rates
2. applies configurable tax classification rules from YAML
3. calculates expected GST amounts for demo scenarios
4. reconciles calculated values against supplied ledger values
5. flags exceptions by severity and reason
6. writes clean outputs to CSV and DuckDB
7. generates scenario summaries and a Markdown audit summary for reviewers

## Enterprise Scenarios Covered

The synthetic dataset includes 36 transactions across the kinds of data domains a large-company tax automation team may need to triage before specialist review:

| Scenario | Example automation control |
| --- | --- |
| Domestic taxable sales and supplier expenses | BAS/GST category mapping and GST amount reconciliation |
| Export sales | GST-free classification and evidence review pattern |
| Missing tax invoice | GST credit routed to exception queue |
| Intercompany recharges | consolidation elimination and ledger-category mismatch checks |
| Cross-border related-party service fees | transfer-pricing documentation review queue |
| Offshore royalties, interest and dividends | withholding-tax review queue |
| Imported digital services and imported goods | cross-border GST / import GST triage |
| Employee entertainment and fleet benefits | FBT evidence and private-use review queue |
| R&D prototype and contractor costs | R&D activity/expenditure evidence review queue |
| Managed investment trust and family business trust distributions | beneficiary, residency and entitlement evidence review |
| Capital equipment purchases | asset register and GST support review |
| Income tax provision and deferred tax journals | tax reporting review queue |
| Treasury hedging and derivative records | financial supply classification review |

The goal is not to encode final tax law. The goal is to show the automation layer that helps tax specialists find the records they need to review.

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
  scenario_summary.csv
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
- `outputs/scenario_summary.csv` for review workload grouped by business unit and tax category
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
- `TRANSFER_PRICING_REVIEW`
- `WHT_REVIEW`
- `FBT_REVIEW`
- `R_AND_D_REVIEW`
- `TRUST_DISTRIBUTION_REVIEW`
- `CONSOLIDATION_ELIMINATION`
- `REVERSE_CHARGE_REVIEW`
- `CAPEX_REVIEW`
- `TAX_PROVISION_REVIEW`
- `FINANCIAL_SUPPLY_REVIEW`

The rules are deliberately simplified. The goal is to show the automation pattern: transparent inputs, explicit rules, testable outputs and reviewer visibility.

## Deloitte-Relevant Skills Demonstrated

- Python pipeline design
- SQL/DuckDB analytical outputs
- configurable rules-based processing
- validation and reconciliation
- exception handling and audit trail
- enterprise review queue design
- cross-border and related-party data triage
- reference data mapping
- technical documentation
- automated tests
- GitHub Actions CI
- careful distinction between automation support and tax specialist judgement

## Source Assumptions

The scenario design is informed by public tax-administration themes such as GST/BAS, withholding, transfer pricing, consolidation, FBT, R&D, trust/fund distributions and tax reporting evidence requirements. See `docs/source_assumptions.md` for the boundary between realistic workflow design and simplified demo rules.

## What This Does Not Claim

This project does not claim production tax-engineering experience, accounting qualification, tax-adviser status, enterprise ERP implementation, or legal/tax correctness.

It is a practical learning and portfolio project showing readiness to work with tax specialists and engineers in a controlled data automation environment.
