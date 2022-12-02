from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXScatterChartConfig(DEXChartBase):
    class Config:
        fields = {
            "formula_display": {"include": True},
            "marginal_graphics": {"include": True},
            "metric1": {"include": True},
            "metric2": {"include": True},
            "scatterplot_size": {"include": True},
            "selected_metrics": {"include": True},
            "show_contours": {"include": True},
            "splom_mode": {"include": True},
            "trend_line": {"include": True},
        }


class DEXScatterChartView(DEXView):
    chart_mode: Literal["scatter"] = "scatter"
    chart: DEXScatterChartConfig = Field(default_factory=DEXScatterChartConfig)
