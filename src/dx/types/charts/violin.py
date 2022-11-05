from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXViolinChartConfig(DEXChartBase):
    class Config:
        fields = {
            "summary_type": {"include": True},
            "metric1": {"include": True},
            "dim1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_bins": {"include": True},
            "violin_iqr": {"include": True},
        }


class DEXViolinChartView(DEXView):
    chart_mode: Literal["violin"] = "violin"
    chart: DEXViolinChartConfig = Field(default_factory=DEXViolinChartConfig)
