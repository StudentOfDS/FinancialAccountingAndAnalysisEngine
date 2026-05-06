def explain_forecast(metric: str, model: str, warning: str | None = None) -> str:
    base = f"{metric} forecast uses {model}; change is driven by historical trend, margin/cost behavior, cash-flow quality, and selected scenario assumptions. Predictions are estimates, not guarantees."
    return f"{base} Warning: {warning}" if warning else base
