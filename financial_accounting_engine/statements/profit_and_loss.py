from __future__ import annotations


def build_profit_and_loss(gross_profit: float, indirect_income: float = 0.0, admin_expenses: float = 0.0, selling_expenses: float = 0.0, distribution_expenses: float = 0.0, finance_costs: float = 0.0, depreciation: float = 0.0, bad_debts: float = 0.0, provisions: float = 0.0, other_operating_expenses: float = 0.0) -> dict[str, float]:
    indirect_expenses = admin_expenses + selling_expenses + distribution_expenses + finance_costs + depreciation + bad_debts + provisions + other_operating_expenses
    net_profit = gross_profit + indirect_income - indirect_expenses
    return {"gross_profit": gross_profit, "indirect_income": indirect_income, "indirect_expenses": indirect_expenses, "depreciation": depreciation, "finance_costs": finance_costs, "net_profit": net_profit}
