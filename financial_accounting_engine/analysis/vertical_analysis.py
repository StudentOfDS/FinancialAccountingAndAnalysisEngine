from __future__ import annotations

import pandas as pd


def vertical_income_statement(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["revenue", "COGS", "gross_profit", "operating_expenses", "operating_profit", "interest_expense", "tax_expense", "net_profit"]
    out = df[["period", *cols]].copy()
    for col in cols:
        out[f"{col}_pct_of_revenue"] = out[col].div(out["revenue"].replace(0, pd.NA)) * 100
    return out


def vertical_balance_sheet(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["current_assets", "non_current_assets", "total_assets", "current_liabilities", "non_current_liabilities", "total_liabilities", "equity"]
    out = df[["period", *cols]].copy()
    base = out["total_assets"].replace(0, pd.NA)
    for col in cols:
        out[f"{col}_pct_of_assets"] = out[col].div(base) * 100
    return out
