from __future__ import annotations


def reconcile_cash_flow(opening_cash: float, operating: float, investing: float, financing: float, closing_cash: float, tolerance: float = 0.01) -> dict[str, object]:
    expected = opening_cash + operating + investing + financing
    difference = expected - closing_cash
    return {"expected_closing_cash": expected, "reported_closing_cash": closing_cash, "difference": difference, "balanced": abs(difference) <= tolerance}


def reconcile_balance_sheet(total_assets: float, total_liabilities: float, equity: float, tolerance: float = 0.01) -> dict[str, object]:
    difference = total_assets - (total_liabilities + equity)
    return {"difference": difference, "balanced": abs(difference) <= tolerance}
