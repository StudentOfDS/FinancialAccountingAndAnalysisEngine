from __future__ import annotations

import pandas as pd
import plotly.express as px


def ratio_chart(ratios: pd.DataFrame):
    """Business question: which financial strengths or risks are improving or worsening?"""
    return px.line(ratios.dropna(subset=["value"]), x="period", y="value", color="ratio_name", markers=True, title="Ratio trends")
