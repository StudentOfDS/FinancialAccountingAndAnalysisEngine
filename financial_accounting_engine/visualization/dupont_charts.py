from __future__ import annotations

import pandas as pd
import plotly.express as px


def dupont_component_chart(dupont: pd.DataFrame):
    """Business question: is ROE driven by profitability, efficiency, or leverage?"""
    long = dupont.melt(id_vars="period", value_vars=["net_profit_margin", "asset_turnover", "equity_multiplier", "ROE"], var_name="component", value_name="value")
    return px.bar(long, x="period", y="value", color="component", barmode="group", title="DuPont decomposition")
