from __future__ import annotations

import pandas as pd

from financial_accounting_engine.utils.exceptions import ValidationError

TRANSACTION_COLUMNS = {"transaction_id", "date", "description", "debit_account", "credit_account", "amount", "currency", "category", "source_document", "narration"}
OPENING_BALANCE_COLUMNS = {"account_name", "account_type", "opening_debit_balance", "opening_credit_balance", "period_start_date"}
ASSET_COLUMNS = {"asset_id", "asset_name", "purchase_date", "purchase_cost", "salvage_value", "useful_life", "depreciation_method", "depreciation_rate", "asset_category"}
STATEMENT_COLUMNS = {"period", "revenue", "COGS", "gross_profit", "operating_expenses", "operating_profit", "interest_expense", "tax_expense", "net_profit", "current_assets", "non_current_assets", "total_assets", "current_liabilities", "non_current_liabilities", "total_liabilities", "equity", "operating_cash_flow", "investing_cash_flow", "financing_cash_flow", "opening_cash", "closing_cash"}


def validate_required_columns(df: pd.DataFrame, required: set[str], dataset_name: str) -> list[str]:
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValidationError(f"{dataset_name} missing required columns: {missing}")
    return []
