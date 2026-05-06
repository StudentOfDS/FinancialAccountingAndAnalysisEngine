from __future__ import annotations

from financial_accounting_engine.validation.reconciliation import reconcile_cash_flow


def build_cash_flow(opening_cash: float, customer_receipts: float = 0, supplier_payments: float = 0, salaries: float = 0, rent: float = 0, tax: float = 0, interest: float = 0, fixed_asset_purchases: float = 0, fixed_asset_sales: float = 0, investments: float = 0, loans: float = 0, loan_repayment: float = 0, capital_introduced: float = 0, share_issue: float = 0, dividend: float = 0, drawings: float = 0, reported_closing_cash: float | None = None) -> dict[str, object]:
    operating = customer_receipts - supplier_payments - salaries - rent - tax - interest
    investing = fixed_asset_sales - fixed_asset_purchases - investments
    financing = loans - loan_repayment + capital_introduced + share_issue - dividend - drawings
    closing = opening_cash + operating + investing + financing
    rec = reconcile_cash_flow(opening_cash, operating, investing, financing, closing if reported_closing_cash is None else reported_closing_cash)
    return {"operating_cash_flow": operating, "investing_cash_flow": investing, "financing_cash_flow": financing, "opening_cash": opening_cash, "closing_cash": closing, **rec}
