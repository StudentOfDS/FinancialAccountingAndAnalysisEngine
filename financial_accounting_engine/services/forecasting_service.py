from __future__ import annotations

import numpy as np
import pandas as pd

from financial_accounting_engine.forecasting.forecast_explainer import explain_forecast
from financial_accounting_engine.forecasting.forecasting_dataset import prepare_forecasting_dataset
from financial_accounting_engine.forecasting.model_selection import select_model
from financial_accounting_engine.forecasting.prediction_intervals import residual_interval
from financial_accounting_engine.validation.forecast_validation import forecast_data_warning

FORECAST_METRICS = ["revenue", "COGS", "gross_profit", "operating_expenses", "operating_profit", "net_profit", "operating_cash_flow", "current_ratio", "quick_ratio", "debt_equity", "ROA", "ROE"]


class ForecastingService:
    def forecast(self, statements: pd.DataFrame, periods: int = 1) -> pd.DataFrame:
        df = prepare_forecasting_dataset(statements)
        warning = forecast_data_warning(df)
        rows = []
        derived = _with_derived_metrics(df)
        for metric in [m for m in FORECAST_METRICS if m in derived.columns]:
            series = _usable_series(derived[metric])
            if series.empty:
                rows.append(_skipped_forecast_row(metric, warning))
                continue
            model, forecast_values, accuracy = select_model(series, periods)
            interval = residual_interval(series, forecast_values)
            for i, point in enumerate(interval, start=1):
                rows.append({"metric": metric, "period": f"T+{i}", "model": model, "accuracy": accuracy, "warning": warning, "explanation": explain_forecast(metric, model, warning), **point})
        return pd.DataFrame(rows)


def _with_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    current_liabilities = out["current_liabilities"].replace(0, pd.NA)
    inventory = out["inventory"] if "inventory" in out.columns else pd.Series(0.0, index=out.index)
    prepaid_expenses = out["prepaid_expenses"] if "prepaid_expenses" in out.columns else pd.Series(0.0, index=out.index)
    quick_assets = out["current_assets"] - inventory.fillna(0.0) - prepaid_expenses.fillna(0.0)
    out["current_ratio"] = out["current_assets"] / current_liabilities
    out["quick_ratio"] = quick_assets / current_liabilities
    out["debt_equity"] = out["total_liabilities"] / out["equity"].replace(0, pd.NA)
    out["ROA"] = out["net_profit"] / out["total_assets"].replace(0, pd.NA)
    out["ROE"] = out["net_profit"] / out["equity"].replace(0, pd.NA)
    return out


def _usable_series(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    return numeric.astype(float)


def _skipped_forecast_row(metric: str, data_warning: str | None) -> dict[str, object]:
    warning = f"Skipped {metric}: no usable historical observations after removing missing, infinite, or invalid values."
    if data_warning:
        warning = f"{warning} {data_warning}"
    return {
        "metric": metric,
        "period": "skipped",
        "model": "not_forecastable",
        "accuracy": {},
        "warning": warning,
        "explanation": "Forecast skipped because the metric has no usable historical observations; no estimate is produced.",
        "expected": None,
        "lower": None,
        "upper": None,
    }
