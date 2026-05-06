from __future__ import annotations

import pandas as pd
import pytest

from financial_accounting_engine.accounting.accounting_cycle import run_accounting_cycle
from financial_accounting_engine.accounting.depreciation import depreciation_schedule
from financial_accounting_engine.accounting.trial_balance import create_trial_balance
from financial_accounting_engine.analysis.dupont import dupont_analysis
from financial_accounting_engine.analysis.financial_health import health_score
from financial_accounting_engine.analysis.ratios import calculate_ratios
from financial_accounting_engine.analysis.red_flags import detect_red_flags
from financial_accounting_engine.analysis.vertical_analysis import (
    vertical_balance_sheet,
    vertical_income_statement,
)
from financial_accounting_engine.forecasting.financial_distress import distress_score
from financial_accounting_engine.forecasting.machine_learning_models import (
    ml_forecast_with_safeguard,
)
from financial_accounting_engine.forecasting.scenario_analysis import scenario_assumptions
from financial_accounting_engine.reports.html_exporter import export_html
from financial_accounting_engine.services.forecasting_service import ForecastingService
from financial_accounting_engine.statements.balance_sheet import build_balance_sheet
from financial_accounting_engine.statements.cash_flow import build_cash_flow
from financial_accounting_engine.statements.final_accounts import build_final_accounts
from financial_accounting_engine.utils.exceptions import ValidationError
from financial_accounting_engine.validation.accounting_rules import (
    classify_expenditure,
    split_prepaid_expense,
)
from financial_accounting_engine.validation.financial_statement_validation import (
    validate_statement_rows,
)


def statements() -> pd.DataFrame:
    return pd.DataFrame([
        {"period": "2021", "revenue": 100, "COGS": 60, "gross_profit": 40, "operating_expenses": 20, "operating_profit": 20, "interest_expense": 2, "tax_expense": 4, "net_profit": 14, "current_assets": 50, "non_current_assets": 100, "total_assets": 150, "current_liabilities": 25, "non_current_liabilities": 50, "total_liabilities": 75, "equity": 75, "operating_cash_flow": 16, "investing_cash_flow": -5, "financing_cash_flow": 1, "opening_cash": 10, "closing_cash": 22, "inventory": 10, "receivables": 12, "payables": 8},
        {"period": "2022", "revenue": 120, "COGS": 72, "gross_profit": 48, "operating_expenses": 26, "operating_profit": 22, "interest_expense": 3, "tax_expense": 5, "net_profit": 14, "current_assets": 55, "non_current_assets": 105, "total_assets": 160, "current_liabilities": 30, "non_current_liabilities": 58, "total_liabilities": 88, "equity": 72, "operating_cash_flow": -2, "investing_cash_flow": -4, "financing_cash_flow": 3, "opening_cash": 22, "closing_cash": 19, "inventory": 11, "receivables": 14, "payables": 9},
        {"period": "2023", "revenue": 140, "COGS": 90, "gross_profit": 50, "operating_expenses": 35, "operating_profit": 15, "interest_expense": 4, "tax_expense": 3, "net_profit": 8, "current_assets": 40, "non_current_assets": 110, "total_assets": 150, "current_liabilities": 45, "non_current_liabilities": 65, "total_liabilities": 110, "equity": 40, "operating_cash_flow": 10, "investing_cash_flow": -8, "financing_cash_flow": 0, "opening_cash": 19, "closing_cash": 21, "inventory": 12, "receivables": 20, "payables": 12},
    ])


def opening_balances() -> pd.DataFrame:
    return pd.DataFrame([
        {"account_name": "Cash", "account_type": "asset", "opening_debit_balance": 10000, "opening_credit_balance": 0, "period_start_date": "2024-01-01"},
        {"account_name": "Capital", "account_type": "capital", "opening_debit_balance": 0, "opening_credit_balance": 10000, "period_start_date": "2024-01-01"},
        {"account_name": "Sales", "account_type": "revenue", "opening_debit_balance": 0, "opening_credit_balance": 0, "period_start_date": "2024-01-01"},
        {"account_name": "Rent Expense", "account_type": "expense", "opening_debit_balance": 0, "opening_credit_balance": 0, "period_start_date": "2024-01-01"},
    ])


def transactions() -> pd.DataFrame:
    return pd.DataFrame([
        {"transaction_id": "T1", "date": "2024-01-10", "description": "Cash sales", "debit_account": "Cash", "credit_account": "Sales", "amount": 5000, "currency": "USD", "category": "sales", "source_document": "INV", "narration": "sale"},
        {"transaction_id": "T2", "date": "2024-01-12", "description": "Rent", "debit_account": "Rent Expense", "credit_account": "Cash", "amount": 1000, "currency": "USD", "category": "rent", "source_document": "R", "narration": "rent"},
    ])


