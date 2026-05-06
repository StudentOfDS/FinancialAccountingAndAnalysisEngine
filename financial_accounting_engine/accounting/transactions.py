from __future__ import annotations

import pandas as pd

from financial_accounting_engine.models.account_model import Account
from financial_accounting_engine.models.transaction_model import Transaction
from financial_accounting_engine.utils.exceptions import ValidationError
from financial_accounting_engine.validation.schema_validation import (
    TRANSACTION_COLUMNS,
    validate_required_columns,
)


def validate_transactions(transactions: pd.DataFrame, accounts: dict[str, Account], period_start: str | None = None, period_end: str | None = None) -> list[Transaction]:
    validate_required_columns(transactions, TRANSACTION_COLUMNS, "transactions")
    validated: list[Transaction] = []
    for record in transactions.to_dict("records"):
        txn = Transaction(**record)
        if txn.debit_account not in accounts or txn.credit_account not in accounts:
            raise ValidationError(f"Transaction {txn.transaction_id} references an unknown account.")
        date = pd.to_datetime(txn.date)
        if period_start and date < pd.to_datetime(period_start):
            raise ValidationError(f"Transaction {txn.transaction_id} is before the accounting period.")
        if period_end and date > pd.to_datetime(period_end):
            raise ValidationError(f"Transaction {txn.transaction_id} is after the accounting period.")
        validated.append(txn)
    return validated
