from __future__ import annotations

import numpy as np
import pandas as pd


def metrics(actual: pd.Series, predicted: pd.Series) -> dict[str, float | None]:
    a = pd.Series(actual, dtype=float).reset_index(drop=True)
    p = pd.Series(predicted, dtype=float).reset_index(drop=True)
    if len(a) == 0:
        return {"MAE": None, "RMSE": None, "MAPE": None, "SMAPE": None, "directional_accuracy": None, "forecast_bias": None}
    err = p - a
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err**2)))
    mape = float(np.mean(np.abs(err / a.replace(0, np.nan))) * 100) if a.replace(0, np.nan).notna().any() else None
    smape = float(np.mean(2 * np.abs(err) / (np.abs(a) + np.abs(p)).replace(0, np.nan)) * 100)
    da = None if len(a) < 2 else float((np.sign(a.diff().dropna()) == np.sign(p.diff().dropna())).mean())
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape, "SMAPE": smape, "directional_accuracy": da, "forecast_bias": float(err.mean())}


def time_based_backtest(series: pd.Series, predictor) -> dict[str, float | None]:
    if len(series) < 4:
        return metrics(pd.Series(dtype=float), pd.Series(dtype=float))
    split = max(2, int(len(series) * 0.75))
    train, test = series.iloc[:split], series.iloc[split:]
    preds = predictor(train, len(test))
    return metrics(test, pd.Series(preds))
