from __future__ import annotations

from pydantic import BaseModel


class LedgerLine(BaseModel):
    account_name: str
    date: str
    particulars: str
    debit_amount: float
    credit_amount: float
    running_balance: float
    balance_type: str
