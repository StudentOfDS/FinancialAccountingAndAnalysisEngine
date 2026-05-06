from __future__ import annotations

from financial_accounting_engine.validation.reconciliation import reconcile_balance_sheet


def build_balance_sheet(non_current_assets: float, current_assets: float, capital: float, drawings: float, net_profit: float, current_liabilities: float, non_current_liabilities: float) -> dict[str, object]:
    total_assets = non_current_assets + current_assets
    equity = capital - drawings + net_profit
    total_liabilities = current_liabilities + non_current_liabilities
    rec = reconcile_balance_sheet(total_assets, total_liabilities, equity)
    return {"non_current_assets": non_current_assets, "current_assets": current_assets, "total_assets": total_assets, "capital": capital, "drawings": drawings, "equity": equity, "current_liabilities": current_liabilities, "non_current_liabilities": non_current_liabilities, "total_liabilities": total_liabilities, **rec}
