from __future__ import annotations

import pandas as pd


def residual_interval(history: pd.Series, expected: list[float], width: float = 1.96) -> list[dict[str, float]]:
    s = history.dropna().astype(float)
    residuals = s.diff().dropna()
    sigma = float(residuals.std()) if len(residuals) > 1 else max(abs(float(s.iloc[-1])) * 0.1, 1.0)
    return [{"expected": float(v), "lower": float(v - width * sigma), "upper": float(v + width * sigma)} for v in expected]
