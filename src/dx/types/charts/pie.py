from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXPieChartConfig(DEXChartBase):
    class Config:
        fields = {
            "show_total": {"include": True},
            "dim1": {"include": True},  # split by
            "metric1": {"include": True},  # slice size metric
            "pie_label_type": {"include": True},
            "pie_label_contents": {"include": True},
        }


class DEXPieChartView(DEXView):
    chart_mode: Literal["pie"] = "pie"
    chart: DEXPieChartConfig = Field(default_factory=DEXPieChartConfig)
