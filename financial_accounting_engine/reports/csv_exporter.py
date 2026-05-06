from __future__ import annotations

import pandas as pd


def export_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)
