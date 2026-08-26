from __future__ import annotations

import pandas as pd


def reconcile(classified: pd.DataFrame, validation_issues: pd.DataFrame, tolerance: float = 0.01) -> pd.DataFrame:
    frame = classified.copy()
    issue_counts = _issue_counts(validation_issues)

    frame["gst_difference"] = frame.apply(_gst_difference, axis=1)
    frame["category_match"] = frame["tax_category"] == frame["ledger_tax_category"]
    frame["gst_match"] = frame["gst_difference"].apply(lambda value: True if pd.isna(value) else abs(value) <= tolerance)
    frame["validation_issue_count"] = frame["transaction_id"].map(issue_counts).fillna(0).astype(int)
    frame["exception_flag"] = frame.apply(_exception_flag, axis=1)
    frame["exception_reason"] = frame.apply(_exception_reason, axis=1)
    return frame


def build_exception_report(reconciled: pd.DataFrame, validation_issues: pd.DataFrame) -> pd.DataFrame:
    exceptions = reconciled[reconciled["exception_flag"]].copy()
    if validation_issues.empty:
        issue_summary = pd.DataFrame(columns=["transaction_id", "validation_issues"])
    else:
        issue_rows = []
        for transaction_id, group in validation_issues.groupby("transaction_id"):
            issue_rows.append(
                {
                    "transaction_id": transaction_id,
                    "validation_issues": "; ".join(
                        f"{row.issue_code}: {row.issue_detail}" for row in group.itertuples()
                    ),
                }
            )
        issue_summary = pd.DataFrame(issue_rows)

    report = exceptions.merge(issue_summary, on="transaction_id", how="left")
    columns = [
        "transaction_id",
        "transaction_date",
        "supplier_customer",
        "account_code",
        "transaction_type",
        "jurisdiction",
        "net_amount",
        "supplied_gst_amount",
        "calculated_gst",
        "gst_difference",
        "ledger_tax_category",
        "tax_category",
        "classification_rule_id",
        "exception_reason",
        "validation_issues",
        "review_reason",
    ]
    return report[columns].sort_values(["transaction_id"])


def build_summary(reconciled: pd.DataFrame) -> pd.DataFrame:
    return (
        reconciled.groupby("tax_category", dropna=False)
        .agg(
            transactions=("transaction_id", "count"),
            net_amount=("net_amount", "sum"),
            calculated_gst=("calculated_gst", "sum"),
            exceptions=("exception_flag", "sum"),
        )
        .reset_index()
        .sort_values(["exceptions", "transactions"], ascending=[False, False])
    )


def _issue_counts(validation_issues: pd.DataFrame) -> dict[str, int]:
    if validation_issues.empty:
        return {}
    return validation_issues.groupby("transaction_id").size().to_dict()


def _gst_difference(row: pd.Series) -> float | None:
    if pd.isna(row["calculated_gst"]):
        return None
    return round(float(row["supplied_gst_amount"]) - float(row["calculated_gst"]), 2)


def _exception_flag(row: pd.Series) -> bool:
    return bool(
        row["tax_category"] == "NEEDS_REVIEW"
        or not row["category_match"]
        or not row["gst_match"]
        or row["validation_issue_count"] > 0
        or bool(row["review_reason"])
    )


def _exception_reason(row: pd.Series) -> str:
    reasons: list[str] = []
    if row["tax_category"] == "NEEDS_REVIEW":
        reasons.append("classification needs review")
    if not row["category_match"]:
        reasons.append("ledger category differs from rules result")
    if not row["gst_match"]:
        reasons.append("GST amount does not reconcile")
    if row["validation_issue_count"] > 0:
        reasons.append("input validation issue")
    if bool(row["review_reason"]):
        reasons.append(str(row["review_reason"]))
    return "; ".join(dict.fromkeys(reasons))
