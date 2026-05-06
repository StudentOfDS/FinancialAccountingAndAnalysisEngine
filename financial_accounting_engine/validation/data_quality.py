from __future__ import annotations

import pandas as pd


def data_quality_report(df: pd.DataFrame) -> dict[str, object]:
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
    }