def assets() -> pd.DataFrame:
    return pd.DataFrame([
        {"asset_id": "A1", "asset_name": "Machine", "purchase_date": "2024-01-01", "purchase_cost": 10000, "salvage_value": 1000, "useful_life": 3, "depreciation_method": "straight_line", "depreciation_rate": 0.2, "asset_category": "machinery"},
        {"asset_id": "A2", "asset_name": "Furniture", "purchase_date": "2024-01-01", "purchase_cost": 5000, "salvage_value": 500, "useful_life": 5, "depreciation_method": "written_down_value", "depreciation_rate": 0.1, "asset_category": "furniture"},
    ])


def test_accounting_cycle_journal_ledger_trial_balance():
    result = run_accounting_cycle(transactions(), opening_balances(), assets())
    assert len(result["journal"]) == 2
    assert {"account_name", "running_balance", "balance_type"}.issubset(result["ledger"].columns)
    assert result["trial_balance_summary"]["balanced"] is True
    assert "balanced trial balance" in result["trial_balance_summary"]["warning"]


def test_invalid_transaction_missing_account():
    tx = transactions()
    tx.loc[0, "debit_account"] = "Missing"
    with pytest.raises(ValidationError):
        run_accounting_cycle(tx, opening_balances())


def test_depreciation_slm_and_wdv():
    schedule = depreciation_schedule(assets())
    assert schedule.loc[0, "depreciation_for_period"] == 3000
    assert schedule.loc[1, "depreciation_for_period"] == 500


def test_accounting_rules_prepaid_and_classification():
    assert classify_expenditure("Major equipment upgrade") == "capital_expenditure"
    assert classify_expenditure("Office rent") == "revenue_expenditure"
    split = split_prepaid_expense(1200, 3, 12)
    assert split["current_expense"] == 300
    assert split["prepaid_asset"] == 900


def test_final_accounts_and_reconciliations():
    final = build_final_accounts(
        {"opening_stock": 10, "purchases": 50, "purchase_returns": 5, "direct_expenses": 5, "sales": 100, "sales_returns": 0, "closing_stock": 15},
        {"indirect_income": 2, "admin_expenses": 10, "selling_expenses": 5, "distribution_expenses": 0, "finance_costs": 1, "depreciation": 3, "bad_debts": 0, "provisions": 0, "other_operating_expenses": 0},
        {"non_current_assets": 80, "current_assets": 40, "capital": 100, "drawings": 5, "current_liabilities": 10, "non_current_liabilities": 0},
    )
    assert final["trading_account"]["COGS"] == 45
    assert final["profit_and_loss"]["net_profit"] == 38
    assert final["balance_sheet"]["balanced"] is False
    cf = build_cash_flow(10, customer_receipts=100, supplier_payments=50, reported_closing_cash=10)
    assert cf["balanced"] is False
    bs = build_balance_sheet(50, 50, 70, 0, 10, 20, 0)
    assert bs["balanced"] is True


def test_statement_analysis_ratios_dupont_common_size_health_red_flags():
    df = statements()
    ratios = calculate_ratios(df)
    assert "zero_or_invalid_denominator" not in ratios["warning"].dropna().tolist()[:3]
    dup = dupont_analysis(df)
    assert {"net_profit_margin", "asset_turnover", "equity_multiplier", "ROE"}.issubset(dup.columns)
    assert vertical_income_statement(df).filter(like="pct_of_revenue").shape[1] > 0
    assert vertical_balance_sheet(df).filter(like="pct_of_assets").shape[1] > 0
    health = health_score(df)
    assert 0 <= health["score"] <= 100
    flags = detect_red_flags(df)
    assert any(flag["flag"] == "Positive net profit but negative OCF" for flag in flags)


def test_zero_denominator_ratio_safeguard():
    df = statements()
    df.loc[0, "current_liabilities"] = 0
    ratios = calculate_ratios(df.head(1))
    current = ratios[ratios.ratio_name == "current_ratio"].iloc[0]
    assert current.value is None
    assert current.warning == "zero_or_invalid_denominator"


def test_forecasting_safeguards_intervals_scenarios_distress_report():
    df = statements()
    forecast = ForecastingService().forecast(df, periods=2)
    assert {"expected", "lower", "upper", "explanation"}.issubset(forecast.columns)
    assert forecast["explanation"].str.contains("estimates, not guarantees").any()
    ml_values, ml_note = ml_forecast_with_safeguard(df["revenue"], 1)
    assert len(ml_values) == 1
    assert "insufficient observations" in ml_note
    assert "stress" in scenario_assumptions()
    distress = distress_score(df)
    assert distress["method"] == "interpretable_rule_based"
    html = export_html({"health": health_score(df), "sections": {"investor": ["profitability"]}})
    assert "Stakeholder Report" in html


def test_statement_validation_flags_mismatches():
    df = statements()
    df.loc[0, "closing_cash"] = 999
    issues = validate_statement_rows(df)
    assert any(issue["type"] == "cash_flow_mismatch" for issue in issues)


