# Tax Data Automation Audit Summary

Generated: 2026-08-26 01:18:03 UTC
Ruleset: `enterprise_tax_automation_demo_rules` version `2026.08-enterprise`

## Executive Summary

- Transactions processed: 36
- Exceptions requiring review: 23
- Exception rate: 63.9%

## Classification Summary

| Tax category | Transactions | Net amount | Calculated GST | Exceptions |
| --- | ---: | ---: | ---: | ---: |
| GST_TAXABLE | 10 | 121760.00 | 12176.00 | 3 |
| WHT_REVIEW | 3 | 585000.00 | 0.00 | 3 |
| CONSOLIDATION_ELIMINATION | 3 | 213725.00 | 0.00 | 2 |
| FBT_REVIEW | 2 | 3650.00 | 365.00 | 2 |
| FINANCIAL_SUPPLY_REVIEW | 2 | 36000.00 | 0.00 | 2 |
| NEEDS_REVIEW | 2 | 1110.00 | 0.00 | 2 |
| R_AND_D_REVIEW | 2 | 90000.00 | 3800.00 | 2 |
| TAX_PROVISION_REVIEW | 2 | 555000.00 | 0.00 | 2 |
| TRUST_DISTRIBUTION_REVIEW | 2 | 106000.00 | 0.00 | 2 |
| CAPEX_REVIEW | 1 | 450000.00 | 45000.00 | 1 |
| REVERSE_CHARGE_REVIEW | 1 | 76000.00 | 0.00 | 1 |
| TRANSFER_PRICING_REVIEW | 1 | 240000.00 | 0.00 | 1 |
| INPUT_TAXED | 2 | 2442.00 | 0.00 | 0 |
| OUT_OF_SCOPE | 2 | 26200.00 | 0.00 | 0 |
| GST_FREE | 1 | 850.00 | 0.00 | 0 |

## Exception Themes

- input validation issue: 9
- ledger category differs from rules result: 4
- GST amount does not reconcile: 3
- Employee benefit record requires FBT evidence and private-use review: 2
- Tax provision journal requires tax reporting review: 2
- Treasury or investment transaction requires financial supply classification review: 2
- Trust or fund distribution requires beneficiary, residency and entitlement evidence review: 2
- classification needs review: 2
- Capital purchase requires asset register and GST credit support: 1
- GST claimed but supporting tax invoice is missing: 1
- Imported service requires cross-border GST treatment review: 1
- No matching classification rule: 1
- Offshore dividend distribution requires franking and withholding evidence review: 1
- Offshore interest payment requires withholding tax and funding evidence review: 1
- Offshore royalty payment requires withholding tax and treaty evidence review: 1
- Overseas R&D-tagged expenditure requires eligibility and supporting evidence review: 1
- R&D-tagged expenditure requires activity and apportionment evidence review: 1
- Related-party cross-border transaction requires transfer pricing documentation review: 1

## Enterprise Scenario Summary

| Business unit | Tax category | Transactions | Related party | Cross-border | Net amount | Exceptions |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Tax | TAX_PROVISION_REVIEW | 2 | 0 | 0 | 555000.00 | 2 |
| Treasury | WHT_REVIEW | 2 | 2 | 2 | 405000.00 | 2 |
| Corporate | CONSOLIDATION_ELIMINATION | 3 | 3 | 0 | 213725.00 | 2 |
| Product Lab | R_AND_D_REVIEW | 2 | 0 | 1 | 90000.00 | 2 |
| Treasury | FINANCIAL_SUPPLY_REVIEW | 2 | 0 | 1 | 36000.00 | 2 |
| People | FBT_REVIEW | 2 | 0 | 0 | 3650.00 | 2 |
| Corporate | GST_TAXABLE | 5 | 0 | 0 | 520.00 | 2 |
| Operations | CAPEX_REVIEW | 1 | 0 | 0 | 450000.00 | 1 |
| Shared Services | TRANSFER_PRICING_REVIEW | 1 | 1 | 1 | 240000.00 | 1 |
| Technology | WHT_REVIEW | 1 | 1 | 1 | 180000.00 | 1 |
| Technology | REVERSE_CHARGE_REVIEW | 1 | 0 | 1 | 76000.00 | 1 |
| Investor Relations | TRUST_DISTRIBUTION_REVIEW | 1 | 0 | 0 | 64000.00 | 1 |

## Reviewer Notes

- This output is designed for human review, not automatic tax lodgement.
- Rules are simplified and intentionally transparent so a tax specialist can challenge or refine them.
- Exceptions are preserved instead of hidden, because traceability matters in tax and finance workflows.
- The synthetic data includes clean records, missing evidence, unknown mappings, reconciliation breaks, related-party transactions, offshore payments, employee benefits, R&D costs, trust/fund distributions, consolidation eliminations and treasury items.

## Next Improvements

- Add a Streamlit dashboard for reviewer triage.
- Add dbt-style SQL models and tests.
- Add Polars implementation for larger local files.
- Add a lightweight LLM prompt that drafts reviewer notes from exception rows, with human approval.
