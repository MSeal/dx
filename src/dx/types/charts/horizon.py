from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.charts.summary import DEXSummaryChartView


class DEXHorizonChartConfig(DEXChartBase):
    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "summary_bins": {"include": True},
        }


class DEXHorizonChartView(DEXSummaryChartView):
    # `chart_mode`` is "summary", and within `chart`,
    # `summary_type` is "horizon"
    chart: DEXHorizonChartConfig = Field(default_factory=DEXHorizonChartConfig)
