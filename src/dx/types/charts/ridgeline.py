from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.charts.summary import DEXSummaryChartView


class DEXRidgelineChartConfig(DEXChartBase):
    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "summary_bins": {"include": True},
        }


class DEXRidgelineChartView(DEXSummaryChartView):
    # `chart_mode`` is "summary", and within `chart`,
    # `summary_type` is "ridgeline"
    chart: DEXRidgelineChartConfig = Field(default_factory=DEXRidgelineChartConfig)
