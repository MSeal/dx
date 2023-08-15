from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXFunnelChartConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXFunnelChartChartView(DEXView):
    chart_mode: Literal["funnel_chart"] = "funnel_chart"
    chart: DEXFunnelChartConfig = Field(default_factory=DEXFunnelChartConfig)
