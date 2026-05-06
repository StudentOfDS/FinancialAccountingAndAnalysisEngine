from __future__ import annotations

import pandas as pd
import plotly.express as px


def red_flag_chart(flags: list[dict[str, str]]):
    """Business question: where are financial red flags concentrated?"""
    df = pd.DataFrame(flags) if flags else pd.DataFrame([{"period": "none", "flag": "No red flags", "count": 0}])
    if "count" not in df:
        df = df.groupby(["period", "flag"]).size().reset_index(name="count")
    return px.bar(df, x="period", y="count", color="flag", title="Red flag dashboard")
