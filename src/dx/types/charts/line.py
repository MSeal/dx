from typing import Literal

from pydantic import Field

from dx.types.charts._configs import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXLineChartConfig(DEXChartBase):
    class Config:
        fields = {
            "bounding_type": {"include": True},
            "combination_mode": {"include": True},
            "line_smoothing": {"include": True},
            "line_width": {"include": True},
            "selected_metrics": {"include": True},
            "zero_base_line": {"include": True},
        }


class DEXLineChartView(DEXView):
    chart_type: Literal["line"] = "line"
    chart: DEXLineChartConfig = Field(default_factory=DEXLineChartConfig)
