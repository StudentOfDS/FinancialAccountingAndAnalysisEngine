from __future__ import annotations

import pandas as pd

from financial_accounting_engine.utils.exceptions import ValidationError
from financial_accounting_engine.validation.schema_validation import (
    ASSET_COLUMNS,
    validate_required_columns,
)


def depreciation_schedule(assets: pd.DataFrame, periods: int = 1) -> pd.DataFrame:
    validate_required_columns(assets, ASSET_COLUMNS, "assets")
    if periods < 0:
        raise ValidationError("Depreciation periods cannot be negative.")

    rows = []
    for row in assets.itertuples(index=False):
        cost = float(row.purchase_cost)
        salvage = float(row.salvage_value)
        life = float(row.useful_life or 0)
        method = str(row.depreciation_method or "").lower().replace("-", "_")
        depreciation, method_used = _depreciation_for_method(
            cost=cost,
            salvage=salvage,
            useful_life=life,
            method=method,
            depreciation_rate=float(row.depreciation_rate or 0),
            periods=periods,
        )
        rows.append({
            "asset_id": row.asset_id,
            "asset_name": row.asset_name,
            "opening_book_value": cost,
            "depreciation_for_period": depreciation,
            "accumulated_depreciation": depreciation,
            "closing_book_value": cost - depreciation,
            "method_used": method_used,
        })
    return pd.DataFrame(rows)


def _depreciation_for_method(
    *,
    cost: float,
    salvage: float,
    useful_life: float,
    method: str,
    depreciation_rate: float,
    periods: int,
) -> tuple[float, str]:
    if method in {"straight_line", "slm"}:
        if useful_life <= 0:
            raise ValidationError("Straight-line depreciation requires useful_life greater than zero.")
        annual_depreciation = max((cost - salvage) / useful_life, 0.0)
        depreciation = annual_depreciation * periods
        return min(depreciation, max(cost - salvage, 0.0)), "straight_line"

    if method in {"written_down_value", "wdv"}:
        if depreciation_rate < 0:
            raise ValidationError("WDV depreciation_rate cannot be negative.")
        book_value = cost
        accumulated = 0.0
        for _ in range(periods):
            period_depreciation = book_value * depreciation_rate
            period_depreciation = min(period_depreciation, max(book_value - salvage, 0.0))
            accumulated += period_depreciation
            book_value -= period_depreciation
        return accumulated, "written_down_value"

    raise ValidationError(f"Unsupported depreciation method: {method or 'blank'}")
