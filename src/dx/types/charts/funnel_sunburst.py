from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXFunnelSunburstConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXFunnelSunburstChartView(DEXView):
    chart_mode: Literal["funnel_sunburst"] = "funnel_sunburst"
    chart: DEXFunnelSunburstConfig = Field(default_factory=DEXFunnelSunburstConfig)
