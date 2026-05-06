class FinanceEngineError(Exception):
    """Base exception for finance engine failures."""


class ValidationError(FinanceEngineError):
    """Raised when source data violates accounting or statement rules."""


class ReconciliationError(FinanceEngineError):
    """Raised when accounting reconciliations fail."""
