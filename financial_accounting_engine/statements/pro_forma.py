from __future__ import annotations

from typing import Any

import pandas as pd

from financial_accounting_engine.analysis.ratios import calculate_ratios
from financial_accounting_engine.models.pro_forma_model import ProFormaAssumptions, ProFormaResult
from financial_accounting_engine.validation.reconciliation import (
    reconcile_balance_sheet,
    reconcile_cash_flow,
)

DAYS_IN_YEAR = 365.0


def build_pro_forma(latest: pd.Series, revenue_growth: float, margin_change: float = 0.0, expense_ratio_change: float = 0.0) -> dict[str, object]:
    """Backward-compatible wrapper around the richer pro forma engine."""
    revenue_base = _safe_ratio(float(latest.gross_profit), float(latest.revenue)) + margin_change
    assumptions = ProFormaAssumptions(
        revenue_growth_rate=revenue_growth,
        cogs_percentage_of_revenue=max(0.0, 1 - revenue_base),
        operating_expense_percentage_of_revenue=_safe_ratio(float(latest.operating_expenses), float(latest.revenue)) + expense_ratio_change,
        interest_expense=float(latest.interest_expense),
        tax_rate=_safe_ratio(float(latest.tax_expense), max(float(latest.operating_profit) - float(latest.interest_expense), 0.0)),
        opening_cash=float(latest.closing_cash),
    )
    result = build_projected_statements(latest, assumptions)
    statements = _combined_statement_frame(result)
    return {"statements": statements, "ratios": result.ratios}


def build_projected_statements(latest: pd.Series, assumptions: ProFormaAssumptions) -> ProFormaResult:
    periods = max(int(assumptions.forecast_periods), 1)
    previous = _latest_state(latest, assumptions)
    income_rows: list[dict[str, Any]] = []
    balance_rows: list[dict[str, Any]] = []
    cash_flow_rows: list[dict[str, Any]] = []
    reconciliation_rows: list[dict[str, Any]] = []

    for period_index in range(1, periods + 1):
        income = _project_income_statement(previous, assumptions, period_index)
        working_capital = _project_working_capital(income, assumptions)
        cash_flow_inputs = _project_cash_flow_inputs(previous, income, working_capital, assumptions)
        balance_sheet, cash_flow, reconciliation = _project_balance_sheet_and_cash_flow(
            previous=previous,
            income=income,
            working_capital=working_capital,
            cash_flow_inputs=cash_flow_inputs,
            assumptions=assumptions,
        )
        income_rows.append(income)
        balance_rows.append(balance_sheet)
        cash_flow_rows.append(cash_flow)
        reconciliation_rows.append(reconciliation)
        previous = {**previous, **income, **balance_sheet, **cash_flow}

    income_statement = pd.DataFrame(income_rows)
    balance_sheet = pd.DataFrame(balance_rows)
    cash_flow_statement = pd.DataFrame(cash_flow_rows)
    statement_frame = _statement_frame_for_ratios(income_statement, balance_sheet, cash_flow_statement)
    ratios = calculate_ratios(statement_frame)
    risk_warnings = scenario_risk_warnings(statement_frame, ratios, reconciliation_rows)
    return ProFormaResult(
        income_statement=income_statement,
        balance_sheet=balance_sheet,
        cash_flow_statement=cash_flow_statement,
        ratios=ratios,
        reconciliation={"periods": reconciliation_rows, "all_balanced": all(bool(row["balance_sheet"]["balanced"] and row["cash_flow"]["balanced"]) for row in reconciliation_rows)},
        risk_warnings=risk_warnings,
    )


