# Architecture

The engine is organized around service classes that orchestrate pure domain modules. Streamlit calls services; services call validation, accounting, statement, analysis, forecasting, risk and reporting modules. This keeps UI concerns separate from finance logic.
