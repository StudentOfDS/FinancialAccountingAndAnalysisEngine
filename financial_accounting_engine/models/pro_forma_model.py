from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass(frozen=True)
class ProFormaAssumptions:
    revenue_growth_rate: float
    cogs_percentage_of_revenue: float
    operating_expense_percentage_of_revenue: float
    depreciation_amount: float | None = None
    depreciation_percentage_of_assets: float = 0.0
    interest_expense: float = 0.0
    tax_rate: float = 0.0
    receivables_days: float = 30.0
    inventory_days: float = 30.0
    payables_days: float = 30.0
    capex: float = 0.0
    debt_change: float = 0.0
    dividend_or_drawings: float = 0.0
    opening_cash: float | None = None
    forecast_periods: int = 1
    auto_balance: bool = True


@dataclass(frozen=True)
class ScenarioAssumptions:
    name: str
    assumptions: ProFormaAssumptions
    explanation: str


@dataclass(frozen=True)
class ProFormaResult:
    income_statement: pd.DataFrame
    balance_sheet: pd.DataFrame
    cash_flow_statement: pd.DataFrame
    ratios: pd.DataFrame
    reconciliation: dict[str, object]
    risk_warnings: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    pro_forma: ProFormaResult
    explanation: str
