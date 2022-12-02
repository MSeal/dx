from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXLineChartConfig(DEXChartBase):
    class Config:
        fields = {
            "bounding_type": {"include": True},
            "combination_mode": {"include": True},
            "line_smoothing": {"include": True},
            "line_type": {"include": True},
            "multi_axis_line": {"include": True},
            "selected_metrics": {"include": True},
            "split_lines_by": {"include": True},
            "timeseries_sort": {"include": True},
            "zero_baseline": {"include": True},
        }


class DEXLineChartView(DEXView):
    chart_mode: Literal["line"] = "line"
    chart: DEXLineChartConfig = Field(default_factory=DEXLineChartConfig)
