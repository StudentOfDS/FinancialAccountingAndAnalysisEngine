from __future__ import annotations

import pandas as pd

from financial_accounting_engine.models.account_model import Account


def post_to_ledgers(journal: pd.DataFrame, accounts: dict[str, Account]) -> pd.DataFrame:
    """Post journal entries using one signed convention: debit-positive, credit-negative.

    Opening balances are emitted as ledger rows for every account so downstream trial
    balances include opening-only accounts that had no current-period movement.
    """
    balances = _opening_signed_balances(accounts)
    lines = _opening_ledger_lines(accounts, balances)

    if journal.empty:
        return pd.DataFrame(lines)

    for row in journal.sort_values("date").itertuples(index=False):
        for account_name, debit, credit, particulars in [
            (row.debit_account, row.debit_amount, 0.0, f"To {row.credit_account}: {row.description}"),
            (row.credit_account, 0.0, row.credit_amount, f"By {row.debit_account}: {row.description}"),
        ]:
            balances[account_name] = balances.get(account_name, 0.0) + float(debit) - float(credit)
            lines.append(_ledger_line(account_name, row.date, particulars, debit, credit, balances[account_name]))
    return pd.DataFrame(lines)


def _opening_signed_balances(accounts: dict[str, Account]) -> dict[str, float]:
    return {
        name: float(account.opening_debit_balance) - float(account.opening_credit_balance)
        for name, account in accounts.items()
    }


def _opening_ledger_lines(accounts: dict[str, Account], balances: dict[str, float]) -> list[dict[str, object]]:
    lines: list[dict[str, object]] = []
    for account_name, account in accounts.items():
        date = account.period_start_date or "opening"
        lines.append(_ledger_line(account_name, date, "Opening balance", 0.0, 0.0, balances[account_name]))
    return lines


def _ledger_line(
    account_name: str,
    date: str,
    particulars: str,
    debit_amount: float,
    credit_amount: float,
    signed_balance: float,
) -> dict[str, object]:
    return {
        "account_name": account_name,
        "date": date,
        "particulars": particulars,
        "debit_amount": float(debit_amount),
        "credit_amount": float(credit_amount),
        "signed_balance": signed_balance,
        "running_balance": abs(signed_balance),
        "balance_type": "debit" if signed_balance >= 0 else "credit",
    }
