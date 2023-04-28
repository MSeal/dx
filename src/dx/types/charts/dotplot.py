from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXDotPlotConfig(DEXChartBase):
    pass


class DEXDotPlotChartView(DEXView):
    chart_mode: Literal["dotplot"] = "dotplot"
    chart: DEXDotPlotConfig = Field(default_factory=DEXDotPlotConfig)
