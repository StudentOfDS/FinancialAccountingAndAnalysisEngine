from __future__ import annotations

from pydantic import BaseModel


class FinancialStatementRow(BaseModel):
    period: str
    revenue: float
    COGS: float
    gross_profit: float
    operating_expenses: float
    operating_profit: float
    interest_expense: float
    tax_expense: float
    net_profit: float
    current_assets: float
    non_current_assets: float
    total_assets: float
    current_liabilities: float
    non_current_liabilities: float
    total_liabilities: float
    equity: float
    operating_cash_flow: float
    investing_cash_flow: float
    financing_cash_flow: float
    opening_cash: float
    closing_cash: float
