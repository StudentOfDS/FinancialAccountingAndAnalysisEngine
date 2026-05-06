from __future__ import annotations

import pandas as pd
import plotly.express as px


def common_size_heatmap(common_size: pd.DataFrame):
    """Business question: how does statement composition shift across periods?"""
    value_cols = [c for c in common_size.columns if c.endswith("_pct_of_revenue") or c.endswith("_pct_of_assets")]
    long = common_size.melt(id_vars="period", value_vars=value_cols, var_name="line_item", value_name="percent")
    return px.imshow(long.pivot(index="line_item", columns="period", values="percent"), aspect="auto", title="Common-size / vertical analysis heatmap")
