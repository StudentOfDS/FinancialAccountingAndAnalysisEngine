from __future__ import annotations

import pandas as pd


def prepare_forecasting_dataset(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy().sort_values("period")
    out = out.drop_duplicates("period", keep="last")
    numeric = out.select_dtypes(include="number").columns
    out[numeric] = out[numeric].interpolate(limit_direction="both")
    return out
