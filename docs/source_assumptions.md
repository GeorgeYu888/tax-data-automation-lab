# Source Assumptions and Boundaries

This project is a synthetic portfolio lab. It is designed to demonstrate tax data automation patterns, not to provide tax advice or implement authoritative tax calculations.

## Public Guidance Themes Referenced

The scenario design was informed by public tax-administration themes, including:

- ATO Business Activity Statement and GST classification concepts: taxable supplies, GST-free supplies, input taxed supplies, GST credits, GST adjustments and PAYG-related reporting workflows.
- ATO foreign-resident withholding themes for offshore royalty, interest and dividend payments.
- ATO transfer-pricing documentation themes for related-party cross-border dealings.
- ATO tax-consolidation themes for wholly owned corporate groups and consolidation treatment.
- ATO FBT themes for employee entertainment, fleet and private-use evidence.
- ATO R&D Tax Incentive themes for activity/expenditure evidence and apportionment.
- ATO managed investment trust and trust distribution themes for beneficiary, residency, entitlement and withholding review.

## Automation Boundary

The rules in `config/tax_rules.yaml` are deliberately simplified. They are not official tax rules, tax-rate guidance, treaty logic, legal interpretation or lodgement logic.

The realistic part of the project is the workflow:

- structure messy finance records
- preserve entity, business-unit, jurisdiction and related-party context
- separate reviewable rules from code
- detect incomplete evidence and ledger mismatches
- produce exception queues rather than silent classifications
- create SQL-readable outputs for review
- compare results against a golden expected-output baseline

## Human Review Model

In a real tax team, this type of pipeline would sit before specialist review. Tax specialists would own the interpretation, rates, legal positions, lodgement decisions and final approvals.

