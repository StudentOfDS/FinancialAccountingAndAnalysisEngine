from __future__ import annotations

import pandas as pd

from financial_accounting_engine.forecasting.backtesting import time_based_backtest
from financial_accounting_engine.forecasting.baseline_models import (
    cagr_forecast,
    moving_average_forecast,
    naive_forecast,
    weighted_moving_average_forecast,
)
from financial_accounting_engine.forecasting.time_series_models import (
    exponential_smoothing_forecast,
)

CANDIDATES = {"naive": naive_forecast, "moving_average": moving_average_forecast, "weighted_moving_average": weighted_moving_average_forecast, "CAGR": cagr_forecast, "exponential_smoothing": exponential_smoothing_forecast}


def select_model(series: pd.Series, periods: int = 1) -> tuple[str, list[float], dict[str, float | None]]:
    best_name = "naive"
    best_metrics: dict[str, float | None] = {"MAE": float("inf")}
    best_fn = naive_forecast
    for name, fn in CANDIDATES.items():
        m = time_based_backtest(series, fn)
        score = m["MAE"] if m["MAE"] is not None else float("inf")
        if score < (best_metrics["MAE"] if best_metrics["MAE"] is not None else float("inf")):
            best_name, best_metrics, best_fn = name, m, fn
    return best_name, best_fn(series, periods), best_metrics
