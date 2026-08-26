# Deloitte Tax Data Automation Mapping

This note maps the project to common requirements in a Tax Data Automation role. It is written for portfolio/interview use.

## Python and SQL

The project uses Python modules to orchestrate validation, classification, reconciliation and reporting. It writes outputs to DuckDB so reviewers can query clean transactions, exception reports and summaries with SQL.

## Rules-Based Processing

The YAML rules file separates business logic from Python code. This makes the rules easier for a tax specialist, analyst or engineer to review and refine.

## Data Quality and Reconciliation

The pipeline checks for missing or invalid data, unknown account mappings, mismatched tax categories and GST amount differences. It preserves exceptions instead of hiding them.

## Reference Data

The account reference file simulates the kind of mapping table often needed between source finance systems and tax/reporting logic.

## Traceability

Every classified transaction includes the rule ID that produced the result. The exception report keeps the input issue, classification result and reconciliation difference together.

## Automated Tests

Tests cover key business logic and the end-to-end pipeline. The GitHub Actions workflow runs the test suite and demo pipeline on each push or pull request.

## Human Review

The project deliberately avoids presenting automation as final tax judgement. Exceptions are routed to a reviewer because tax automation should support specialists, not pretend domain judgement is unnecessary.

