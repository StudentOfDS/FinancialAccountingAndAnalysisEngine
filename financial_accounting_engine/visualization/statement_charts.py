from __future__ import annotations

import pandas as pd
import plotly.express as px


def trend_chart(df: pd.DataFrame, metrics: list[str]):
    """Business question: how are core statement line items trending over time?"""
    long = df.melt(id_vars="period", value_vars=[m for m in metrics if m in df.columns], var_name="metric", value_name="value")
    return px.line(long, x="period", y="value", color="metric", markers=True, title="Statement trend: revenue, profit, assets, liabilities, equity and cash flow")
