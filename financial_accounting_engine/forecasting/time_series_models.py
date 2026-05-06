from __future__ import annotations

import pandas as pd
from statsmodels.tsa.holtwinters import Holt, SimpleExpSmoothing

from financial_accounting_engine.forecasting.baseline_models import naive_forecast


def exponential_smoothing_forecast(series: pd.Series, periods: int) -> list[float]:
    s = series.dropna().astype(float)
    if len(s) < 4:
        return naive_forecast(s, periods)
    try:
        if len(s) >= 8:
            model = Holt(s, initialization_method="estimated").fit(optimized=True)
        else:
            model = SimpleExpSmoothing(s, initialization_method="estimated").fit(optimized=True)
        return [float(x) for x in model.forecast(periods)]
    except Exception:
        return naive_forecast(s, periods)
