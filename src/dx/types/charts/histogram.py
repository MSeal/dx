from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.charts.summary import DEXSummaryChartView


class DEXHistogramChartConfig(DEXChartBase):
    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "summary_bins": {"include": True},
        }


class DEXHistogramChartView(DEXSummaryChartView):
    # `chart_mode`` is "summary", and within `chart`,
    # `summary_type` is "histogram"
    chart: DEXHistogramChartConfig = Field(default_factory=DEXHistogramChartConfig)
