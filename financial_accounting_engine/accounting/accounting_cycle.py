from __future__ import annotations

import pandas as pd

from financial_accounting_engine.accounting.accounts import load_accounts
from financial_accounting_engine.accounting.depreciation import depreciation_schedule
from financial_accounting_engine.accounting.journal import generate_journal_entries
from financial_accounting_engine.accounting.ledger import post_to_ledgers
from financial_accounting_engine.accounting.transactions import validate_transactions
from financial_accounting_engine.accounting.trial_balance import create_trial_balance
from financial_accounting_engine.validation.reconciliation import (
    reconcile_journal_totals,
    reconcile_ledger_to_trial_balance,
)


def run_accounting_cycle(transactions: pd.DataFrame, opening_balances: pd.DataFrame, assets: pd.DataFrame | None = None, period_start: str | None = None, period_end: str | None = None) -> dict[str, object]:
    accounts = load_accounts(opening_balances)
    validated = validate_transactions(transactions, accounts, period_start, period_end)
    journal = generate_journal_entries(validated)
    ledger = post_to_ledgers(journal, accounts)
    trial_balance, trial_summary = create_trial_balance(ledger)
    journal_reconciliation = reconcile_journal_totals(journal)
    ledger_trial_balance_reconciliation = reconcile_ledger_to_trial_balance(ledger, trial_balance)
    depreciation = depreciation_schedule(assets) if assets is not None and not assets.empty else pd.DataFrame()
    return {
        "accounts": accounts,
        "journal": journal,
        "ledger": ledger,
        "trial_balance": trial_balance,
        "trial_balance_summary": trial_summary,
        "journal_reconciliation": journal_reconciliation,
        "ledger_trial_balance_reconciliation": ledger_trial_balance_reconciliation,
        "depreciation": depreciation,
    }
