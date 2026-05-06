from __future__ import annotations

import pandas as pd

from financial_accounting_engine.utils.math_helpers import safe_divide


def dupont_analysis(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    previous = None
    for r in df.itertuples(index=False):
        npm = safe_divide(r.net_profit, r.revenue, name="net_profit_margin").value
        at = safe_divide(r.revenue, r.total_assets, name="asset_turnover").value
        em = safe_divide(r.total_assets, r.equity, name="equity_multiplier").value
        roe = None if npm is None or at is None or em is None else npm * at * em
        warning = None
        previous_roe: float | None = previous["roe"] if previous else None
        previous_multiplier: float | None = previous["equity_multiplier"] if previous else None
        if (
            previous
            and roe is not None
            and previous_roe is not None
            and previous_multiplier is not None
            and roe > previous_roe
            and em is not None
            and em > previous_multiplier
        ):
            warning = "ROE improved while equity multiplier rose; improvement may be leverage-driven."
        effect = _effect(npm, at, em)
        rows.append({"period": str(r.period), "net_profit_margin": npm, "asset_turnover": at, "equity_multiplier": em, "ROE": roe, "interpretation": effect, "warning": warning})
        previous = {"roe": roe, "equity_multiplier": em}
    return pd.DataFrame(rows)


def _effect(npm, at, em) -> str:
    vals = {"profitability effect": npm or 0, "efficiency effect": at or 0, "leverage effect": em or 0}
    strongest = max(vals, key=lambda key: vals[key])
    return f"ROE is most influenced by the {strongest}; review profitability, asset efficiency, and leverage together."
