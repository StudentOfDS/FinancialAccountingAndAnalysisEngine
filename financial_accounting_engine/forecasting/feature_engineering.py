from __future__ import annotations

import pandas as pd


def add_time_series_features(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    out = df.copy()
    out[f"{metric}_lag1"] = out[metric].shift(1)
    out[f"{metric}_growth"] = out[metric].pct_change()
    return out
