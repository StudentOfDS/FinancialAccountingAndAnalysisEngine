from __future__ import annotations

import numpy as np
import pandas as pd


def naive_forecast(series: pd.Series, periods: int) -> list[float]:
    return [float(series.dropna().iloc[-1])] * periods


def moving_average_forecast(series: pd.Series, periods: int, window: int = 3) -> list[float]:
    value = float(series.dropna().tail(window).mean())
    return [value] * periods


def weighted_moving_average_forecast(series: pd.Series, periods: int) -> list[float]:
    s = series.dropna().tail(3).astype(float)
    weights = np.arange(1, len(s) + 1)
    value = float(np.average(s, weights=weights))
    return [value] * periods


def cagr_forecast(series: pd.Series, periods: int) -> list[float]:
    s = series.dropna().astype(float)
    if len(s) < 2 or s.iloc[0] <= 0:
        return naive_forecast(series, periods)
    rate = (s.iloc[-1] / s.iloc[0]) ** (1 / (len(s) - 1)) - 1
    return [float(s.iloc[-1] * ((1 + rate) ** i)) for i in range(1, periods + 1)]
