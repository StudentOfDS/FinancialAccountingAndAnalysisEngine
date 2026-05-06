from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_tabular_file(path_or_buffer, *, sheet_name: str | int | None = 0) -> pd.DataFrame:
    name = getattr(path_or_buffer, "name", str(path_or_buffer))
    suffix = Path(name).suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path_or_buffer, sheet_name=sheet_name)
    return pd.read_csv(path_or_buffer)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().replace(" ", "_") for c in out.columns]
    return out
