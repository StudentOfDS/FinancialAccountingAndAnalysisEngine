from __future__ import annotations

import streamlit as st

from financial_accounting_engine.services.analysis_service import AnalysisService
from financial_accounting_engine.services.forecasting_service import ForecastingService
from financial_accounting_engine.services.report_service import ReportService
from financial_accounting_engine.services.risk_service import RiskService
from financial_accounting_engine.services.visualization_service import VisualizationService
from financial_accounting_engine.utils.dataframe_helpers import normalize_columns, read_tabular_file
from financial_accounting_engine.validation.schema_validation import (
    STATEMENT_COLUMNS,
    validate_required_columns,
)

st.set_page_config(page_title="Financial Accounting Intelligence", layout="wide")
st.title("Financial Accounting, Analysis, Visualization, and Forecasting Intelligence System")
st.caption("Raw data → validation → statements → analysis → visualization → forecasting → distress scoring → stakeholder reporting")

mode = st.sidebar.radio("Operating mode", ["Financial Analyst Mode", "Accounting Builder Mode"])
st.sidebar.info("Use the pages in this app package for dedicated workflows. This home page runs the analyst pipeline end-to-end.")

uploaded = st.file_uploader("Upload financial statements CSV/Excel", type=["csv", "xlsx", "xls"])
if uploaded:
    df = normalize_columns(read_tabular_file(uploaded))
    try:
        validate_required_columns(df, STATEMENT_COLUMNS, "financial_statements")
        st.success("Schema validation passed.")
        st.dataframe(df, use_container_width=True)
        analysis = AnalysisService().analyze(df)
        forecast = ForecastingService().forecast(df)
        distress = RiskService().score(df)
        report_service = ReportService()
        visualization_service = VisualizationService()
        report = report_service.stakeholder_report(df)
        tabs = st.tabs(["Ratios", "DuPont", "Common-size", "Charts", "Forecast", "Risk", "Stakeholder report"])
        with tabs[0]:
            st.dataframe(analysis["ratios"], use_container_width=True)
        with tabs[1]:
            st.dataframe(analysis["dupont"], use_container_width=True)
            st.plotly_chart(visualization_service.dupont(analysis["dupont"]), use_container_width=True)
        with tabs[2]:
            st.dataframe(analysis["vertical_income_statement"], use_container_width=True)
            st.dataframe(analysis["vertical_balance_sheet"], use_container_width=True)
        with tabs[3]:
            st.plotly_chart(visualization_service.trend(df, ["revenue", "gross_profit", "operating_profit", "net_profit", "total_assets", "total_liabilities", "equity", "operating_cash_flow", "investing_cash_flow", "financing_cash_flow"]), use_container_width=True)
            st.plotly_chart(visualization_service.red_flags(analysis["red_flags"] if isinstance(analysis["red_flags"], list) else []), use_container_width=True)
        with tabs[4]:
            st.warning("Predictions are estimates, not guarantees.")
            st.dataframe(forecast, use_container_width=True)
        with tabs[5]:
            st.json(distress)
        with tabs[6]:
            st.json(report)
            st.download_button("Download HTML report", report_service.html(report), file_name="stakeholder_report.html")
    except Exception as exc:
        st.error(str(exc))
else:
    st.info("Upload a CSV or Excel file with the required statement schema to begin.")
    st.write("Selected mode:", mode)
