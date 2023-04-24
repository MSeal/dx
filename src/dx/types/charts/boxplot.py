from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.charts.summary import DEXSummaryChartView


class DEXBoxplotChartConfig(DEXChartBase):
    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "boxplot_outliers": {"include": True},
        }


class DEXBoxplotChartView(DEXSummaryChartView):
    # `chart_mode`` is "summary", and within `chart`,
    # `summary_type` is "boxplot"
    chart: DEXBoxplotChartConfig = Field(default_factory=DEXBoxplotChartConfig)
