# Deloitte Tax Data Automation Mapping

This note maps the project to common requirements in a Tax Data Automation role. It is written for portfolio/interview use.

## Positioning

This project is designed to show readiness for the technology, data, process and automation layer of tax transformation work. It does not present the builder as a qualified accountant, tax adviser or production tax-engineer. The value is in converting messy finance records into traceable outputs that a tax specialist can review.

## Python and SQL

The project uses Python modules to orchestrate validation, classification, reconciliation and reporting. It writes outputs to DuckDB so reviewers can query clean transactions, exception reports and summaries with SQL.

## Enterprise Tax Scenarios

The synthetic dataset is shaped around large-company and listed-group style workflows:

- BAS/GST classification for domestic sales, supplier expenses, exports, imports and adjustment notes
- intercompany and consolidation-elimination triage
- cross-border related-party management fees for transfer-pricing review
- offshore royalty, interest and dividend payments for withholding-tax review
- employee entertainment and fleet records for FBT evidence review
- R&D expenditure tagged to projects and overseas contractors
- managed investment trust and family-business trust distribution review
- capital expenditure requiring asset-register support
- income tax provision and deferred tax journal review
- treasury hedging and derivative records requiring financial-supply classification

## Rules-Based Processing

The YAML rules file separates business logic from Python code. This makes the rules easier for a tax specialist, analyst or engineer to review and refine.

## Data Quality and Reconciliation

The pipeline checks for missing or invalid data, unknown account mappings, mismatched tax categories, GST amount differences, incomplete evidence, related-party evidence gaps and cross-border metadata gaps. It preserves exceptions instead of hiding them.

## Reference Data

The account reference file simulates the kind of mapping table often needed between source finance systems and tax/reporting logic.

## Traceability

Every classified transaction includes the rule ID that produced the result. The exception report keeps the input issue, entity, business unit, counterparty country, related-party flag, evidence status, classification result and reconciliation difference together.

## Review Queue Thinking

The project writes `scenario_summary.csv` so a reviewer can quickly see which business units and tax categories are producing the most exceptions. This is closer to a tax operations workflow than a single calculation script.

## Automated Tests

Tests cover key business logic and the end-to-end pipeline. The GitHub Actions workflow runs the test suite and demo pipeline on each push or pull request.

The golden expected output file acts as a regression baseline. The pipeline writes a `golden_comparison` table to DuckDB and tests assert that no expected-output breaks are present.

## Human Review

The project deliberately avoids presenting automation as final tax judgement. Exceptions are routed to a reviewer because tax automation should support specialists, not pretend domain judgement is unnecessary.
