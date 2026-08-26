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
                    "supplier_customer": "Customer",
                    "account_code": "4000",
                    "transaction_type": "SALE",
                    "jurisdiction": "AU",
                    "net_amount": "100.00",
                    "supplied_gst_amount": "10.00",
                    "tax_invoice_available": "true",
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
                    "supplier_customer": "Supplier",
                    "account_code": "5100",
                    "transaction_type": "EXPENSE",
                    "jurisdiction": "AU",
                    "net_amount": "100.00",
                    "supplied_gst_amount": "10.00",
                    "tax_invoice_available": "false",
                    "ledger_tax_category": "GST_TAXABLE",
                }
            ]
        )
    )

    classified = classify_transactions(transactions, rules)

    assert classified.loc[0, "tax_category"] == "NEEDS_REVIEW"
    assert classified.loc[0, "classification_rule_id"] == "MISSING_TAX_INVOICE_REVIEW"

