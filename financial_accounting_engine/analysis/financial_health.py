from __future__ import annotations

import pandas as pd

from financial_accounting_engine.analysis.ratios import calculate_ratios


def health_score(df: pd.DataFrame) -> dict[str, object]:
    latest = df.tail(1)
    ratios = calculate_ratios(latest)
    lookup = {r.ratio_name: r.value for r in ratios.itertuples(index=False)}
    components = {
        "liquidity_strength": _score_high(lookup.get("current_ratio"), 2),
        "profitability_strength": _score_high(lookup.get("net_profit_ratio"), 0.15),
        "leverage_risk": _score_low(lookup.get("debt_equity"), 1),
        "cash_flow_quality": 100 if float(latest.iloc[0].operating_cash_flow) >= float(latest.iloc[0].net_profit) else 45,
        "efficiency": _score_high(lookup.get("asset_turnover"), 1),
        "growth_consistency": _growth_score(df),
    }
    score = round(sum(components.values()) / len(components), 2)
    band = "strong" if score >= 80 else "moderate" if score >= 60 else "weak" if score >= 40 else "high risk"
    return {"score": score, "band": band, "components": components, "explanation": f"Overall financial health is {band}; score blends liquidity, profitability, leverage, cash-flow quality, efficiency, and growth consistency."}


def _score_high(value, target):
    if value is None:
        return 35
    return max(0, min(100, (float(value) / target) * 100))


def _score_low(value, target):
    if value is None:
        return 35
    return max(0, min(100, (target / max(float(value), 0.01)) * 100))


def _growth_score(df: pd.DataFrame) -> float:
    if len(df) < 2:
        return 50
    growth = df["revenue"].pct_change().dropna()
    return 80 if (growth >= 0).mean() >= 0.75 else 50 if (growth >= 0).mean() >= 0.5 else 25
