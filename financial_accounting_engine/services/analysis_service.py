from __future__ import annotations

import pandas as pd

from financial_accounting_engine.analysis.dupont import dupont_analysis
from financial_accounting_engine.analysis.financial_health import health_score
from financial_accounting_engine.analysis.ratios import calculate_ratios
from financial_accounting_engine.analysis.red_flags import detect_red_flags
from financial_accounting_engine.analysis.vertical_analysis import (
    vertical_balance_sheet,
    vertical_income_statement,
)


class AnalysisService:
    def analyze(self, statements: pd.DataFrame) -> dict[str, object]:
        return {"ratios": calculate_ratios(statements), "dupont": dupont_analysis(statements), "vertical_income_statement": vertical_income_statement(statements), "vertical_balance_sheet": vertical_balance_sheet(statements), "health": health_score(statements), "red_flags": detect_red_flags(statements)}
