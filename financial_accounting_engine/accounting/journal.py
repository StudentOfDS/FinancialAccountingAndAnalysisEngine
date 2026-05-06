from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from financial_accounting_engine.models.journal_model import JournalEntry
from financial_accounting_engine.models.transaction_model import Transaction


def generate_journal_entries(transactions: list[Transaction]) -> pd.DataFrame:
    entries = []
    created_at = datetime.now(timezone.utc).isoformat()
    for idx, txn in enumerate(transactions, start=1):
        entry = JournalEntry(
            journal_id=f"J{idx:06d}", date=txn.date, description=txn.description,
            debit_account=txn.debit_account, credit_account=txn.credit_account,
            debit_amount=txn.amount, credit_amount=txn.amount, narration=txn.narration,
            source_document=txn.source_document, created_at=created_at, validation_status="valid",
        )
        entries.append(entry.model_dump())
    return pd.DataFrame(entries)
