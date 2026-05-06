from __future__ import annotations

from pydantic import BaseModel


class JournalEntry(BaseModel):
    journal_id: str
    date: str
    description: str
    debit_account: str
    credit_account: str
    debit_amount: float
    credit_amount: float
    narration: str | None
    source_document: str | None
    created_at: str
    validation_status: str
