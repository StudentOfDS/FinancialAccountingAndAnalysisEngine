from __future__ import annotations

ACCOUNT_TYPES = {
    "asset", "liability", "capital", "equity", "revenue", "expense", "gain", "loss", "drawings",
    "debtor", "creditor", "stock", "depreciation", "accrual", "prepaid_expense", "accrued_income",
    "unearned_income", "capital_expenditure", "revenue_expenditure",
}
VALID_CURRENCIES = {"USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD"}
CAPITAL_EXPENDITURE_KEYWORDS = {"machinery", "furniture", "installation", "building", "construction", "equipment upgrade", "vehicle", "computer"}
REVENUE_EXPENDITURE_KEYWORDS = {"rent", "salary", "electricity", "repairs", "office", "selling", "admin", "distribution", "utilities"}
GAAP_CONCEPTS = [
    "business entity", "money measurement", "going concern", "accounting period", "accrual",
    "matching", "consistency", "conservatism/prudence", "materiality", "dual aspect",
]
