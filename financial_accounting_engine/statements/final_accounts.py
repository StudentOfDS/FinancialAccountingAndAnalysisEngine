from __future__ import annotations

from financial_accounting_engine.statements.balance_sheet import build_balance_sheet
from financial_accounting_engine.statements.profit_and_loss import build_profit_and_loss
from financial_accounting_engine.statements.trading_account import build_trading_account


def build_final_accounts(trading_inputs: dict, pnl_inputs: dict, balance_sheet_inputs: dict) -> dict[str, object]:
    trading = build_trading_account(**trading_inputs)
    pnl = build_profit_and_loss(gross_profit=trading["gross_profit"], **pnl_inputs)
    bs = build_balance_sheet(net_profit=pnl["net_profit"], **balance_sheet_inputs)
    return {"trading_account": trading, "profit_and_loss": pnl, "balance_sheet": bs}
