# Tax Data Automation Audit Summary

Generated: sample output
Ruleset: `demo_gst_classification_rules` version `2026.08`

## Executive Summary

- Transactions processed: 12
- Exceptions requiring review: 4
- Exception rate: 33.3%

## Classification Summary

| Tax category | Transactions | Net amount | Calculated GST | Exceptions |
| --- | ---: | ---: | ---: | ---: |
| NEEDS_REVIEW | 3 | 1835.00 | 0.00 | 3 |
| GST_TAXABLE | 6 | 3460.00 | 346.00 | 1 |
| GST_FREE | 1 | 850.00 | 0.00 | 0 |
| INPUT_TAXED | 1 | 42.00 | 0.00 | 0 |
| OUT_OF_SCOPE | 1 | 4200.00 | 0.00 | 0 |

## Exception Themes

- classification needs review: 3
- ledger category differs from rules result: 3
- No matching classification rule: 2
- input validation issue: 2
- GST amount does not reconcile: 1
- GST claimed but tax invoice missing: 1