def scenario_risk_warnings(statement_frame: pd.DataFrame, ratios: pd.DataFrame, reconciliation_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    ratio_pivot = ratios.pivot(index="period", columns="ratio_name", values="value") if not ratios.empty else pd.DataFrame()
    previous_net_margin: float | None = None
    for row in statement_frame.itertuples(index=False):
        period = str(row.period)
        if float(row.closing_cash) < 0:
            warnings.append(_risk(period, "negative_closing_cash", "Projected closing cash is negative."))
        if float(row.current_assets) - float(row.current_liabilities) < 0:
            warnings.append(_risk(period, "negative_working_capital", "Projected current liabilities exceed current assets."))
        net_margin = _safe_ratio(float(row.net_profit), float(row.revenue))
        if previous_net_margin is not None and net_margin < previous_net_margin:
            warnings.append(_risk(period, "declining_net_margin", "Projected net margin declined from the prior projected period."))
        previous_net_margin = net_margin
        if float(row.operating_cash_flow) < float(row.net_profit):
            warnings.append(_risk(period, "ocf_below_net_profit", "Projected operating cash flow is below net profit."))
        if period in ratio_pivot.index:
            values = ratio_pivot.loc[period]
            debt_equity = values.get("debt_equity")
            interest_coverage = values.get("interest_coverage")
            if debt_equity is not None and debt_equity > 2:
                warnings.append(_risk(period, "high_debt_equity", "Projected debt-equity ratio is above the safe threshold of 2.0."))
            if interest_coverage is not None and interest_coverage < 2:
                warnings.append(_risk(period, "low_interest_coverage", "Projected interest coverage is below the safe threshold of 2.0."))
    for reconciliation in reconciliation_rows:
        period = str(reconciliation["period"])
        balance_sheet = reconciliation["balance_sheet"]
        cash_flow = reconciliation["cash_flow"]
        if isinstance(balance_sheet, dict) and not balance_sheet["balanced"]:
            warnings.append(_risk(period, "balance_sheet_mismatch", "Projected assets do not equal liabilities plus equity."))
        if isinstance(cash_flow, dict) and not cash_flow["balanced"]:
            warnings.append(_risk(period, "cash_flow_mismatch", "Projected cash flow does not reconcile to closing cash."))
    return warnings


def _project_income_statement(previous: dict[str, Any], assumptions: ProFormaAssumptions, period_index: int) -> dict[str, Any]:
    revenue = previous["revenue"] * (1 + assumptions.revenue_growth_rate)
    cogs = revenue * assumptions.cogs_percentage_of_revenue
    gross_profit = revenue - cogs
    operating_expenses = revenue * assumptions.operating_expense_percentage_of_revenue
    depreciation = _depreciation(previous, assumptions)
    operating_profit = gross_profit - operating_expenses - depreciation
    profit_before_tax = operating_profit - assumptions.interest_expense
    tax_expense = max(profit_before_tax, 0.0) * assumptions.tax_rate
    net_profit = profit_before_tax - tax_expense
    return {
        "period": f"T+{period_index}",
        "revenue": revenue,
        "COGS": cogs,
        "gross_profit": gross_profit,
        "operating_expenses": operating_expenses,
        "depreciation": depreciation,
        "operating_profit": operating_profit,
        "interest_expense": assumptions.interest_expense,
        "tax_expense": tax_expense,
        "net_profit": net_profit,
    }


def _project_working_capital(income: dict[str, Any], assumptions: ProFormaAssumptions) -> dict[str, float]:
    revenue = float(income["revenue"])
    cogs = float(income["COGS"])
    return {
        "receivables": revenue * assumptions.receivables_days / DAYS_IN_YEAR,
        "inventory": cogs * assumptions.inventory_days / DAYS_IN_YEAR,
        "payables": cogs * assumptions.payables_days / DAYS_IN_YEAR,
    }


def _project_cash_flow_inputs(previous: dict[str, Any], income: dict[str, Any], working_capital: dict[str, float], assumptions: ProFormaAssumptions) -> dict[str, float]:
    change_receivables = working_capital["receivables"] - previous["receivables"]
    change_inventory = working_capital["inventory"] - previous["inventory"]
    change_payables = working_capital["payables"] - previous["payables"]
    operating_cash_flow = float(income["net_profit"]) + float(income["depreciation"]) - change_receivables - change_inventory + change_payables
    investing_cash_flow = -assumptions.capex
    financing_cash_flow = assumptions.debt_change - assumptions.dividend_or_drawings
    closing_cash = previous["closing_cash"] + operating_cash_flow + investing_cash_flow + financing_cash_flow
    return {
        "operating_cash_flow": operating_cash_flow,
        "investing_cash_flow": investing_cash_flow,
        "financing_cash_flow": financing_cash_flow,
        "closing_cash": closing_cash,
    }


def _project_balance_sheet_and_cash_flow(
    *,
    previous: dict[str, Any],
    income: dict[str, Any],
    working_capital: dict[str, float],
    cash_flow_inputs: dict[str, float],
    assumptions: ProFormaAssumptions,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    fixed_assets = max(previous["non_current_assets"] + assumptions.capex - float(income["depreciation"]), 0.0)
    debt = max(previous["non_current_liabilities"] + assumptions.debt_change, 0.0)
    equity = previous["equity"] + float(income["net_profit"]) - assumptions.dividend_or_drawings
    closing_cash = cash_flow_inputs["closing_cash"]
    current_assets_without_cash = working_capital["receivables"] + working_capital["inventory"]
    current_liabilities = working_capital["payables"]
    total_assets = closing_cash + current_assets_without_cash + fixed_assets
    total_liabilities = current_liabilities + debt
    balancing_difference = total_assets - (total_liabilities + equity)
    balancing_asset_plug = 0.0
    balancing_liability_plug = 0.0
    if assumptions.auto_balance and abs(balancing_difference) > 0.01:
        if balancing_difference > 0:
            balancing_liability_plug = balancing_difference
        else:
            balancing_asset_plug = abs(balancing_difference)
        total_assets += balancing_asset_plug
        total_liabilities += balancing_liability_plug
        balancing_difference = total_assets - (total_liabilities + equity)
    current_assets = closing_cash + current_assets_without_cash + balancing_asset_plug
    balance_reconciliation = reconcile_balance_sheet(total_assets, total_liabilities, equity)
    cash_reconciliation = reconcile_cash_flow(previous["closing_cash"], cash_flow_inputs["operating_cash_flow"], cash_flow_inputs["investing_cash_flow"], cash_flow_inputs["financing_cash_flow"], closing_cash)
    balance_difference = _object_to_float(balance_reconciliation["difference"])
    cash_difference = _object_to_float(cash_reconciliation["difference"])
    balance_sheet = {
        "period": str(income["period"]),
        "cash": closing_cash,
        "receivables": working_capital["receivables"],
        "inventory": working_capital["inventory"],
        "current_assets": current_assets,
        "fixed_assets": fixed_assets,
        "non_current_assets": fixed_assets,
        "total_assets": total_assets,
        "balancing_asset_plug": balancing_asset_plug,
        "payables": current_liabilities,
        "current_liabilities": current_liabilities,
        "debt": debt,
        "non_current_liabilities": debt,
        "total_liabilities": total_liabilities,
        "balancing_liability_plug": balancing_liability_plug,
        "equity": equity,
        "balanced": bool(balance_reconciliation["balanced"]),
        "balancing_difference": balance_difference,
    }
    cash_flow = {
        "period": str(income["period"]),
        "opening_cash": previous["closing_cash"],
        "operating_cash_flow": cash_flow_inputs["operating_cash_flow"],
        "investing_cash_flow": cash_flow_inputs["investing_cash_flow"],
        "financing_cash_flow": cash_flow_inputs["financing_cash_flow"],
        "net_change_in_cash": cash_flow_inputs["operating_cash_flow"] + cash_flow_inputs["investing_cash_flow"] + cash_flow_inputs["financing_cash_flow"],
        "closing_cash": closing_cash,
        "balanced": bool(cash_reconciliation["balanced"]),
        "cash_flow_difference": cash_difference,
    }
    return balance_sheet, cash_flow, {"period": str(income["period"]), "balance_sheet": balance_reconciliation, "cash_flow": cash_reconciliation}


def _latest_state(latest: pd.Series, assumptions: ProFormaAssumptions) -> dict[str, Any]:
    return {
        "revenue": float(latest.revenue),
        "closing_cash": float(assumptions.opening_cash if assumptions.opening_cash is not None else latest.closing_cash),
        "receivables": float(getattr(latest, "receivables", 0.0)),
        "inventory": float(getattr(latest, "inventory", 0.0)),
        "payables": float(getattr(latest, "payables", 0.0)),
        "non_current_assets": float(latest.non_current_assets),
        "non_current_liabilities": float(latest.non_current_liabilities),
        "equity": float(latest.equity),
    }


def _statement_frame_for_ratios(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame, cash_flow_statement: pd.DataFrame) -> pd.DataFrame:
    return income_statement.merge(balance_sheet, on="period").merge(cash_flow_statement, on="period")


def _combined_statement_frame(result: ProFormaResult) -> pd.DataFrame:
    return _statement_frame_for_ratios(result.income_statement, result.balance_sheet, result.cash_flow_statement)


def _depreciation(previous: dict[str, Any], assumptions: ProFormaAssumptions) -> float:
    if assumptions.depreciation_amount is not None:
        return assumptions.depreciation_amount
    return previous["non_current_assets"] * assumptions.depreciation_percentage_of_assets


def _safe_ratio(numerator: float, denominator: float) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def _risk(period: str, code: str, message: str) -> dict[str, str]:
    return {"period": period, "risk": code, "message": message}


def _object_to_float(value: object) -> float:
    return float(value) if isinstance(value, int | float | str) else 0.0
