import pandas as pd

from tax_automation_lab.io import read_yaml
from tax_automation_lab.rules_engine import classify_transactions
from tax_automation_lab.validation import normalise_transactions


def test_classifies_standard_sale_as_gst_taxable():
    rules = read_yaml("config/tax_rules.yaml")
    transactions = normalise_transactions(
        pd.DataFrame(
            [
                {
                    "transaction_id": "T1",
                    "transaction_date": "2026-07-01",
                    "entity": "DemoCo AU",
                    "business_unit": "AU Retail",
                    "supplier_customer": "Customer",
                    "account_code": "4000",
                    "transaction_type": "SALE",
                    "jurisdiction": "AU",
                    "counterparty_country": "AU",
                    "related_party": "false",
                    "net_amount": "100.00",
                    "supplied_gst_amount": "10.00",
                    "tax_invoice_available": "true",
                    "evidence_status": "COMPLETE",
                    "ledger_tax_category": "GST_TAXABLE",
                }
            ]
        )
    )

    classified = classify_transactions(transactions, rules)

    assert classified.loc[0, "tax_category"] == "GST_TAXABLE"
    assert classified.loc[0, "classification_rule_id"] == "SALES_STANDARD_GST"
    assert classified.loc[0, "calculated_gst"] == 10.00


def test_missing_tax_invoice_rule_takes_priority():
    rules = read_yaml("config/tax_rules.yaml")
    transactions = normalise_transactions(
        pd.DataFrame(
            [
                {
                    "transaction_id": "T2",
                    "transaction_date": "2026-07-01",
                    "entity": "DemoCo AU",
                    "business_unit": "Operations",
                    "supplier_customer": "Supplier",
                    "account_code": "5100",
                    "transaction_type": "EXPENSE",
                    "jurisdiction": "AU",
                    "counterparty_country": "AU",
                    "related_party": "false",
                    "net_amount": "100.00",
                    "supplied_gst_amount": "10.00",
                    "tax_invoice_available": "false",
                    "evidence_status": "MISSING",
                    "ledger_tax_category": "GST_TAXABLE",
                }
            ]
        )
    )

    classified = classify_transactions(transactions, rules)

    assert classified.loc[0, "tax_category"] == "NEEDS_REVIEW"
    assert classified.loc[0, "classification_rule_id"] == "MISSING_TAX_INVOICE_REVIEW"


def test_cross_border_related_party_recharge_goes_to_transfer_pricing_review():
    rules = read_yaml("config/tax_rules.yaml")
    transactions = normalise_transactions(
        pd.DataFrame(
            [
                {
                    "transaction_id": "T3",
                    "transaction_date": "2026-07-13",
                    "entity": "DemoCo Australia Ltd",
                    "business_unit": "Shared Services",
                    "supplier_customer": "DemoCo Singapore Pte Ltd",
                    "account_code": "8100",
                    "transaction_type": "INTERCOMPANY",
                    "jurisdiction": "CROSS_BORDER",
                    "counterparty_country": "SG",
                    "related_party": "true",
                    "net_amount": "240000.00",
                    "supplied_gst_amount": "0.00",
                    "tax_invoice_available": "true",
                    "evidence_status": "INCOMPLETE",
                    "ledger_tax_category": "TRANSFER_PRICING_REVIEW",
                }
            ]
        )
    )

    classified = classify_transactions(transactions, rules)

    assert classified.loc[0, "tax_category"] == "TRANSFER_PRICING_REVIEW"
    assert classified.loc[0, "classification_rule_id"] == "CROSS_BORDER_RELATED_PARTY_TRANSFER_PRICING"


def test_offshore_royalty_goes_to_withholding_review():
    rules = read_yaml("config/tax_rules.yaml")
    transactions = normalise_transactions(
        pd.DataFrame(
            [
                {
                    "transaction_id": "T4",
                    "transaction_date": "2026-07-14",
                    "entity": "DemoCo Australia Ltd",
                    "business_unit": "Technology",
                    "supplier_customer": "DemoCo IP Holdings LLC",
                    "account_code": "8200",
                    "transaction_type": "ROYALTY",
                    "jurisdiction": "CROSS_BORDER",
                    "counterparty_country": "US",
                    "related_party": "true",
                    "net_amount": "180000.00",
                    "supplied_gst_amount": "0.00",
                    "tax_invoice_available": "true",
                    "evidence_status": "INCOMPLETE",
                    "ledger_tax_category": "WHT_REVIEW",
                }
            ]
        )
    )

    classified = classify_transactions(transactions, rules)

    assert classified.loc[0, "tax_category"] == "WHT_REVIEW"
    assert classified.loc[0, "classification_rule_id"] == "FOREIGN_ROYALTY_WITHHOLDING_REVIEW"
