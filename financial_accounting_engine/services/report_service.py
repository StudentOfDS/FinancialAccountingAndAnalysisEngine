from financial_accounting_engine.analysis.stakeholder_report import build_stakeholder_report
from financial_accounting_engine.reports.html_exporter import export_html


class ReportService:
    def stakeholder_report(self, statements):
        return build_stakeholder_report(statements)

    def html(self, report):
        return export_html(report)
