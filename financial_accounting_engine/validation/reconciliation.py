from __future__ import annotations

import pandas as pd


def reconcile_cash_flow(opening_cash: float, operating: float, investing: float, financing: float, closing_cash: float, tolerance: float = 0.01) -> dict[str, object]:
    expected = opening_cash + operating + investing + financing
    difference = expected - closing_cash
    return {"expected_closing_cash": expected, "reported_closing_cash": closing_cash, "difference": difference, "balanced": abs(difference) <= tolerance}


def reconcile_balance_sheet(total_assets: float, total_liabilities: float, equity: float, tolerance: float = 0.01) -> dict[str, object]:
    difference = total_assets - (total_liabilities + equity)
    return {"difference": difference, "balanced": abs(difference) <= tolerance}


def reconcile_journal_totals(journal: pd.DataFrame, tolerance: float = 0.01) -> dict[str, object]:
    total_debit = _sum_column(journal, "debit_amount")
    total_credit = _sum_column(journal, "credit_amount")
    difference = total_debit - total_credit
    return {"total_debit": total_debit, "total_credit": total_credit, "difference": difference, "balanced": abs(difference) <= tolerance}


def reconcile_ledger_to_trial_balance(ledger: pd.DataFrame, trial_balance: pd.DataFrame, tolerance: float = 0.01) -> dict[str, object]:
    if ledger.empty and trial_balance.empty:
        return {"balanced": True, "differences": [], "account_count": 0}

    ledger_balances = _latest_ledger_signed_balances(ledger)
    trial_balances = _trial_balance_signed_balances(trial_balance)
    accounts = sorted(set(ledger_balances) | set(trial_balances))
    differences = [
        {"account_name": account, "ledger_signed_balance": ledger_balances.get(account, 0.0), "trial_balance_signed_balance": trial_balances.get(account, 0.0), "difference": ledger_balances.get(account, 0.0) - trial_balances.get(account, 0.0)}
        for account in accounts
        if abs(ledger_balances.get(account, 0.0) - trial_balances.get(account, 0.0)) > tolerance
    ]
    return {"balanced": not differences, "differences": differences, "account_count": len(accounts)}


def _sum_column(df: pd.DataFrame, column: str) -> float:
    if df.empty or column not in df.columns:
        return 0.0
    return float(df[column].sum())


def _latest_ledger_signed_balances(ledger: pd.DataFrame) -> dict[str, float]:
    if ledger.empty:
        return {}
    latest = ledger.groupby("account_name", as_index=False).tail(1)
    balances: dict[str, float] = {}
    for row in latest.itertuples(index=False):
        signed_balance = float(getattr(row, "signed_balance", 0.0))
        if signed_balance == 0.0:
            running_balance = float(getattr(row, "running_balance", 0.0))
            balance_type = str(getattr(row, "balance_type", "debit"))
            signed_balance = running_balance if balance_type == "debit" else -running_balance
        balances[str(row.account_name)] = signed_balance
    return balances


def _trial_balance_signed_balances(trial_balance: pd.DataFrame) -> dict[str, float]:
    if trial_balance.empty:
        return {}
    return {
        str(row.account_name): float(row.debit_balance) - float(row.credit_balance)
        for row in trial_balance.itertuples(index=False)
    }
