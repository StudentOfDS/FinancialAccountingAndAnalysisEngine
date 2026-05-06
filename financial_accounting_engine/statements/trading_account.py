from __future__ import annotations


def build_trading_account(opening_stock=0.0, purchases=0.0, purchase_returns=0.0, direct_expenses=0.0, sales=0.0, sales_returns=0.0, closing_stock=0.0) -> dict[str, float]:
    net_purchases = purchases - purchase_returns
    net_sales = sales - sales_returns
    cogs = opening_stock + net_purchases + direct_expenses - closing_stock
    gross_profit = net_sales - cogs
    return {"opening_stock": opening_stock, "net_purchases": net_purchases, "direct_expenses": direct_expenses, "net_sales": net_sales, "closing_stock": closing_stock, "COGS": cogs, "gross_profit": gross_profit}
