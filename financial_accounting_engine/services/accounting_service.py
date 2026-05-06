from financial_accounting_engine.accounting.accounting_cycle import run_accounting_cycle


class AccountingService:
    def run(self, transactions, opening_balances, assets=None, period_start=None, period_end=None):
        return run_accounting_cycle(transactions, opening_balances, assets, period_start, period_end)
