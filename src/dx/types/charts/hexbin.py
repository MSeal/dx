from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView

__all__ = ["DEXHexbinChartView"]


class DEXHexbinChartConfig(DEXChartBase):
    class Config:
        fields = {
            "metric1": {"include": True},
            "metric2": {"include": True},
        }


class DEXHexbinChartView(DEXView):
    chart_mode: Literal["hexbin"] = "hexbin"
    chart: DEXHexbinChartConfig = Field(default_factory=DEXHexbinChartConfig)
