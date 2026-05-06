from __future__ import annotations

import pandas as pd

from financial_accounting_engine.analysis.ratios import calculate_ratios


def build_pro_forma(latest: pd.Series, revenue_growth: float, margin_change: float = 0.0, expense_ratio_change: float = 0.0) -> dict[str, object]:
    revenue = float(latest.revenue) * (1 + revenue_growth)
    gross_margin = (float(latest.gross_profit) / float(latest.revenue) if latest.revenue else 0) + margin_change
    gross_profit = revenue * gross_margin
    operating_expenses = revenue * ((float(latest.operating_expenses) / float(latest.revenue) if latest.revenue else 0) + expense_ratio_change)
    operating_profit = gross_profit - operating_expenses
    net_profit = operating_profit - float(latest.interest_expense) - float(latest.tax_expense)
    current_assets = float(latest.current_assets) * (1 + revenue_growth)
    non_current_assets = float(latest.non_current_assets)
    total_assets = current_assets + non_current_assets
    total_liabilities = float(latest.total_liabilities)
    equity = total_assets - total_liabilities
    row = pd.DataFrame([{**latest.to_dict(), "revenue": revenue, "gross_profit": gross_profit, "operating_expenses": operating_expenses, "operating_profit": operating_profit, "net_profit": net_profit, "current_assets": current_assets, "non_current_assets": non_current_assets, "total_assets": total_assets, "equity": equity}])
    return {"statements": row, "ratios": calculate_ratios(row)}
