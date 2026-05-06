from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator

from financial_accounting_engine.utils.constants import VALID_CURRENCIES


class Transaction(BaseModel):
    transaction_id: str
    date: str
    description: str
    debit_account: str
    credit_account: str
    amount: float = Field(gt=0)
    currency: str
    category: str
    source_document: str | None = None
    narration: str | None = None

    @field_validator("currency")
    @classmethod
    def valid_currency(cls, value: str) -> str:
        code = value.strip().upper()
        if code not in VALID_CURRENCIES:
            raise ValueError(f"Unsupported currency: {value}")
        return code

    @model_validator(mode="after")
    def debit_credit_distinct(self):
        if self.debit_account.strip().lower() == self.credit_account.strip().lower():
            raise ValueError("Debit and credit accounts must be different.")
        return self
