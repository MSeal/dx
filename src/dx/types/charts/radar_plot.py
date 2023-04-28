from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXRadarPlotConfig(DEXChartBase):
    pass


class DEXRadarPlotChartView(DEXView):
    chart_mode: Literal["radar_plot"] = "radar_plot"
    chart: DEXRadarPlotConfig = Field(default_factory=DEXRadarPlotConfig)
