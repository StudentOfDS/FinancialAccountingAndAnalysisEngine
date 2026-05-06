from __future__ import annotations

import pandas as pd

from financial_accounting_engine.accounting.accounts import load_accounts
from financial_accounting_engine.accounting.depreciation import depreciation_schedule
from financial_accounting_engine.accounting.journal import generate_journal_entries
from financial_accounting_engine.accounting.ledger import post_to_ledgers
from financial_accounting_engine.accounting.transactions import validate_transactions
from financial_accounting_engine.accounting.trial_balance import create_trial_balance


def run_accounting_cycle(transactions: pd.DataFrame, opening_balances: pd.DataFrame, assets: pd.DataFrame | None = None, period_start: str | None = None, period_end: str | None = None) -> dict[str, object]:
    accounts = load_accounts(opening_balances)
    validated = validate_transactions(transactions, accounts, period_start, period_end)
    journal = generate_journal_entries(validated)
    ledger = post_to_ledgers(journal, accounts)
    trial_balance, trial_summary = create_trial_balance(ledger)
    depreciation = depreciation_schedule(assets) if assets is not None and not assets.empty else pd.DataFrame()
    return {"accounts": accounts, "journal": journal, "ledger": ledger, "trial_balance": trial_balance, "trial_balance_summary": trial_summary, "depreciation": depreciation}
