from __future__ import annotations

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge

from financial_accounting_engine.forecasting.baseline_models import naive_forecast

MIN_ML_OBSERVATIONS = 24
MODELS = {
    "linear_regression": LinearRegression,
    "ridge": lambda: Ridge(random_state=42),
    "lasso": lambda: Lasso(random_state=42),
    "elastic_net": lambda: ElasticNet(random_state=42),
    "random_forest": lambda: RandomForestRegressor(n_estimators=100, random_state=42),
    "gradient_boosting": lambda: GradientBoostingRegressor(random_state=42),
}


def ml_forecast_with_safeguard(series: pd.Series, periods: int, model_name: str = "ridge") -> tuple[list[float], str]:
    s = series.dropna().astype(float).reset_index(drop=True)
    if len(s) < MIN_ML_OBSERVATIONS:
        return naive_forecast(s, periods), "ML skipped: insufficient observations; used naive baseline to avoid overfitting."
    X = pd.DataFrame({"t": range(len(s)), "lag1": s.shift(1), "growth": s.pct_change().replace([float("inf"), -float("inf")], 0)}).fillna(0)
    model = MODELS.get(model_name, MODELS["ridge"])()
    model.fit(X, s)
    future = []
    last = float(s.iloc[-1])
    for t in range(len(s), len(s) + periods):
        x = pd.DataFrame([{"t": t, "lag1": last, "growth": 0.0}])
        last = float(model.predict(x)[0])
        future.append(last)
    return future, f"ML model {model_name} used with deterministic seed where applicable."
