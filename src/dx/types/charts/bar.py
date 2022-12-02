from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXBarChartConfig(DEXChartBase):
    class Config:
        fields = {
            "bar_label": {"include": True},
            "bar_projection": {"include": True},
            "bar_subcategory": {"include": True},
            "combination_mode": {"include": True},
            "dim1": {"include": True},
            "group_other": {"include": True},
            "metric1": {"include": True},
            "metric3": {"include": True},
            "pro_bar_mode": {"include": True},
            "second_bar_metric": {"include": True},
            "second_metric_style": {"include": True},
            "selected_bar_metrics": {"include": True},
            "sort_columns_by": {"include": True},
        }


class DEXBarChartView(DEXView):
    chart_mode: Literal["bar"] = "bar"
    chart: DEXBarChartConfig = Field(default_factory=DEXBarChartConfig)
