from __future__ import annotations

import pandas as pd

from financial_accounting_engine.utils.math_helpers import safe_divide


def calculate_ratios(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    prev_inventory = prev_receivables = prev_payables = None
    for r in df.itertuples(index=False):
        inventory = float(getattr(r, "inventory", 0.0))
        prepaid = float(getattr(r, "prepaid_expenses", 0.0))
        cash = float(getattr(r, "closing_cash", 0.0))
        receivables = float(getattr(r, "receivables", 0.0))
        payables = float(getattr(r, "payables", 0.0))
        total_debt = float(r.total_liabilities)
        ebit = float(r.operating_profit)
        period = str(r.period)
        metrics = {
            "current_ratio": (r.current_assets, r.current_liabilities),
            "quick_ratio": (r.current_assets - inventory - prepaid, r.current_liabilities),
            "cash_ratio": (cash, r.current_liabilities),
            "debt_equity": (total_debt, r.equity),
            "debt_ratio": (total_debt, r.total_assets),
            "interest_coverage": (ebit, r.interest_expense),
            "gross_profit_ratio": (r.gross_profit, r.revenue),
            "operating_profit_ratio": (r.operating_profit, r.revenue),
            "net_profit_ratio": (r.net_profit, r.revenue),
            "ROA": (r.net_profit, r.total_assets),
            "ROE": (r.net_profit, r.equity),
            "asset_turnover": (r.revenue, r.total_assets),
        }
        avg_inventory = _avg(prev_inventory, inventory)
        avg_receivables = _avg(prev_receivables, receivables)
        avg_payables = _avg(prev_payables, payables)
        metrics.update({
            "inventory_turnover": (r.COGS, avg_inventory),
            "debtors_turnover": (getattr(r, "credit_sales", r.revenue), avg_receivables),
            "creditors_turnover": (getattr(r, "credit_purchases", r.COGS), avg_payables),
        })
        dio = safe_divide(365, safe_divide(r.COGS, avg_inventory, name="inventory_turnover").value or 0, name="DIO")
        dso = safe_divide(365, safe_divide(getattr(r, "credit_sales", r.revenue), avg_receivables, name="debtors_turnover").value or 0, name="DSO")
        dpo = safe_divide(365, safe_divide(getattr(r, "credit_purchases", r.COGS), avg_payables, name="creditors_turnover").value or 0, name="DPO")
        for name, (num, den) in metrics.items():
            metric = safe_divide(num, den, name=name)
            rows.append({"period": period, "ratio_name": name, "value": metric.value, "interpretation": metric.interpretation, "warning": metric.warning})
        for metric in [dio, dso, dpo]:
            rows.append({"period": period, "ratio_name": metric.name, "value": metric.value, "interpretation": metric.interpretation, "warning": metric.warning})
        if dio.value is None or dso.value is None or dpo.value is None:
            ccc = None
        else:
            ccc = dio.value + dso.value - dpo.value
        rows.append({"period": period, "ratio_name": "cash_conversion_cycle", "value": ccc, "interpretation": "Lower CCC generally indicates faster cash recovery." if ccc is not None else "Not meaningful without inventory/receivable/payable data.", "warning": None if ccc is not None else "missing_working_capital_components"})
        prev_inventory, prev_receivables, prev_payables = inventory, receivables, payables
    return pd.DataFrame(rows)


def _avg(prev, current: float) -> float:
    return current if prev is None else (float(prev) + current) / 2
