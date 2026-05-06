import streamlit as st

from financial_accounting_engine.utils.dataframe_helpers import normalize_columns, read_tabular_file
from financial_accounting_engine.validation.data_quality import data_quality_report

st.title("Upload Data")
file = st.file_uploader("CSV or Excel", type=["csv", "xlsx", "xls"])
if file:
    df = normalize_columns(read_tabular_file(file))
    st.dataframe(df)
    st.json(data_quality_report(df))
