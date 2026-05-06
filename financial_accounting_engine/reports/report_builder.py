from __future__ import annotations

import pandas as pd

from financial_accounting_engine.analysis.stakeholder_report import build_stakeholder_report


def build_report_payload(statements: pd.DataFrame) -> dict[str, object]:
    return build_stakeholder_report(statements)
