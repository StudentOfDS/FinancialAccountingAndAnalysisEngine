from __future__ import annotations

import pandas as pd

from financial_accounting_engine.analysis.financial_health import health_score
from financial_accounting_engine.analysis.red_flags import detect_red_flags


def build_stakeholder_report(df: pd.DataFrame) -> dict[str, object]:
    health = health_score(df)
    flags = detect_red_flags(df)
    latest = df.tail(1).iloc[0]
    sections = {
        "investor": [f"Net profit {latest.net_profit:,.2f}; ROE/ROA should be read with leverage and cash-flow quality.", f"Health band: {health['band']}"],
        "lender": [f"Operating cash flow {latest.operating_cash_flow:,.2f}; current liabilities {latest.current_liabilities:,.2f}.", "Stress survival depends on OCF and interest coverage."],
        "management": ["Focus on gross margin, expenses, asset turnover, collections, inventory turnover, and CCC.", f"Detected red flags: {len(flags)}"],
        "supplier": [f"Working capital {latest.current_assets - latest.current_liabilities:,.2f}; closing cash {latest.closing_cash:,.2f}.", "Short-term payment ability depends on liquid assets."],
        "owner_founder": [f"Profit growth and cash survival should be balanced with debt pressure; health score {health['score']}.", "Sustainability requires profit backed by operating cash flow."],
    }
    return {"health": health, "red_flags": flags, "sections": sections}
