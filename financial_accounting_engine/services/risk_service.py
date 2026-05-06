from financial_accounting_engine.forecasting.financial_distress import distress_score


class RiskService:
    def score(self, statements):
        return distress_score(statements)
