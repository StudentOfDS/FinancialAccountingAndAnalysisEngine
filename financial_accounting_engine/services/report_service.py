from financial_accounting_engine.analysis.stakeholder_report import build_stakeholder_report


class ReportService:
    def stakeholder_report(self, statements):
        return build_stakeholder_report(statements)
