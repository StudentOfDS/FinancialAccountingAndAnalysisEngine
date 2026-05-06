from __future__ import annotations

from financial_accounting_engine.utils.constants import (
    CAPITAL_EXPENDITURE_KEYWORDS,
    GAAP_CONCEPTS,
    REVENUE_EXPENDITURE_KEYWORDS,
)


def classify_expenditure(description: str, category: str = "") -> str:
    text = f"{description} {category}".lower()
    if any(word in text for word in CAPITAL_EXPENDITURE_KEYWORDS):
        return "capital_expenditure"
    if any(word in text for word in REVENUE_EXPENDITURE_KEYWORDS):
        return "revenue_expenditure"
    return "unclassified"


def split_prepaid_expense(amount: float, months_consumed: int, total_months: int) -> dict[str, float | str]:
    if total_months <= 0 or months_consumed < 0 or months_consumed > total_months:
        raise ValueError("Prepaid split requires 0 <= months_consumed <= total_months.")
    expense = amount * months_consumed / total_months
    prepaid_asset = amount - expense
    return {"current_expense": expense, "prepaid_asset": prepaid_asset, "concept": "matching"}


def syllabus_concepts() -> list[str]:
    return GAAP_CONCEPTS.copy()
