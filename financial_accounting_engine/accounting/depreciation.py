from __future__ import annotations

import pandas as pd

from financial_accounting_engine.validation.schema_validation import (
    ASSET_COLUMNS,
    validate_required_columns,
)


def depreciation_schedule(assets: pd.DataFrame, periods: int = 1) -> pd.DataFrame:
    validate_required_columns(assets, ASSET_COLUMNS, "assets")
    rows = []
    for row in assets.itertuples(index=False):
        cost = float(row.purchase_cost)
        salvage = float(row.salvage_value)
        life = float(row.useful_life or 0)
        method = str(row.depreciation_method or "straight_line").lower().replace("-", "_")
        opening = cost
        if method in {"straight_line", "slm"}:
            dep = max((cost - salvage) / life, 0.0) * periods if life > 0 else 0.0
            method_used = "straight_line"
        elif method in {"written_down_value", "wdv"}:
            dep = opening * float(row.depreciation_rate or 0) * periods
            method_used = "written_down_value"
        else:
            dep = 0.0
            method_used = "unsupported_default_zero"
        dep = min(dep, max(opening - salvage, 0.0))
        rows.append({
            "asset_id": row.asset_id,
            "asset_name": row.asset_name,
            "opening_book_value": opening,
            "depreciation_for_period": dep,
            "accumulated_depreciation": dep,
            "closing_book_value": opening - dep,
            "method_used": method_used,
        })
    return pd.DataFrame(rows)
