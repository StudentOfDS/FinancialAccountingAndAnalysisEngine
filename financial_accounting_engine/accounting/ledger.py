from __future__ import annotations

import pandas as pd

from financial_accounting_engine.models.account_model import Account

DEBIT_NATURE = {"asset", "expense", "loss", "drawings", "debtor", "stock", "prepaid_expense", "capital_expenditure"}


def post_to_ledgers(journal: pd.DataFrame, accounts: dict[str, Account]) -> pd.DataFrame:
    balances = {name: acc.opening_debit_balance - acc.opening_credit_balance for name, acc in accounts.items()}
    lines: list[dict[str, object]] = []
    for row in journal.sort_values("date").itertuples(index=False):
        for account_name, debit, credit, particulars in [
            (row.debit_account, row.debit_amount, 0.0, f"To {row.credit_account}: {row.description}"),
            (row.credit_account, 0.0, row.credit_amount, f"By {row.debit_account}: {row.description}"),
        ]:
            acc_type = accounts[account_name].account_type
            delta = debit - credit if acc_type in DEBIT_NATURE else credit - debit
            balances[account_name] = balances.get(account_name, 0.0) + delta
            balance = balances[account_name]
            lines.append({
                "account_name": account_name, "date": row.date, "particulars": particulars,
                "debit_amount": debit, "credit_amount": credit, "running_balance": abs(balance),
                "balance_type": "debit" if balance >= 0 else "credit",
            })
    return pd.DataFrame(lines)
