from __future__ import annotations

import pandas as pd

from financial_accounting_engine.analysis.dupont import dupont_analysis
from financial_accounting_engine.analysis.ratios import calculate_ratios


def detect_red_flags(df: pd.DataFrame) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []
    ratios = calculate_ratios(df)
    pivot = ratios.pivot(index="period", columns="ratio_name", values="value") if not ratios.empty else pd.DataFrame()
    dup = dupont_analysis(df)
    for i, row in enumerate(df.itertuples(index=False)):
        period = str(row.period)
        if row.net_profit > 0 and row.operating_cash_flow < 0:
            flags.append(_flag(period, "Positive net profit but negative OCF", "Cash quality risk"))
        if row.current_assets - row.current_liabilities < 0:
            flags.append(_flag(period, "Negative working capital", "Liquidity pressure"))
        if i > 0:
            prev = df.iloc[i - 1]
            if row.revenue > prev.revenue and row.net_profit < prev.net_profit:
                flags.append(_flag(period, "Revenue up but net profit down", "Margins or expenses deteriorated"))
            if row.operating_expenses / row.revenue > prev.operating_expenses / prev.revenue:
                flags.append(_flag(period, "Expenses growing faster than revenue", "Cost control issue"))
            if row.gross_profit / row.revenue < prev.gross_profit / prev.revenue:
                flags.append(_flag(period, "Declining gross margin", "Pricing or COGS pressure"))
            if row.closing_cash < prev.closing_cash:
                flags.append(_flag(period, "Falling closing cash", "Cash balance declined"))
        if not pivot.empty and period in pivot.index:
            vals = pivot.loc[period]
            if vals.get("current_ratio") is not None and vals.get("current_ratio") < 1:
                flags.append(_flag(period, "Weak current ratio", "Current assets do not cover current liabilities"))
            if vals.get("quick_ratio") is not None and vals.get("quick_ratio") < 1:
                flags.append(_flag(period, "Weak quick ratio", "Immediate liquidity is weak"))
        dup_row = dup[dup.period == period]
        if not dup_row.empty and dup_row.iloc[0].warning:
            flags.append(_flag(period, "ROE rising only from leverage", dup_row.iloc[0].warning))
    return flags


def _flag(period: str, title: str, detail: str) -> dict[str, str]:
    return {"period": period, "flag": title, "detail": detail}
