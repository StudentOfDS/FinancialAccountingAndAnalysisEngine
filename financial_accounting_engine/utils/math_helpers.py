from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SafeMetric:
    name: str
    value: float | None
    interpretation: str
    warning: str | None = None


def safe_divide(numerator: float, denominator: float, *, name: str = "ratio") -> SafeMetric:
    if denominator is None or float(denominator) == 0 or math.isnan(float(denominator)):
        return SafeMetric(name, None, "Not meaningful because the denominator is zero or invalid.", "zero_or_invalid_denominator")
    value = float(numerator) / float(denominator)
    return SafeMetric(name, value, _interpret(name, value))


def pct(value: float | None) -> float | None:
    return None if value is None else value * 100


def _interpret(name: str, value: float) -> str:
    lname = name.lower()
    if "current" in lname:
        return "Strong short-term liquidity." if value >= 2 else "Adequate liquidity." if value >= 1 else "Weak liquidity; current liabilities exceed current assets."
    if "quick" in lname:
        return "Liquid assets cover current liabilities." if value >= 1 else "Liquid asset coverage is weak."
    if "debt_equity" in lname or "debt-equity" in lname:
        return "Leverage appears conservative." if value <= 1 else "Leverage is elevated; monitor repayment capacity."
    if "coverage" in lname:
        return "Interest is comfortably covered." if value >= 3 else "Interest coverage is thin."
    if "margin" in lname or "roa" in lname or "roe" in lname:
        return "Positive profitability contribution." if value > 0 else "Profitability is negative or absent."
    return "Computed with safeguards against invalid denominators."
