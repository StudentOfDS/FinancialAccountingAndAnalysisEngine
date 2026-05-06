from financial_accounting_engine.visualization.dupont_charts import dupont_component_chart
from financial_accounting_engine.visualization.ratio_charts import ratio_chart
from financial_accounting_engine.visualization.red_flag_dashboard import red_flag_chart
from financial_accounting_engine.visualization.statement_charts import trend_chart


class VisualizationService:
    def trend(self, df, metrics):
        return trend_chart(df, metrics)

    def ratios(self, ratios_df):
        return ratio_chart(ratios_df)

    def dupont(self, dupont_df):
        return dupont_component_chart(dupont_df)

    def red_flags(self, flags):
        return red_flag_chart(flags)
