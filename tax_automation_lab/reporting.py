from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd


def render_audit_summary(
    reconciled: pd.DataFrame,
    exceptions: pd.DataFrame,
    summary: pd.DataFrame,
    scenario_summary: pd.DataFrame,
    ruleset_name: str,
    ruleset_version: str,
) -> str:
    total = len(reconciled)
    exception_count = len(exceptions)
    exception_rate = (exception_count / total) if total else 0
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Tax Data Automation Audit Summary",
        "",
        f"Generated: {generated_at}",
        f"Ruleset: `{ruleset_name}` version `{ruleset_version}`",
        "",
        "## Executive Summary",
        "",
        f"- Transactions processed: {total}",
        f"- Exceptions requiring review: {exception_count}",
        f"- Exception rate: {exception_rate:.1%}",
        "",
        "## Classification Summary",
        "",
        "| Tax category | Transactions | Net amount | Calculated GST | Exceptions |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for row in summary.itertuples():
        lines.append(
            f"| {row.tax_category} | {row.transactions} | {row.net_amount:.2f} | "
            f"{row.calculated_gst:.2f} | {row.exceptions} |"
        )

    lines.extend(["", "## Exception Themes", ""])
    if exceptions.empty:
        lines.append("- No exceptions were generated.")
    else:
        for reason, count in _reason_counts(exceptions).items():
            lines.append(f"- {reason}: {count}")

    lines.extend(
        [
            "",
            "## Enterprise Scenario Summary",
            "",
            "| Business unit | Tax category | Transactions | Related party | Cross-border | Net amount | Exceptions |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in scenario_summary.head(12).itertuples():
        lines.append(
            f"| {row.business_unit} | {row.tax_category} | {row.transactions} | "
            f"{row.related_party_transactions} | {row.cross_border_transactions} | "
            f"{row.net_amount:.2f} | {row.exceptions} |"
        )

    lines.extend(
        [
            "",
            "## Reviewer Notes",
            "",
            "- This output is designed for human review, not automatic tax lodgement.",
            "- Rules are simplified and intentionally transparent so a tax specialist can challenge or refine them.",
            "- Exceptions are preserved instead of hidden, because traceability matters in tax and finance workflows.",
            "- The synthetic data includes clean records, missing evidence, unknown mappings, reconciliation breaks, related-party transactions, offshore payments, employee benefits, R&D costs, trust/fund distributions, consolidation eliminations and treasury items.",
            "",
            "## Next Improvements",
            "",
            "- Add a Streamlit dashboard for reviewer triage.",
            "- Add dbt-style SQL models and tests.",
            "- Add Polars implementation for larger local files.",
            "- Add a lightweight LLM prompt that drafts reviewer notes from exception rows, with human approval.",
        ]
    )
    return "\n".join(lines) + "\n"


def _reason_counts(exceptions: pd.DataFrame) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in exceptions["exception_reason"].fillna("unspecified"):
        for reason in str(value).split("; "):
            if reason:
                counts[reason] = counts.get(reason, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