def detailed_opening_balances() -> pd.DataFrame:
    return pd.DataFrame([
        {"account_name": "Cash", "account_type": "asset", "opening_debit_balance": 1000, "opening_credit_balance": 0, "period_start_date": "2024-01-01"},
        {"account_name": "Equipment", "account_type": "asset", "opening_debit_balance": 500, "opening_credit_balance": 0, "period_start_date": "2024-01-01"},
        {"account_name": "Capital", "account_type": "capital", "opening_debit_balance": 0, "opening_credit_balance": 1200, "period_start_date": "2024-01-01"},
        {"account_name": "Accounts Payable", "account_type": "liability", "opening_debit_balance": 0, "opening_credit_balance": 300, "period_start_date": "2024-01-01"},
        {"account_name": "Sales", "account_type": "revenue", "opening_debit_balance": 0, "opening_credit_balance": 0, "period_start_date": "2024-01-01"},
        {"account_name": "Rent Expense", "account_type": "expense", "opening_debit_balance": 0, "opening_credit_balance": 0, "period_start_date": "2024-01-01"},
    ])


def detailed_transactions() -> pd.DataFrame:
    return pd.DataFrame([
        {"transaction_id": "T1", "date": "2024-01-05", "description": "Service revenue", "debit_account": "Cash", "credit_account": "Sales", "amount": 200, "currency": "USD", "category": "sales", "source_document": "INV-1", "narration": "sale"},
        {"transaction_id": "T2", "date": "2024-01-10", "description": "Rent paid", "debit_account": "Rent Expense", "credit_account": "Cash", "amount": 50, "currency": "USD", "category": "rent", "source_document": "RCPT-1", "narration": "rent"},
    ])


def _trial_row(result: dict[str, object], account_name: str) -> pd.Series:
    trial_balance = result["trial_balance"]
    assert isinstance(trial_balance, pd.DataFrame)
    rows = trial_balance[trial_balance.account_name == account_name]
    assert len(rows) == 1
    return rows.iloc[0]


def _latest_ledger_row(result: dict[str, object], account_name: str) -> pd.Series:
    ledger = result["ledger"]
    assert isinstance(ledger, pd.DataFrame)
    rows = ledger[ledger.account_name == account_name]
    assert len(rows) >= 1
    return rows.iloc[-1]


def test_opening_only_capital_and_asset_accounts_appear_in_trial_balance():
    result = run_accounting_cycle(detailed_transactions(), detailed_opening_balances())

    capital = _trial_row(result, "Capital")
    equipment = _trial_row(result, "Equipment")

    assert capital.credit_balance == 1200
    assert capital.debit_balance == 0
    assert equipment.debit_balance == 500
    assert equipment.credit_balance == 0


def test_liability_opening_credit_balance_remains_credit():
    result = run_accounting_cycle(detailed_transactions(), detailed_opening_balances())

    liability = _trial_row(result, "Accounts Payable")
    latest_ledger = _latest_ledger_row(result, "Accounts Payable")

    assert liability.credit_balance == 300
    assert latest_ledger.signed_balance == -300
    assert latest_ledger.balance_type == "credit"


def test_revenue_credit_and_expense_debit_transactions_update_correct_balance_side():
    result = run_accounting_cycle(detailed_transactions(), detailed_opening_balances())

    sales = _trial_row(result, "Sales")
    rent = _trial_row(result, "Rent Expense")
    sales_ledger = _latest_ledger_row(result, "Sales")
    rent_ledger = _latest_ledger_row(result, "Rent Expense")

    assert sales.credit_balance == 200
    assert sales_ledger.signed_balance == -200
    assert sales_ledger.balance_type == "credit"
    assert rent.debit_balance == 50
    assert rent_ledger.signed_balance == 50
    assert rent_ledger.balance_type == "debit"


def test_trial_balance_balances_with_openings_and_journal_entries():
    result = run_accounting_cycle(detailed_transactions(), detailed_opening_balances())
    summary = result["trial_balance_summary"]

    assert summary["balanced"] is True
    assert summary["total_debit"] == 1750
    assert summary["total_credit"] == 1750
    assert summary["difference"] == 0


def test_trial_balance_fails_when_ledger_is_intentionally_mismatched():
    result = run_accounting_cycle(detailed_transactions(), detailed_opening_balances())
    ledger = result["ledger"].copy()
    assert isinstance(ledger, pd.DataFrame)
    ledger = ledger[ledger.account_name != "Sales"]

    _, summary = create_trial_balance(ledger)

    assert summary["balanced"] is False
    assert summary["difference"] == 200


def test_wdv_depreciation_compounds_over_multiple_periods():
    wdv_assets = pd.DataFrame([
        {"asset_id": "A1", "asset_name": "Machine", "purchase_date": "2024-01-01", "purchase_cost": 10000, "salvage_value": 1000, "useful_life": 5, "depreciation_method": "wdv", "depreciation_rate": 0.1, "asset_category": "machinery"},
    ])

    schedule = depreciation_schedule(wdv_assets, periods=3)

    assert schedule.loc[0, "depreciation_for_period"] == 2710
    assert schedule.loc[0, "closing_book_value"] == 7290


def test_unsupported_depreciation_method_raises_validation_error():
    bad_assets = assets().copy()
    bad_assets.loc[0, "depreciation_method"] = "sum_of_years_digits"

    with pytest.raises(ValidationError, match="Unsupported depreciation method"):
        depreciation_schedule(bad_assets)
