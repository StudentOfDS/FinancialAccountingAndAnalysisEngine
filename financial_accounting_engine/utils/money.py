def format_money(value: float, currency: str = "USD") -> str:
    return f"{currency} {value:,.2f}"
