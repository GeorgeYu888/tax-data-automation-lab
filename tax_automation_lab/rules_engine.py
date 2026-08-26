from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    tax_category: str
    expected_gst_rate: float | None
    review_reason: str


def classify_transactions(transactions: pd.DataFrame, rules_config: dict[str, Any]) -> pd.DataFrame:
    rules = sorted(rules_config.get("rules", []), key=lambda rule: int(rule.get("priority", 999)))
    defaults = rules_config.get("defaults", {})

    classified = transactions.copy()
    results = [_classify_row(row, rules, defaults) for _, row in classified.iterrows()]
    classified["classification_rule_id"] = [result.rule_id for result in results]
    classified["tax_category"] = [result.tax_category for result in results]
    classified["expected_gst_rate"] = [result.expected_gst_rate for result in results]
    classified["review_reason"] = [result.review_reason for result in results]
    classified["calculated_gst"] = classified.apply(_calculate_gst, axis=1)
    return classified


def _classify_row(row: pd.Series, rules: list[dict[str, Any]], defaults: dict[str, Any]) -> RuleResult:
    for rule in rules:
        if _matches(row, rule.get("conditions", {})):
            result = rule["result"]
            return RuleResult(
                rule_id=rule["id"],
                tax_category=result["tax_category"],
                expected_gst_rate=result.get("expected_gst_rate"),
                review_reason=result.get("review_reason", ""),
            )
    return RuleResult(
        rule_id="DEFAULT_REVIEW",
        tax_category=defaults.get("tax_category", "NEEDS_REVIEW"),
        expected_gst_rate=defaults.get("expected_gst_rate"),
        review_reason=defaults.get("review_reason", "No matching classification rule"),
    )


def _matches(row: pd.Series, conditions: dict[str, Any]) -> bool:
    for key, expected in conditions.items():
        if key.endswith("_in"):
            column = key.removesuffix("_in")
            if row[column] not in expected:
                return False
        elif key.endswith("_gt"):
            column = key.removesuffix("_gt")
            if not row[column] > expected:
                return False
        else:
            raise ValueError(f"Unsupported condition operator: {key}")
    return True


def _calculate_gst(row: pd.Series) -> float | None:
    if pd.isna(row["expected_gst_rate"]):
        return None
    return round(float(row["net_amount"]) * float(row["expected_gst_rate"]), 2)

