from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXTreemapConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXTreemapChartView(DEXView):
    chart_mode: Literal["treemap"] = "treemap"
    chart: DEXTreemapConfig = Field(default_factory=DEXTreemapConfig)
