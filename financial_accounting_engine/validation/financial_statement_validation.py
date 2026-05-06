from __future__ import annotations

import pandas as pd

from financial_accounting_engine.validation.reconciliation import (
    reconcile_balance_sheet,
    reconcile_cash_flow,
)


def validate_statement_rows(df: pd.DataFrame) -> list[dict[str, object]]:
    issues = []
    for _, row in df.iterrows():
        cf = reconcile_cash_flow(row.opening_cash, row.operating_cash_flow, row.investing_cash_flow, row.financing_cash_flow, row.closing_cash)
        bs = reconcile_balance_sheet(row.total_assets, row.total_liabilities, row.equity)
        if not cf["balanced"]:
            issues.append({"period": row.period, "type": "cash_flow_mismatch", **cf})
        if not bs["balanced"]:
            issues.append({"period": row.period, "type": "balance_sheet_mismatch", **bs})
    return issues
