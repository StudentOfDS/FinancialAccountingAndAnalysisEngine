from __future__ import annotations


def build_income_statement(revenue: float, COGS: float, operating_expenses: float, interest_expense: float, tax_expense: float) -> dict[str, float]:
    gross_profit = revenue - COGS
    operating_profit = gross_profit - operating_expenses
    net_profit = operating_profit - interest_expense - tax_expense
    return {"revenue": revenue, "COGS": COGS, "gross_profit": gross_profit, "operating_expenses": operating_expenses, "operating_profit": operating_profit, "interest_expense": interest_expense, "tax_expense": tax_expense, "net_profit": net_profit}
