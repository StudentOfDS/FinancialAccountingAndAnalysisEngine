from __future__ import annotations

import pandas as pd

from financial_accounting_engine.forecasting.scenario_analysis import run_scenarios
from financial_accounting_engine.models.pro_forma_model import (
    ProFormaAssumptions,
    ScenarioAssumptions,
)
from financial_accounting_engine.statements.pro_forma import build_projected_statements


class ProFormaService:
    def project(self, statements: pd.DataFrame, assumptions: ProFormaAssumptions):
        latest = statements.sort_values("period").tail(1).iloc[0]
        return build_projected_statements(latest, assumptions)

    def scenarios(self, statements: pd.DataFrame, scenarios: list[ScenarioAssumptions] | None = None, forecast_periods: int = 1):
        latest = statements.sort_values("period").tail(1).iloc[0]
        return run_scenarios(latest, scenarios, forecast_periods)
