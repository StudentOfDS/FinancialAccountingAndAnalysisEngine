from __future__ import annotations

from typing import Any

import pandas as pd


def create_trial_balance(ledger: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    if ledger.empty:
        return _empty_trial_balance(), {"total_debit": 0.0, "total_credit": 0.0, "difference": 0.0, "balanced": True, "warning": _warning()}

    latest = ledger.groupby("account_name", as_index=False).tail(1)
    rows = [_trial_balance_row(row) for row in latest.itertuples(index=False)]
    trial_balance = pd.DataFrame(rows).sort_values("account_name").reset_index(drop=True)
    total_debit = float(trial_balance.debit_balance.sum())
    total_credit = float(trial_balance.credit_balance.sum())
    difference = total_debit - total_credit
    summary = {
        "total_debit": total_debit,
        "total_credit": total_credit,
        "difference": difference,
        "balanced": abs(difference) <= 0.01,
        "warning": _warning(),
    }
    return trial_balance, summary


def _trial_balance_row(row: Any) -> dict[str, float | str]:
    signed_balance = float(getattr(row, "signed_balance", 0.0))
    if signed_balance == 0.0:
        running_balance = float(getattr(row, "running_balance", 0.0))
        balance_type = str(getattr(row, "balance_type", "debit"))
        signed_balance = running_balance if balance_type == "debit" else -running_balance
    return {
        "account_name": str(row.account_name),
        "debit_balance": signed_balance if signed_balance >= 0 else 0.0,
        "credit_balance": abs(signed_balance) if signed_balance < 0 else 0.0,
    }


def _empty_trial_balance() -> pd.DataFrame:
    return pd.DataFrame(columns=["account_name", "debit_balance", "credit_balance"])


def _warning() -> str:
    return "A balanced trial balance proves only equality of debit and credit totals; it does not prove that all accounting errors are absent."
