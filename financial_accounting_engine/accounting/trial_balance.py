from __future__ import annotations

import pandas as pd


def create_trial_balance(ledger: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    rows = []
    if ledger.empty:
        return pd.DataFrame(columns=["account_name", "debit_balance", "credit_balance"]), {"balanced": True, "difference": 0.0, "warning": _warning()}
    latest = ledger.sort_values("date").groupby("account_name", as_index=False).tail(1)
    for row in latest.itertuples(index=False):
        rows.append({"account_name": row.account_name, "debit_balance": row.running_balance if row.balance_type == "debit" else 0.0, "credit_balance": row.running_balance if row.balance_type == "credit" else 0.0})
    tb = pd.DataFrame(rows).sort_values("account_name")
    total_debit = float(tb.debit_balance.sum())
    total_credit = float(tb.credit_balance.sum())
    summary = {"total_debit": total_debit, "total_credit": total_credit, "difference": total_debit - total_credit, "balanced": abs(total_debit - total_credit) <= 0.01, "warning": _warning()}
    return tb, summary


def _warning() -> str:
    return "A balanced trial balance proves only equality of debit and credit totals; it does not prove that all accounting errors are absent."
