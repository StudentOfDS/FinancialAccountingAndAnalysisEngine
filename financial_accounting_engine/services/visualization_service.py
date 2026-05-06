from financial_accounting_engine.visualization.ratio_charts import ratio_chart
from financial_accounting_engine.visualization.statement_charts import trend_chart


class VisualizationService:
    def trend(self, df, metrics):
        return trend_chart(df, metrics)
    def ratios(self, ratios_df):
        return ratio_chart(ratios_df)
