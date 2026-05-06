import streamlit as st

from financial_accounting_engine.models.pro_forma_model import ProFormaAssumptions
from financial_accounting_engine.services.pro_forma_service import ProFormaService
from financial_accounting_engine.utils.dataframe_helpers import normalize_columns, read_tabular_file

st.title("Forecasting and Pro Forma Scenario Lab")
st.caption("Build projected statements, ratios, reconciliations, and risk warnings from scenario assumptions.")

uploaded = st.file_uploader("Upload historical financial statements CSV/Excel", type=["csv", "xlsx", "xls"])
if uploaded:
    df = normalize_columns(read_tabular_file(uploaded))
    st.subheader("Scenario assumptions")
    col1, col2, col3 = st.columns(3)
    with col1:
        revenue_growth = st.number_input("Revenue growth rate", value=0.05, step=0.01, format="%.4f")
        cogs_pct = st.number_input("COGS % of revenue", value=0.60, min_value=0.0, step=0.01, format="%.4f")
        opex_pct = st.number_input("Operating expense % of revenue", value=0.20, min_value=0.0, step=0.01, format="%.4f")
    with col2:
        depreciation = st.number_input("Depreciation amount", value=0.0, step=100.0)
        interest = st.number_input("Interest expense", value=0.0, step=100.0)
        tax_rate = st.number_input("Tax rate", value=0.25, min_value=0.0, max_value=1.0, step=0.01, format="%.4f")
    with col3:
        receivables_days = st.number_input("Receivables days", value=30.0, min_value=0.0, step=1.0)
        inventory_days = st.number_input("Inventory days", value=30.0, min_value=0.0, step=1.0)
        payables_days = st.number_input("Payables days", value=30.0, min_value=0.0, step=1.0)
    capex = st.number_input("Capex", value=0.0, step=100.0)
    debt_change = st.number_input("Debt change", value=0.0, step=100.0)
    dividends = st.number_input("Dividend/drawings", value=0.0, step=100.0)
    forecast_periods = st.number_input("Forecast periods", value=1, min_value=1, step=1)
    auto_balance = st.checkbox("Use financing plug to reconcile projected balance sheet", value=True)

    if st.button("Run pro forma projection"):
        assumptions = ProFormaAssumptions(
            revenue_growth_rate=revenue_growth,
            cogs_percentage_of_revenue=cogs_pct,
            operating_expense_percentage_of_revenue=opex_pct,
            depreciation_amount=depreciation,
            interest_expense=interest,
            tax_rate=tax_rate,
            receivables_days=receivables_days,
            inventory_days=inventory_days,
            payables_days=payables_days,
            capex=capex,
            debt_change=debt_change,
            dividend_or_drawings=dividends,
            forecast_periods=int(forecast_periods),
            auto_balance=auto_balance,
        )
        result = ProFormaService().project(df, assumptions)
        tabs = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow", "Ratios", "Risks"])
        with tabs[0]:
            st.dataframe(result.income_statement, use_container_width=True)
        with tabs[1]:
            st.dataframe(result.balance_sheet, use_container_width=True)
            st.json(result.reconciliation)
        with tabs[2]:
            st.dataframe(result.cash_flow_statement, use_container_width=True)
        with tabs[3]:
            st.dataframe(result.ratios, use_container_width=True)
        with tabs[4]:
            st.json(result.risk_warnings)
else:
    st.info("Upload financial statements to run pro forma projections.")
