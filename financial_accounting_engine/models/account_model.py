from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from financial_accounting_engine.utils.constants import ACCOUNT_TYPES


class Account(BaseModel):
    account_name: str
    account_type: str
    opening_debit_balance: float = Field(default=0, ge=0)
    opening_credit_balance: float = Field(default=0, ge=0)
    period_start_date: str | None = None

    @field_validator("account_type")
    @classmethod
    def valid_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in ACCOUNT_TYPES:
            raise ValueError(f"Unsupported account type: {value}")
        return normalized
