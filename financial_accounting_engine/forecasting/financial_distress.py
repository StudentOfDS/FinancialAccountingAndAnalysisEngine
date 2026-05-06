from __future__ import annotations

import pandas as pd

from financial_accounting_engine.analysis.financial_health import health_score


def distress_score(df: pd.DataFrame) -> dict[str, object]:
    health = health_score(df)
    raw_score = health.get("score", 0.0)
    health_value = float(raw_score) if isinstance(raw_score, int | float | str) else 0.0
    score = max(0.0, 100.0 - health_value)
    risk = "low" if score < 20 else "moderate" if score < 40 else "elevated" if score < 60 else "high"
    return {
        "distress_score": round(score, 2),
        "risk_band": risk,
        "method": "interpretable_rule_based",
        "explanation": "Rule-based distress score derived from liquidity, profitability, leverage, OCF quality, efficiency, and growth. Altman/logistic ML is not used without suitability or labeled distress data.",
    }
