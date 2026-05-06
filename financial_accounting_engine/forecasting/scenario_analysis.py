from __future__ import annotations

import pandas as pd

from financial_accounting_engine.models.pro_forma_model import (
    ProFormaAssumptions,
    ScenarioAssumptions,
    ScenarioResult,
)
from financial_accounting_engine.statements.pro_forma import build_projected_statements


def scenario_assumptions(history_growth: float = 0.05, margin: float = 0.2) -> dict[str, dict[str, float | str]]:
    return {
        "base": {"revenue_growth": history_growth, "margin_change": 0.0, "expense_ratio_change": 0.0, "description": "Historical average growth/margins/debt/working capital."},
        "optimistic": {"revenue_growth": history_growth + 0.05, "margin_change": 0.02, "expense_ratio_change": -0.02, "description": "Higher growth, better margin and collections, lower debt pressure."},
        "pessimistic": {"revenue_growth": history_growth - 0.05, "margin_change": -0.03, "expense_ratio_change": 0.03, "description": "Lower growth, higher expenses, blocked working capital, weaker OCF."},
        "stress": {"revenue_growth": -0.15, "margin_change": -0.07, "expense_ratio_change": 0.05, "description": "Revenue decline, margin compression, weak OCF, debt and liquidity pressure."},
    }


def default_scenario_assumptions(latest: pd.Series, forecast_periods: int = 1) -> list[ScenarioAssumptions]:
    base = _base_assumptions(latest, forecast_periods)
    return [
        ScenarioAssumptions("base", base, "Base case uses recent revenue growth, margins, working-capital days, debt and cash levels."),
        ScenarioAssumptions("optimistic", _adjust(base, revenue_growth_delta=0.05, cogs_delta=-0.02, opex_delta=-0.02, receivables_days_delta=-5, debt_change_delta=-1000), "Optimistic case assumes stronger growth, better margins, faster collections and lower debt pressure."),
        ScenarioAssumptions("pessimistic", _adjust(base, revenue_growth_delta=-0.05, cogs_delta=0.03, opex_delta=0.03, receivables_days_delta=10, debt_change_delta=1000), "Pessimistic case assumes lower growth, cost pressure, slower collections and higher debt pressure."),
        ScenarioAssumptions("stress", _adjust(base, revenue_growth_delta=-0.20, cogs_delta=0.07, opex_delta=0.05, receivables_days_delta=20, capex_delta=-base.capex, debt_change_delta=2500, auto_balance=False), "Stress case models revenue decline, margin compression, working-capital pressure and liquidity strain."),
    ]


def run_scenarios(latest: pd.Series, scenarios: list[ScenarioAssumptions] | None = None, forecast_periods: int = 1) -> dict[str, ScenarioResult]:
    selected = scenarios or default_scenario_assumptions(latest, forecast_periods)
    return {
        scenario.name: ScenarioResult(
            name=scenario.name,
            pro_forma=build_projected_statements(latest, scenario.assumptions),
            explanation=scenario.explanation,
        )
        for scenario in selected
    }


def _base_assumptions(latest: pd.Series, forecast_periods: int) -> ProFormaAssumptions:
    revenue = float(latest.revenue)
    return ProFormaAssumptions(
        revenue_growth_rate=_latest_growth(latest),
        cogs_percentage_of_revenue=_safe_ratio(float(latest.COGS), revenue),
        operating_expense_percentage_of_revenue=_safe_ratio(float(latest.operating_expenses), revenue),
        depreciation_percentage_of_assets=0.05,
        interest_expense=float(latest.interest_expense),
        tax_rate=_safe_ratio(float(latest.tax_expense), max(float(latest.operating_profit) - float(latest.interest_expense), 0.0)),
        receivables_days=_days(getattr(latest, "receivables", 0.0), revenue),
        inventory_days=_days(getattr(latest, "inventory", 0.0), float(latest.COGS)),
        payables_days=_days(getattr(latest, "payables", 0.0), float(latest.COGS)),
        capex=max(abs(float(latest.investing_cash_flow)), 0.0),
        debt_change=0.0,
        dividend_or_drawings=0.0,
        opening_cash=float(latest.closing_cash),
        forecast_periods=forecast_periods,
        auto_balance=True,
    )


def _adjust(
    assumptions: ProFormaAssumptions,
    *,
    revenue_growth_delta: float = 0.0,
    cogs_delta: float = 0.0,
    opex_delta: float = 0.0,
    receivables_days_delta: float = 0.0,
    capex_delta: float = 0.0,
    debt_change_delta: float = 0.0,
    auto_balance: bool | None = None,
) -> ProFormaAssumptions:
    return ProFormaAssumptions(
        revenue_growth_rate=assumptions.revenue_growth_rate + revenue_growth_delta,
        cogs_percentage_of_revenue=max(0.0, assumptions.cogs_percentage_of_revenue + cogs_delta),
        operating_expense_percentage_of_revenue=max(0.0, assumptions.operating_expense_percentage_of_revenue + opex_delta),
        depreciation_amount=assumptions.depreciation_amount,
        depreciation_percentage_of_assets=assumptions.depreciation_percentage_of_assets,
        interest_expense=assumptions.interest_expense,
        tax_rate=assumptions.tax_rate,
        receivables_days=max(0.0, assumptions.receivables_days + receivables_days_delta),
        inventory_days=assumptions.inventory_days,
        payables_days=assumptions.payables_days,
        capex=max(0.0, assumptions.capex + capex_delta),
        debt_change=assumptions.debt_change + debt_change_delta,
        dividend_or_drawings=assumptions.dividend_or_drawings,
        opening_cash=assumptions.opening_cash,
        forecast_periods=assumptions.forecast_periods,
        auto_balance=assumptions.auto_balance if auto_balance is None else auto_balance,
    )


def _latest_growth(latest: pd.Series) -> float:
    return float(getattr(latest, "revenue_growth_rate", 0.05))


def _days(balance: float, flow: float) -> float:
    return 0.0 if flow == 0 else float(balance) / flow * 365.0


def _safe_ratio(numerator: float, denominator: float) -> float:
    return 0.0 if denominator == 0 else numerator / denominator
