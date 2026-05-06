from financial_accounting_engine.statements.final_accounts import build_final_accounts


class StatementService:
    def final_accounts(self, trading_inputs, pnl_inputs, balance_sheet_inputs):
        return build_final_accounts(trading_inputs, pnl_inputs, balance_sheet_inputs)
