from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def cash_flow_waterfall(row: pd.Series):
    """Business question: which activities explain the cash movement?"""
    return go.Figure(go.Waterfall(x=["Opening", "Operating", "Investing", "Financing", "Closing"], measure=["absolute", "relative", "relative", "relative", "total"], y=[row.opening_cash, row.operating_cash_flow, row.investing_cash_flow, row.financing_cash_flow, row.closing_cash])).update_layout(title="Cash-flow waterfall")
