from __future__ import annotations

import pandas as pd

from financial_accounting_engine.models.account_model import Account
from financial_accounting_engine.validation.schema_validation import (
    OPENING_BALANCE_COLUMNS,
    validate_required_columns,
)


def load_accounts(opening_balances: pd.DataFrame) -> dict[str, Account]:
    validate_required_columns(opening_balances, OPENING_BALANCE_COLUMNS, "opening_balances")
    return {str(record["account_name"]): Account(**record) for record in opening_balances.to_dict("records")}
