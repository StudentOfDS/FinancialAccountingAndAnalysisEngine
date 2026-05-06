import streamlit as st

from financial_accounting_engine.validation.accounting_rules import (
    classify_expenditure,
    split_prepaid_expense,
    syllabus_concepts,
)

st.title("Accounting Rules and Classification")
description = st.text_input("Description", "Machinery installation charges")
st.write("Classification:", classify_expenditure(description))
st.write("GAAP concepts implemented:", syllabus_concepts())
st.write("Prepaid example:", split_prepaid_expense(12000, 3, 12))
