from __future__ import annotations

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
            series = derived[metric]
            model, one, accuracy = select_model(series)
            interval = residual_interval(series, [one[0]] * periods)
            for i, point in enumerate(interval, start=1):
                rows.append({"metric": metric, "period": f"T+{i}", "model": model, "accuracy": accuracy, "explanation": explain_forecast(metric, model, warning), **point})
        return pd.DataFrame(rows)

def _with_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["current_ratio"] = out["current_assets"] / out["current_liabilities"].replace(0, pd.NA)
    out["quick_ratio"] = out["current_assets"] / out["current_liabilities"].replace(0, pd.NA)
    out["debt_equity"] = out["total_liabilities"] / out["equity"].replace(0, pd.NA)
    out["ROA"] = out["net_profit"] / out["total_assets"].replace(0, pd.NA)
    out["ROE"] = out["net_profit"] / out["equity"].replace(0, pd.NA)
    return out
