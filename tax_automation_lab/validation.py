from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "entity",
    "supplier_customer",
    "account_code",
    "transaction_type",
    "jurisdiction",
    "net_amount",
    "supplied_gst_amount",
    "tax_invoice_available",
    "ledger_tax_category",
]


def normalise_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    frame = transactions.copy()
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    frame["transaction_id"] = frame["transaction_id"].astype(str).str.strip()
    frame["account_code"] = frame["account_code"].astype(str).str.strip()
    frame["transaction_type"] = frame["transaction_type"].astype(str).str.strip().str.upper()
    frame["jurisdiction"] = frame["jurisdiction"].astype(str).str.strip().str.upper()
    frame["ledger_tax_category"] = frame["ledger_tax_category"].astype(str).str.strip().str.upper()
    frame["tax_invoice_available"] = frame["tax_invoice_available"].map(_to_bool)
    frame["transaction_date"] = pd.to_datetime(frame["transaction_date"], errors="coerce")
    frame["net_amount"] = pd.to_numeric(frame["net_amount"], errors="coerce")
    frame["supplied_gst_amount"] = pd.to_numeric(frame["supplied_gst_amount"], errors="coerce")
    return frame


def validate_transactions(transactions: pd.DataFrame, account_rules: pd.DataFrame) -> pd.DataFrame:
    known_accounts = set(account_rules["account_code"].astype(str))
    issues: list[dict[str, object]] = []

    for _, row in transactions.iterrows():
        transaction_id = row["transaction_id"]
        if not transaction_id:
            issues.append(_issue(transaction_id, "CRITICAL", "MISSING_TRANSACTION_ID", "Transaction ID is blank"))
        if pd.isna(row["transaction_date"]):
            issues.append(_issue(transaction_id, "HIGH", "INVALID_DATE", "Transaction date could not be parsed"))
        if pd.isna(row["net_amount"]):
            issues.append(_issue(transaction_id, "HIGH", "INVALID_NET_AMOUNT", "Net amount is not numeric"))
        if pd.isna(row["supplied_gst_amount"]):
            issues.append(_issue(transaction_id, "HIGH", "INVALID_GST_AMOUNT", "Supplied GST amount is not numeric"))
        if row["account_code"] not in known_accounts:
            issues.append(_issue(transaction_id, "MEDIUM", "UNKNOWN_ACCOUNT_CODE", "Account code is not in reference mapping"))
        if row["transaction_type"] not in {"SALE", "EXPENSE", "PAYROLL"}:
            issues.append(_issue(transaction_id, "MEDIUM", "UNKNOWN_TRANSACTION_TYPE", "Transaction type is outside configured values"))
        if pd.notna(row["net_amount"]) and pd.notna(row["supplied_gst_amount"]):
            if row["net_amount"] == 0 and row["supplied_gst_amount"] != 0:
                issues.append(_issue(transaction_id, "HIGH", "GST_ON_ZERO_NET", "GST cannot be reconciled against zero net amount"))
            if abs(row["supplied_gst_amount"]) > abs(row["net_amount"]):
                issues.append(_issue(transaction_id, "HIGH", "GST_EXCEEDS_NET", "GST amount is larger than net amount"))

    return pd.DataFrame(issues, columns=["transaction_id", "severity", "issue_code", "issue_detail"])


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _issue(transaction_id: object, severity: str, code: str, detail: str) -> dict[str, object]:
    return {
        "transaction_id": transaction_id,
        "severity": severity,
        "issue_code": code,
        "issue_detail": detail,
    }

