from __future__ import annotations

import pandas as pd


def forecast_data_warning(df: pd.DataFrame) -> str | None:
    n = len(df)
    if n < 3:
        return "Fewer than 3 observations: forecasting is not reliable; use only descriptive scenarios."
    if n <= 5:
        return "3-5 annual observations: basic/weak forecasts only."
    if n <= 10:
        return "5-10 observations: trend forecasts are usable but should be stress-tested."
    return None
