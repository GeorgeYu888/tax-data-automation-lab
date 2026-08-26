# Portfolio Case Study

## Project

Tax Data Automation Lab

## Problem

Finance and tax teams often receive transaction data from different operational systems, entities and jurisdictions. Before specialists can rely on the data, they need to know:

- whether required fields are present
- whether account mappings are understood
- whether tax categories are explainable
- whether supplied tax amounts reconcile to rule-based expectations
- which records require human review
- which business units, entities or tax workstreams are creating the highest review load

Manual review is slow and inconsistent. A small automation pipeline can help by turning the review into a repeatable process with clear exceptions.

## What I Built

I built a Python and SQL workflow that ingests synthetic ERP-style transaction data, applies configurable tax classification rules, validates data quality, compares outputs against expected values, and produces an audit summary and review queue.

The project includes:

- a metadata-driven rules file in YAML
- synthetic finance transaction data for a fictional listed-group style company
- account reference data
- classification logic
- validation checks
- reconciliation checks
- exception report generation
- scenario-level review summaries
- DuckDB output for SQL review
- automated tests and GitHub Actions CI

## Enterprise Scenarios Modelled

The dataset includes 36 transactions across:

- BAS/GST classification for domestic sales, supplier expenses, exports, imported goods and adjustment notes
- missing tax invoice review
- intercompany recharges and consolidation-elimination checks
- cross-border related-party service fees for transfer-pricing review
- offshore royalties, interest and dividends for withholding-tax review
- employee entertainment and fleet benefits for FBT review
- R&D prototype and contractor costs requiring activity/expenditure evidence
- managed investment trust and family business trust distribution review
- capital equipment purchases requiring asset-register support
- income tax provision and deferred tax journals
- treasury hedging and derivative records requiring financial-supply classification

## Skills Demonstrated

- Python for data workflow automation
- SQL/DuckDB for analytical review
- data quality checks
- reconciliation and output comparison
- rules-based classification
- reference data mapping
- enterprise tax operations thinking
- human-in-the-loop review queue design
- audit-friendly documentation
- test-driven confidence for business logic

## Role Relevance

This project was designed around tax data automation work where analysts support tax specialists and engineers by turning complex rules and expected outcomes into repeatable logic.

It is especially relevant to a transition profile because it shows the practical bridge between business operations, data quality, process mapping, Python/SQL automation and careful reviewer escalation.

It is relevant to roles involving:

- tax transformation
- finance-data automation
- data-quality controls
- ERP or ledger data mapping
- rule-based processing
- AI-enabled business transformation

## Boundaries

This is a learning and portfolio project using simplified synthetic data. It does not claim:

- qualified tax advice
- accounting qualification
- production tax-engineering experience
- enterprise ERP implementation experience
- legal correctness of tax rules

The value is in the automation pattern: transparent assumptions, reviewable rules, clean outputs and human-in-the-loop exceptions.

## Next Iterations

- Add a Streamlit reviewer dashboard.
- Add Polars for larger local data processing.
- Add dbt-style SQL models and tests.
- Add an LLM-assisted reviewer-note generator that never sends or changes records without human approval.
