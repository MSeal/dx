from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXBarChartConfig(DEXChartBase):
    class Config:
        fields = {
            "bar_projection": {"include": True},
            "second_bar_metric": {"include": True},
            "dim1": {"include": True},
            "metric1": {"include": True},
            "group_other": {"include": True},
            "sort_columns_by": {"include": True},
            "metric3": {"include": True},
            "pro_bar_mode": {"include": True},
            "bar_label": {"include": True},
        }


class DEXBarChartView(DEXView):
    chart_type: Literal["bar"] = "bar"
    chart: DEXBarChartConfig = Field(default_factory=DEXBarChartConfig)
