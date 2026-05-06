# Financial Accounting, Analysis, Visualization, and Forecasting Intelligence System

A production-oriented Python/Streamlit system for the full finance workflow:

`Raw data -> validation -> journal entries -> ledgers -> trial balance -> adjustments/depreciation -> final accounts -> income statement/balance sheet/cash-flow statement -> vertical/common-size analysis -> ratio analysis -> DuPont analysis -> visualization -> forecasting -> scenario/distress analysis -> stakeholder report`.

## Operating modes

1. **Accounting Builder Mode** accepts transactions, opening balances, adjustments and assets to generate journals, ledgers, trial balance, depreciation, final accounts, statements, analysis, charts, forecasts and reports.
2. **Financial Analyst Mode** accepts financial statements to produce vertical/common-size analysis, ratios, DuPont, trends, forecasting, scenarios, distress scoring and stakeholder reports.

## Architecture

The package is modular:

- `accounting/`: account validation, transactions, journals, ledgers, trial balance, depreciation and accounting cycle orchestration.
- `statements/`: trading account, profit and loss, balance sheet, income statement, cash-flow and pro forma statements.
- `analysis/`: ratios, DuPont, vertical/common-size analysis, health scoring, red flags and stakeholder reporting.
- `forecasting/`: baselines, time-series safeguards, ML safeguards, backtesting, intervals, scenarios, distress scoring and explanations.
- `visualization/`: Plotly charts where every chart answers a business question.
- `services/`: clean orchestration classes for app/API usage.
- `reports/`: HTML, Excel, CSV and PDF-text export helpers.
- `validation/`: schema, accounting rule, reconciliation, data quality and forecast validation.

## Run

```bash
pip install -r requirements.txt
streamlit run financial_accounting_engine/app/streamlit_app.py
```

## Test

```bash
pytest
ruff check .
mypy financial_accounting_engine
```

## Accounting and analysis concepts covered

The implementation covers accounting terms, GAAP concepts, capital/revenue expenditure classification, matching concept prepaid splits, accounting cycle, journal, ledger, trial balance warning, SLM/WDV depreciation, final accounts, corporate statements, vertical/common-size statements, liquidity/leverage/profitability/activity ratios, DuPont analysis, cash-flow reconciliation, health scoring, red flags, forecasting safeguards, scenario analysis, distress scoring and stakeholder views.
